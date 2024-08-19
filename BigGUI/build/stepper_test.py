import RPi.GPIO as GPIO
import asyncio
from tkinter import Tk, Button
from datetime import datetime
# GPIO Setup
STEP_PIN = 17
DIR_PIN = 27
ENABLE_PIN = 22
speed = 1000
motor_running = False

async def step_motor(direction):
    GPIO.output(DIR_PIN, direction)
    GPIO.output(ENABLE_PIN, GPIO.LOW)
    old_now = datetime.now()
    steps_taken = 0
    while motor_running:
        now = datetime.now()
        print(f"While loop {now - old_now}")
        GPIO.output(STEP_PIN, GPIO.HIGH)
        await asyncio.sleep(1 / speed)
        print(f"GPIO LOW {datetime.now()-now}")
        GPIO.output(STEP_PIN, GPIO.LOW)
        await asyncio.sleep(1 / speed)
        steps_taken += 1
        print(f"Steps_taken: {steps_taken}")
        old_now = now

    GPIO.output(ENABLE_PIN, GPIO.HIGH)

async def on_button_click_forward():
    global motor_running
    motor_running = True
    await step_motor(GPIO.HIGH)

async def on_button_release_forward():
    global motor_running
    motor_running = False
    GPIO.output(ENABLE_PIN, GPIO.HIGH)

async def on_button_click_backward():
    global motor_running
    motor_running = True
    await step_motor(GPIO.LOW)

async def on_button_release_backward():
    global motor_running
    motor_running = False
    GPIO.output(ENABLE_PIN, GPIO.HIGH)

def setup_tkinter(window):
    button_forward = Button(window, text="Forward", width=15, height=2)
    button_forward.bind("<ButtonPress-1>", lambda event: asyncio.create_task(on_button_click_forward()))
    button_forward.bind("<ButtonRelease-1>", lambda event: asyncio.create_task(on_button_release_forward()))
    button_forward.pack(pady=20)

    button_backward = Button(window, text="Backward", width=15, height=2)
    button_backward.bind("<ButtonPress-1>", lambda event: asyncio.create_task(on_button_click_backward()))
    button_backward.bind("<ButtonRelease-1>", lambda event: asyncio.create_task(on_button_release_backward()))
    button_backward.pack(pady=20)

async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(ENABLE_PIN, GPIO.OUT)

    window = Tk()
    window.geometry("300x200")
    setup_tkinter(window)

    while True:
        window.update()
        await asyncio.sleep(0.01)

    GPIO.cleanup()

asyncio.run(main())
