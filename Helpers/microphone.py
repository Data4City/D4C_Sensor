import sounddevice as sd
import numpy as np
import asyncio, queue
import time as t
from datetime import datetime


class MicrophoneSensor:
    def __init__(self, sensor=None):
        if sensor is None:
            sensor = {}

        sd.default.samplerate = 44100
        self.mean = 0.
        self.samples = np.empty(0)
        self.recording = False
        self.record_start = None
        self.record_queue = queue.Queue()
        self.last_loud_noise = None
        self.max_time_between_noises = sensor.get("max_time_between_noises", 3)
        self.max_clip_size = sensor.get("max_clip_size", 4)
        self.min_clip_size = sensor.get("min_clip_size", 3)
    #TODO Implement this
    def post_to_api(self):
        pass
    def start_sensing(self, window: int = 1500):
        loop = asyncio.get_event_loop()
        with sd.InputStream(callback=self.callback):
            while (True):
                # sd.sleep(10)
                if (len(self.samples) >= window):
                    print("updating mean")
                    self.mean = loop.run_until_complete(self.running_mean(self.samples, window))
                    self.samples = np.empty(0)
            # asyncio.ensure_future(self.calculate_average(), vol_values)

    async def running_mean(self, x, N) -> np.ndarray:
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return np.mean((cumsum[N:] - cumsum[:-N]) / float(N))

    def get_label(self, audio_queue):
        # TODO Add label creator
        return "ay lemao wat"

    def process_signal(self, audio_queue):
        print(self.__post_data__())
        # rh.post_sensor.delay(self.__post_data__(self.get_label(audio_queue)))

    def time_passed(self, end: float = None, start: float = None):
        start_check = self.record_start if start is None else start  # Can't use self in parameters
        end_check = t.time() if end is None else end
        if not self.recording:
            return 0
        else:
            return round(end_check - start_check, 2)

    def is_loud(self, volume) -> bool:
        return volume > self.mean * 3  # TODO Figure something smarter than this

    def callback(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        self.samples = np.append(self.samples, volume_norm)
        if self.mean != 0:
            if not self.recording and self.is_loud(volume_norm):
                print("Started recording")
                self.recording = True
                self.record_start = t.time()

            if self.recording:
                self.record_queue.put(indata.copy())
                if self.time_passed() > self.min_clip_size:  # Make sure the clip is at least n seconds long
                    if (self.time_passed(start=self.last_loud_noise) > self.max_time_between_noises) or (
                            self.time_passed < self.max_clip_size):
                        print("Stopped recording")
                        self.process_signal(queue)
                        self.recording = False

                if self.is_loud(volume_norm):
                    self.last_loud_noise = t.time()

            # print("|" * int(volume_norm))

    def __post_data__(self, label: str = "No category"):
        return {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": "mic",
            "duration": self.time_passed(),
            "label": label
        }


if __name__ == "__main__":
    mic = MicrophoneSensor()
    mic.start_sensing()
