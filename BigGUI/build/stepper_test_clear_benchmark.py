import RPi.GPIO as GPIO
import time
from threading import Thread
from tkinter import Tk, Button

# GPIO Setup
GPIO.setmode(GPIO.BCM)
STEP_PIN = 17
DIR_PIN = 27
ENABLE_PIN = 22
speed = 1000
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

motor_running = False

def step_motor(direction):
    GPIO.output(DIR_PIN, direction)
    GPIO.output(ENABLE_PIN, GPIO.LOW)

    while motor_running:
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(1/speed)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(1/speed)
    GPIO.output(ENABLE_PIN, GPIO.HIGH)

def on_button_click_forward():
    global motor_running
    motor_running = True
    motor_thread = Thread(target=step_motor, args=(GPIO.HIGH,))
    motor_thread.start()

def on_button_release_forward():
    global motor_running
    motor_running = False
    GPIO.output(ENABLE_PIN, GPIO.HIGH)

def on_button_click_backward():
    global motor_running
    motor_running = True
    motor_thread = Thread(target=step_motor, args=(GPIO.LOW,))
    motor_thread.start()

def on_button_release_backward():
    global motor_running
    motor_running = False
    GPIO.output(ENABLE_PIN, GPIO.HIGH)

# GUI Setup
window = Tk()
window.geometry("300x200")

button_forward = Button(window, text="Forward", width=15, height=2)
button_forward.bind("<ButtonPress-1>", lambda event: on_button_click_forward())
button_forward.bind("<ButtonRelease-1>", lambda event: on_button_release_forward())
button_forward.pack(pady=20)

button_backward = Button(window, text="Backward", width=15, height=2)
button_backward.bind("<ButtonPress-1>", lambda event: on_button_click_backward())
button_backward.bind("<ButtonRelease-1>", lambda event: on_button_release_backward())
button_backward.pack(pady=20)

window.mainloop()

# Clean up GPIO
GPIO.cleanup()
