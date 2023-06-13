import time
import soundcard as sc
import soundfile as sf
import numpy as np
import threading
from utils import get_curr_time


class AudioRecord:
    def __init__(self, output_file_name="audio_recording_"+str(get_curr_time()), sample_rate=48000):
        self.OUTPUT_FILE_NAME = output_file_name+".wav"
        self.SAMPLE_RATE = sample_rate
        self.TOTAL_DATA = None
        self.IS_RECORDING = True

    def start_audio(self):
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.SAMPLE_RATE) as mic:
            while self.IS_RECORDING:
                data = mic.record(numframes=self.SAMPLE_RATE)
                if self.TOTAL_DATA is None:
                    self.TOTAL_DATA = data
                else:
                    self.TOTAL_DATA = np.concatenate((self.TOTAL_DATA, data))

    def stop_audio(self):
        self.IS_RECORDING = False
        sf.write(file=self.OUTPUT_FILE_NAME,
                 data=self.TOTAL_DATA[:, 0], samplerate=self.SAMPLE_RATE)


if __name__ == '__main__':
    rec = AudioRecord()
    rec_thread = threading.Thread(target=rec.start_audio)
    rec_thread.start()
    time.sleep(8)
    rec.stop_audio()
    rec_thread.join()
    exit()
