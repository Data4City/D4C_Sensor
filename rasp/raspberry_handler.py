import busio, board, asyncio, logging
from Helpers import plugged_sensor, requests_handler, microphone
from threading import Thread

__current_plugged_sensors = []
__serial_num = "0000000000000000"
__threads = {}
def get_serial(serial = __serial_num):
  # Extract serial from cpuinfo file
    if serial == "0000000000000000" or serial == "ERROR000000000":
        try:
            with open('/proc/cpuinfo','r') as f:
                for line in f:
                    if line[0:6]=='Serial':
                        serial = line[10:26]
        except:
            logger = logging.getLogger(__name__)
            logger.error("Serial number not found")
            serial = "ERROR000000000"
    return serial

  
def initialize_sensors(sensorList):
    i2c = busio.I2C(board.SCL, board.SDA)
    logger = logging.getLogger(__name__)
    for sensor in sensorList["sensors"]:
            global __current_plugged_sensors
            try:
                if(sensor["type"] == "i2c"):
                    __current_plugged_sensors.append(plugged_sensor.PluggedSensor(sensor, i2c))
                    logger.info("{} sensor initialized".format(sensor["model"]))
                if(sensor["type"] == "mic"):
                    mic = microphone.MicrophoneSensor(sensor)
                    __threads["microphone"] = Thread(target=mic.start_sensing)
            except RuntimeError:
                logger.error("{} sensor not found, ignoring".format(sensor["model"]))

def start_sense_loop():
    sensor_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(sensor_loop)
    asyncio.ensure_future(sense())
    sensor_loop.run_forever()

async def sense():
    while True:
        for sensor in __current_plugged_sensors:
            if sensor.update_sensors():
                if sensor.type == "i2c":
                    for i,data in enumerate(sensor.sensor_data):
                        if not data.enqueued:
                            requests_handler.post_sensor.delay(sensor.__post_data__(i))
                            data.enqueued = True
        await asyncio.sleep(10)


def init_rasp(sensor_list):
    get_serial(__serial_num)
    initialize_sensors(sensor_list)
    __threads["sense"] = Thread(target=start_sense_loop)
    #TODO check this
    for key,value in __threads.items():
        value.start()