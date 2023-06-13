import time
from audiorecord import AudioRecord
from screenrecord import ScreenRecorder
from postprocessing import Proj
from utils import get_curr_time, select_region_by_mouse
import tkinter as tk
import os
import threading

start_bg = "#16a34a"
start_active_bg = "#15803d"
stop_bg = "#b91c1c"
stop_active_bg = "#991b1b"
font_color = "#eeeeee"


current_name = str(get_curr_time())

# os.makedirs(current_name)

audio_rec = AudioRecord(output_file_name=current_name)
screen_rec = ScreenRecorder(output_file_name=current_name, frame_rate=28)


class OnlineNotesMaker:
    def __init__(self, title="Online Notes Maker", alpha=0.25, min_size=(400, 200), margin=10):
        self.root = tk.Tk()
        self.root.title(title)
        # self.root.attributes('-alpha', alpha)
        self.root.minsize(*min_size)

        self.margin = margin
        self.start_bg = start_bg
        self.start_active_bg = start_active_bg
        self.stop_bg = stop_bg
        self.stop_active_bg = stop_active_bg
        self.font_color = font_color

        self.start_button = tk.Button(self.root, text="Start", command=self.start_overlay, bg=self.start_bg,
                                      activebackground=self.start_active_bg, fg=self.font_color, activeforeground=self.font_color)
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_overlay, bg=self.stop_bg,
                                     activebackground=self.stop_active_bg, fg=self.font_color, activeforeground=self.font_color)

        self.start_button.grid(
            row=0, column=0, sticky="nsew", padx=self.margin, pady=self.margin)
        self.stop_button.grid(row=1, column=0, sticky="nsew",
                              padx=self.margin, pady=self.margin)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def start_overlay(self):
        print("Starting overlay...")
        screen_rec.recording_region = select_region_by_mouse()
        print("started recording")
        self.audio_rec_thread = threading.Thread(target=audio_rec.start_audio)
        self.audio_rec_thread.start()
        self.screen_rec_thread = threading.Thread(
            target=screen_rec.start_recording)
        self.screen_rec_thread.start()

    def stop_overlay(self):
        print("Stopping overlay...")
        audio_rec.stop_audio()
        self.audio_rec_thread.join()
        screen_rec.stop_recording()
        time.sleep(2)
        proj = Proj(f"./{current_name}.mp4", "./frames/", "./diff/",
                    f"./{current_name}.wav", "./video.mp4", F"./{current_name}.pptx")
        proj.generate_frames()
        proj.generate_slides()
        proj.generate_ppt()
        self.root.quit()

    def start_mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    notes_maker = OnlineNotesMaker()
    # mainloop_thread = threading.Thread(target=notes_maker.start_mainloop)
    # mainloop_thread.start()
    notes_maker.start_mainloop()
    exit()
