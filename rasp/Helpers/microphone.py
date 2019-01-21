import sounddevice as sd
import numpy as np
    
class MicrophoneSensor():

    def __init__(self, test_time: int = 10):
        self.test_time = test_time
        with sd.Stream(callback=self.print_sound):
            sd.sleep(test_time * 1000)
        
    def print_sound(self, indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        print("|" * int(volume_norm))


if __name__ == "__main__":
    mic = MicrophoneSensor()