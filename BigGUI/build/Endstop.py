import RPi.GPIO as GPIO
import time
from threading import Thread


class Endstop:
    def __init__(self,
                pin,
                motor_to_stop,
                endstop_pressed_set_angle,
                serial_reader_hnaci_kolo,
                serial_reader_hnane_kolo,
                natoceni_paky,
                natoceni_kola,
                natoceni_paky_hlavni,
                pressed_state=GPIO.LOW):

        self.pin = pin
        self.motor_to_stop = motor_to_stop
        self.pressed_state = pressed_state
        self.serial_reader_hnaci_kolo = serial_reader_hnaci_kolo
        self.serial_reader_hnane_kolo = serial_reader_hnane_kolo
        self.natoceni_paky = natoceni_paky
        self.natoceni_kola = natoceni_kola
        self.natoceni_paky_hlavni = natoceni_paky_hlavni
        self.endstop_pressed_set_angle = endstop_pressed_set_angle
        self._GPIO_setup()

    def _GPIO_setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.pressed_action, bouncetime=1500)


    def pressed_action(self, channel):
        # stop motor
        self.motor_to_stop.stop_motor()
        print("End stop reached!")

        # couvni s motorem
        time.sleep(0.5)
        self.motor_to_stop.sekvence_up(self.motor_to_stop.endstop_velikost_cuknuti)
        time.sleep(0.1)

        # vynuluj pole a nastav je na hodnotu self.endstop_pressed_set_angle
        current_angle_paka = float(self.natoceni_paky.get())
        self.serial_reader_hnaci_kolo.zero_angle(current_angle_paka - self.endstop_pressed_set_angle)
        current_angle_kolo = float(self.natoceni_kola.get())
        self.serial_reader_hnane_kolo.zero_angle(current_angle_kolo + self.endstop_pressed_set_angle)
        
        # nastavení hodnoty hlavního natočení páky
        self.natoceni_paky_hlavni.set(self.endstop_pressed_set_angle)        
        #current_angle_paka_hlavni =  current_angle_paka #float(self.natoceni_paky.get())
        #self.serial_reader_hnaci_kolo.zero_angle(current_angle_paka_hlavni + self.endstop_pressed_set_angle)
        