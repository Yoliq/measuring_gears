import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import threading
import time

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, height=1, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.btn_record = tk.Button(window, text="Start Recording", width=50, height=2, command=self.toggle_recording)
        self.btn_record.pack(anchor=tk.CENTER, expand=True)

        self.recording = False
        self.out = None
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        if self.fps == 0:
            self.fps = 29  # Default value if unable to get FPS from camera

        print(f"FPS kamery: {self.fps}")

        self.delay = int(1000 / self.fps)
        self.start_time = None
        self.frame_counter = 0

        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("frame-" + str(time.time()) + ".jpg", frame)

    def toggle_recording(self):
        if self.recording:
            self.recording = False
            self.btn_record.config(text="Start Recording")
            self.out.release()
        else:
            self.recording = True
            self.btn_record.config(text="Stop Recording")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter('output.mp4', fourcc, self.fps, (int(self.vid.get(3)), int(self.vid.get(4))))
            self.start_time = time.time()
            self.frame_counter = 0

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            if self.recording:
                elapsed_time = time.time() - self.start_time
                expected_frames = int(elapsed_time * self.fps)
                while self.frame_counter < expected_frames:
                    self.out.write(frame)
                    self.frame_counter += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.recording and self.out is not None:
            self.out.release()
        self.window.destroy()

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.recording and self.out is not None:
            self.out.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Camera App")
