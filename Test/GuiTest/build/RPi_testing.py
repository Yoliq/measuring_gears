import RPi.GPIO as GPIO
import time
from threading import Thread
from tkinter import Tk, Button, Canvas, PhotoImage
from pathlib import Path

# GPIO pin numbers
STEP_PIN = 17
DIR_PIN = 27
ENABLE_PIN = 7
SPEED = 0.0005  # Sleep time between steps, adjust for speed

# Initial setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# Initial state
GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable driver at start

# State variables
motor_running = False

def step_motor(direction):
    global motor_running
    GPIO.output(DIR_PIN, direction)
    GPIO.output(ENABLE_PIN, GPIO.LOW)  # Enable driver

    while motor_running:
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(SPEED)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(SPEED)

    GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Disable driver when stopping

def start_motor(direction):
    global motor_running
    motor_running = True
    motor_thread = Thread(target=step_motor, args=(direction,))
    motor_thread.start()

def stop_motor():
    global motor_running
    motor_running = False

def on_button_press_forward(event):
    print("button_1 pressed")
    start_motor(GPIO.HIGH)

def on_button_release_forward(event):
    print("button_1 released")
    stop_motor()

def on_button_press_backward(event):
    print("button_2 pressed")
    start_motor(GPIO.LOW)

def on_button_release_backward(event):
    print("button_2 released")
    stop_motor()

# Tkinter GUI setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    window.state = not window.state  # Just toggling the boolean
    window.attributes("-fullscreen", window.state)
    return "break"

# Function to end fullscreen mode
def end_fullscreen(event=None):
    window.state = False
    window.attributes("-fullscreen", False)
    return "break"

window.bind("<F11>", toggle_fullscreen)
window.bind("<Escape>", end_fullscreen)

# Initially start in fullscreen mode
window.state = True
window.attributes("-fullscreen", True)

canvas = Canvas(
    window,
    bg="#ADD8E6",  # Set pastel blue background
    height=window.winfo_screenheight(),
    width=window.winfo_screenwidth(),
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.pack(fill="both", expand=True)

# Simple flat button 1
button_1 = Button(
    window,
    text="+",
    font=("Arial", 24),
    bg="#98FB98",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_1.place(
    x=window.winfo_screenwidth() * 0.2,
    y=window.winfo_screenheight() * 0.7,
    width=121,
    height=133
)
button_1.bind('<ButtonPress-1>', on_button_press_forward)
button_1.bind('<ButtonRelease-1>', on_button_release_forward)

# Simple flat button 2
button_2 = Button(
    window,
    text="−",
    font=("Arial", 24),
    bg="#e06666",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_2.place(
    x=window.winfo_screenwidth() * 0.6,
    y=window.winfo_screenheight() * 0.7,
    width=121,
    height=133
)
button_2.bind('<ButtonPress-1>', on_button_press_backward)
button_2.bind('<ButtonRelease-1>', on_button_release_backward)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(window.winfo_screenwidth() / 2, window.winfo_screenheight() * 0.3, image=image_image_2)

window.mainloop()

# Cleanup GPIO
GPIO.cleanup()
