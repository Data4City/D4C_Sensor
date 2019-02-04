import sounddevice as sd
import numpy as np
import asyncio    
class MicrophoneSensor():

    def __init__(self, window: int = 1500):
        sd.default.samplerate = 44100
        self.samples = np.empty(0)
        self.window = window
        self.mean = 0.

        loop = asyncio.get_event_loop()
        with sd.InputStream(callback=self.callback):

            while(True):
                sd.sleep(10)
                if(len(self.samples) >= self.window):
                    self.mean = loop.run_until_complete(self.running_mean(self.samples, window))
                    self.samples = np.empty(0)
            #asyncio.ensure_future(self.calculate_average(), vol_values)
    


    async def running_mean(self,x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0)) 
        return np.mean((cumsum[N:] - cumsum[:-N]) / float(N))
    
    def callback(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        self.samples = np.append(self.samples,volume_norm)

        #print("|" * int(volume_norm))


if __name__ == "__main__":
    mic = MicrophoneSensor()
    self.window = window