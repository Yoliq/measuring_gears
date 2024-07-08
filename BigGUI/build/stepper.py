import RPi.GPIO as GPIO
import time
from threading import Thread
from tkinter import Tk, Button, Canvas, PhotoImage
from pathlib import Path
GPIO.setwarnings(False)



class Stepper_motor:
    def __init__(self, STEP_PIN, DIR_PIN, ENABLE_PIN, SPEED, STEPS, END_STOP_PIN):
        self.step_pin = STEP_PIN
        self.dir_pin = DIR_PIN
        self.enable_pin = ENABLE_PIN
        self.speed = SPEED
        self.steps = STEPS
        self.end_stop_pin = END_STOP_PIN
        self.motor_running = False
        self._GPIO_setup()
        
    def _GPIO_setup(self):
        # Initial setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.end_stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Initial state
        GPIO.output(self.enable_pin, GPIO.HIGH)  # Disable driver at start
        
    def step_motor(self, direction, steps=None):
        GPIO.output(self.dir_pin, direction)
        GPIO.output(self.enable_pin, GPIO.LOW)  # Enable driver
        steps_taken = 0

        while self.motor_running and (steps is None or steps_taken<steps):
            if GPIO.input(self.end_stop_pin) == GPIO.LOW:  # Koncový spínač je stisknutý
                print("End stop reached!")
                self.stop_motor()
                break
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.speed)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(self.speed)
            steps_taken +=1

        GPIO.output(self.enable_pin, GPIO.HIGH)  # Disable driver when stopping

    def start_motor(self, direction):
        self.motor_running = True
        motor_thread = Thread(target=self.step_motor, args=(direction,))
        motor_thread.start()

    def stop_motor(self):
        self.motor_running = False
        
    def sekvence_up(self, event):
        steps = self.steps / 360 * 360  # otočení o 90 stupňů
        self.motor_running = True
        motor_thread = Thread(target=self.step_motor, args=(GPIO.HIGH, steps))
        motor_thread.start()
        motor_thread.join()  # Wait for the rotation to complete
        self.motor_running = False 

    def sekvence_down(self):
        steps = self.steps / 360 * 90  # otočení o 90 stupňů
        self.motor_running = True
        motor_thread = Thread(target=self.step_motor, args=(GPIO.LOW, steps))
        motor_thread.start()
        motor_thread.join()  # Wait for the rotation to complete
        self.motor_running = False
    
    def on_button_press_forward(self, event):
        #print("button_1 pressed")
        self.start_motor(GPIO.HIGH)

    def on_button_release_forward(self, event):
        #print("button_1 released")
        self.stop_motor()

    def on_button_press_backward(self, event):
        #print("button_2 pressed")
        self.start_motor(GPIO.LOW)

    def on_button_release_backward(self, event):
        #print("button_2 released")
        self.stop_motor()


#button_1.bind('<ButtonPress-1>', main_motor.on_button_press_forward)
#button_1.bind('<ButtonRelease-1>', main_motor.on_button_release_forward)