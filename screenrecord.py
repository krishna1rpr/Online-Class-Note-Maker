import cv2
import numpy as np
import time
import pyautogui
import threading

from utils import get_curr_time

screenWidth, screenHeight = pyautogui.size()
screen_size = (screenWidth, screenHeight)


class ScreenRecorder:
    def __init__(self, output_file_name="screen_recording_" + str(get_curr_time()), frame_rate=2.0, screen_size=(screenWidth, screenHeight), recording_region=None):
        self.output_file_name = output_file_name + ".mp4"
        self.frame_rate = frame_rate
        self.screen_size = screen_size
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = None
        self.is_recording = False
        self.recording_region = recording_region

    def start_recording(self):
        self.out = cv2.VideoWriter(
            self.output_file_name, self.fourcc, self.frame_rate, self.screen_size if self.recording_region is None else (self.recording_region[2], self.recording_region[3]))
        self.is_recording = True
        while self.is_recording:
            # images = pyautogui.screenshot()
            if self.recording_region is None:
                images = pyautogui.screenshot()
            else:
                images = pyautogui.screenshot(region=self.recording_region)
            frames = np.array(images)
            frames_RGB = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

            self.out.write(frames_RGB)

    def stop_recording(self):
        self.is_recording = False
        self.out.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    rec = ScreenRecorder()
    record_thread = threading.Thread(target=rec.start_recording)
    record_thread.start()

    # Do other tasks here...
    time.sleep(5)

    # Call the stop_recording method when you're ready to stop recording
    rec.stop_recording()
    exit()
