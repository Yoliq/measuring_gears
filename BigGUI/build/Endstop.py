import RPi.GPIO as GPIO
import time
from threading import Thread


class Endstop:
    def __init__(self,
                pin,
                motor_to_stop,
                endstop_pressed_set_angle,
                pressed_state=GPIO.LOW):
        self.pin = pin
        self.motor_to_stop = motor_to_stop
        self.pressed_state = pressed_state
        #self.serial_reader_hnaci_kolo = serial_reader_hnaci_kolo
        #self.serial_reader_hnane_kolo = serial_reader_hnane_kolo
        self.endstop_pressed_set_angle = endstop_pressed_set_angle
        self._GPIO_setup()

    def _GPIO_setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.pressed_action, bouncetime=1000)


    def pressed_action(self, channel):
        # stop motor
        self.motor_to_stop.stop_motor()
        print("End stop reached!")

        # couvni s motorem
        time.sleep(0.5)
        self.motor_to_stop.sekvence_up(self.motor_to_stop.endstop_velikost_cuknuti)

        # vynuluj pole a nastav je na hodnotu self.endstop_pressed_set_angle
        current_angle_paka = float(natoceni_paky.get())
        serial_reader_hnaci_kolo.zero_angle(current_angle_paka - self.endstop_pressed_set_angle)
        current_angle_kolo = float(natoceni_kola.get())
        serial_reader_hnane_kolo.zero_angle(current_angle_kolo - self.endstop_pressed_set_angle)