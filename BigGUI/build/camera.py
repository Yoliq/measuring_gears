import cv2
import time

class Camera:
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.recording = False
        self.out = None
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        if self.fps == 0:
            self.fps = 10.0  # Default value if unable to get FPS from camera

        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"FPS kamery: {self.fps}")
        print(f"Šířka: {self.width}, Výška: {self.height}")

        self.start_time = None
        self.frame_counter = 0

    def start_recording(self, filename='output.mp4'):
        if not self.recording:
            self.recording = True
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))
            self.start_time = time.time()
            self.frame_counter = 0
            print("Recording started.")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.out.release()
            self.out = None
            print("Recording stopped.")

    def get_frame(self):
        ret, frame = self.vid.read()
        if ret:
            if self.recording:
                elapsed_time = time.time() - self.start_time
                expected_frames = int(elapsed_time * self.fps)
                while self.frame_counter < expected_frames:
                    self.out.write(frame)
                    self.frame_counter += 1
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

    def release(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.recording and self.out is not None:
            self.out.release()

    def __del__(self):
        self.release()
