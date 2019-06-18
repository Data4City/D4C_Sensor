""
import argparse
import tempfile
import queue
import sys

import numpy as np
import asyncio
from datetime import datetime
import sounddevice as sd


class MicrophoneSensor:
    def __init__(self, sensor=None):
        if sensor is None:
            sensor = {}

        sd.default.samplerate = self.fs = 44100
        sd.default.channels = 1
        self.mean = 0.
        self.samples = np.empty(0)
        self.recording = False
        self.record_start = None
        self.record_queue = queue.Queue()
        self.last_loud_noise = None
        self.max_clip_size = sensor.get("max_clip_size", 5)
        self.time_check = 0

    def start_recording(self):
        self.time_check = datetime.now()
        while True:
            if (datetime.now() - self.time_check).seconds >= self.max_clip_size * 2:
                self.analyze_recording(self.record())

    def record(self):
        return sd.rec(int(self.max_clip_size * self.fs), blocking=True)

    def analyze_recording(self, recording):
        pass


if __name__ == "__main__":
    mic = MicrophoneSensor()
    mic.start_recording()
