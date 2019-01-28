import busio, board, asyncio
from Helpers import plugged_sensor, requests_handler
from threading import Thread

__current_plugged_sensors = []
__serial_num = None

def get_serial():
  # Extract serial from cpuinfo file
    if not __serial_num or __serial_num == "ERROR000000000":
        __serial_num = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
                for line in f:
                    if line[0:6]=='Serial':
                        __serial_num = line[10:26]
                f.close()
        except:
            logger = logging.getLogger(__name__)
            logger.error("Serial number not found")
            __serial_num = "ERROR000000000"
        return __serial_num

  
def initialize_sensors(sensorList):
    i2c = busio.I2C(board.SCL, board.SDA)
    for sensor in sensorList["sensors"]:
            global __current_plugged_sensors
            if(sensor["type"] == "i2c"):
                __current_plugged_sensors.append(plugged_sensor.PluggedSensor(sensor, i2c))

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
                            requests_handler.post_sensor.delay(sensor.__post_data__(i), get_serial())
                            data.enqueued = True
                elif sensor.type == "mic":
                    print("Microphone check")
        await asyncio.sleep(10)





def init_rasp(sensor_list):
    initialize_sensors(sensor_list)
    sense_thread = Thread(target=start_sense_loop)
    sense_thread.start()



