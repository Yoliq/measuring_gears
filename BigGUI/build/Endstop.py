import RPi.GPIO as GPIO
import time
from threading import Thread

class Endstop:
    def __init__(self, pin, motor_to_stop, pressed_state=GPIO.LOW):
        self.pin = pin
        self.motor_to_stop = motor_to_stop
        self.pressed_state = pressed_state
        self._GPIO_setup()

    def _GPIO_setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.pressed_action, bouncetime=1000)


    def pressed_action(self, channel):
        # stop motor
        self.motor_to_stop.stop_motor()
        # couvni s motorem
        print("End stop reached!")
        time.sleep(0.5)
        
    
        self.motor_to_stop.sekvence_up(self.motor_to_stop.endstop_velikost_cuknuti)
            # TODO vynulovat hodnoty pro natoceni paky