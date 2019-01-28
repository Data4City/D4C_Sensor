import busio, board, asyncio
from Helpers import plugged_sensor, requests_handler
from threading import Thread


current_plugged_sensors = []

def initialize_sensors(sensorList):
    i2c = busio.I2C(board.SCL, board.SDA)
    for sensor in sensorList["sensors"]:
            global current_plugged_sensors
            if(sensor["type"] == "i2c"):
                current_plugged_sensors.append(plugged_sensor.PluggedSensor(sensor, i2c))

def start_sense_loop():
    sensor_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(sensor_loop)
    asyncio.ensure_future(sense())
    sensor_loop.run_forever()

async def sense():
    while True:
        for sensor in current_plugged_sensors:
            if sensor.update_sensors():
                if sensor.type == "i2c":
                    for i,data in enumerate(sensor.sensor_data):
                        if not data.enqueued:
                            requests_handler.post_sensor.delay(sensor.__post_data__(i))
                            data.enqueued = True
                elif sensor.type == "mic":
                    print("Microphone check")
        await asyncio.sleep(10)



def init_rasp(sensor_list):
    initialize_sensors(sensor_list)
    sense_thread = Thread(target=start_sense_loop)
    sense_thread.start()



