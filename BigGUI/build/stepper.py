import RPi.GPIO as GPIO
import time
from threading import Thread
from tkinter import Tk, Button, Canvas, PhotoImage
from pathlib import Path
GPIO.setwarnings(False)
from datetime import datetime


class Stepper_motor:
    def __init__(self, step_pin, dir_pin, enable_pin, speed, steps, 
                 prevodovy_pomer, velikost_natoceni, endstop_velikost_cuknuti):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.speed = speed
        self.steps = steps
        self.prevodovy_pomer = prevodovy_pomer
        self.sekvence_velikost_natoceni = velikost_natoceni
        self.endstop_velikost_cuknuti = endstop_velikost_cuknuti
        self.motor_running = False
        self._GPIO_setup()
        
    def _GPIO_setup(self):
        '''
        Initial GPIO setup
        '''

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

        # Initial state
        GPIO.output(self.enable_pin, GPIO.HIGH)  # Disable driver at start

    def step_motor(self, direction, steps=None):
        '''
        Function to step motor
        '''

        GPIO.output(self.dir_pin, direction)
        GPIO.output(self.enable_pin, GPIO.LOW)  # Enable driver

        steps_taken = 0
        old_now = datetime.now()
        while self.motor_running and (steps is None or steps_taken<steps):
            # ENDSTOP PRESSED PART
            # if GPIO.input(self.end_stop_pin) == GPIO.LOW:  # Koncový spínač je stisknutý
            #     print("End stop reached!")
            #     self.stop_motor()
            #     time.sleep(0.5)
            #     cuknuti = self.steps / 360 *105.23*1.5 # otočení o 1,5 stupňů
            #     GPIO.output(self.dir_pin, GPIO.HIGH)
            #     for _ in range(int(cuknuti)):
            #         GPIO.output(self.step_pin, GPIO.HIGH)
            #         time.sleep(self.speed)
            #         GPIO.output(self.step_pin, GPIO.LOW)
            #         time.sleep(self.speed)
            #     self.motor_running = False
            #     # TODO vynulovat hodnoty pro natoceni paky
            #     break
            
            now = datetime.now()
            print(f"While loop {now-old_now}")
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.speed)
            print(f"GPIO LOW {datetime.now()-now}")
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(self.speed)
            steps_taken +=1
            print(f"Steps_taken:{steps_taken}")
            old_now = now

        GPIO.output(self.enable_pin, GPIO.HIGH)  # Disable driver when stopping

    def start_motor(self, direction):
        self.motor_running = True
        motor_thread = Thread(target=self.step_motor, args=(direction,))
        motor_thread.start()

    def stop_motor(self):
        self.motor_running = False
        
    def sekvence_up(self, sekvence_velikost_natoceni):
        steps = self.steps / 360 * self.prevodovy_pomer * sekvence_velikost_natoceni
        self.motor_running = True
        motor_thread = Thread(target=self.step_motor, args=(GPIO.HIGH, steps))
        motor_thread.start() # Start parallel thread
        # space for things to be done in between
        motor_thread.join()  # Wait for the rotation to complete
        self.motor_running = False 

    def sekvence_down(self, sekvence_velikost_natoceni):
        steps = self.steps / 360 * self.prevodovy_pomer * sekvence_velikost_natoceni
        self.motor_running = True
        motor_thread = Thread(target=self.step_motor, args=(GPIO.LOW, steps))
        motor_thread.start() # Start parallel thread
        # space for things to be done in between
        motor_thread.join()  # Wait for the rotation to complete
        self.motor_running = False

    '''
    TODO:
    PUT THESE AS PART OF BUTTON CLASSES
    '''
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