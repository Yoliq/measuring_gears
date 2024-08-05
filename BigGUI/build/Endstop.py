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
        GPIO.add_event_detect(self.pin, self.pressed_state, callback=self.pressed_action, bouncetime=300)

    
    def pressed_action(self):
        # stop motor
        self.motor_to_stop.stop_motor()
        # couvni s motorem
        print("End stop reached!")
        self.motor_to_stop.stop_motor()
        time.sleep(0.5)
        cuknuti = self.motor_to_stop.steps / 360 *self.motor_to_stop.prevodovy_pomer * self.motor_to_stop.endstop_velikost_cuknuti
        GPIO.output(self.motor_to_stop.dir_pin, GPIO.HIGH)
        for _ in range(int(cuknuti)):
            GPIO.output(self.motor_to_stop.step_pin, GPIO.HIGH)
            time.sleep(self.motor_to_stop.speed)
            GPIO.output(self.motor_to_stop.step_pin, GPIO.LOW)
            time.sleep(self.motor_to_stop.speed)
        self.motor_to_stop.motor_running = False
            # TODO vynulovat hodnoty pro natoceni paky
