import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window, video_source=0, fps=30, x=0, y=0, scale=1.0):
        self.window = window
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        
        # Set FPS (in milliseconds between frames)
        self.delay = int(1000 / fps)
        
        # Set the position (X, Y) and scale factor for the video
        self.x = x
        self.y = y
        self.scale = scale
        
        # Get original dimensions
        self.orig_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.orig_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Scale the dimensions
        self.width = int(self.orig_width * self.scale)
        self.height = int(self.orig_height * self.scale)

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.place(x=self.x, y=self.y)  # Place the canvas at the (X, Y) location
        
        # Start displaying video
        self.update()

    def update(self):
        # Get the current frame from the video feed
        ret, frame = self.vid.read()
        if ret:
            # Resize the frame according to the scale factor
            frame = cv2.resize(frame, (self.width, self.height))
            
            # Convert the frame to RGB format for Tkinter compatibility
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            
            # Display the image on the canvas at (X, Y)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Schedule the next frame update
        self.window.after(self.delay, self.update)

    def __del__(self):
        # Release the video source when the object is destroyed
        if self.vid.isOpened():
            self.vid.release()
