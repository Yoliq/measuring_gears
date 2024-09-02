import RPi.GPIO as GPIO
import time
import subprocess
GPIO.setwarnings(False)

# motor pyprocess test

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
        self._move_up_process = None
        self._move_down_process = None
        self._enable_pin_setup()
        
        

    def _enable_pin_setup(self):
        '''
        Initial GPIO setup - only ENABLE pin.
        DIR and STEP pins are handled in subprocess
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)  # Enable driver

    
    
    def move_up(self, angle=float('inf')):
        print(f"Pohyb motoru nahoru o {angle} stupnu")   
        '''
        angle in degrees
        call subprocess move_up_process.py
        '''
        # check that no subprocesses run
        if isinstance(self._move_up_process, subprocess.Popen):
            self._move_up_process.kill()
            self._move_up_process = None
        if isinstance(self._move_down_process, subprocess.Popen):
            self._move_down_process.kill()
            self._move_down_process = None

        # start move_up_subprocess.py
        if angle == float('inf'):
            self._move_up_process = subprocess.Popen(['python',
                                                    'move_up_subprocess.py',
                                                    str(self.dir_pin),
                                                    str(self.enable_pin),
                                                    str(self.step_pin),
                                                    str(self.speed),
                                                    str(self.steps),
                                                    str(self.prevodovy_pomer),
                                                    str(angle)])
        else:
            self._move_up_process = subprocess.Popen(['python',
                                                    'move_up_subprocess.py',
                                                    str(self.dir_pin),
                                                    str(self.enable_pin),
                                                    str(self.step_pin),
                                                    str(self.speed),
                                                    str(self.steps),
                                                    str(self.prevodovy_pomer),
                                                    str(angle)])
            

    def move_down(self, angle=float('inf')):
        '''
        angle in degrees
        call subprocess move_down_process.py
        '''
        pass
        # TODO once move_up works



    def stop_motor(self):
        GPIO.output(self.enable_pin, GPIO.HIGH)  # Disable driver
        
        # check that no subprocesses run
        if isinstance(self._move_up_process, subprocess.Popen):
            self._move_up_process.kill()
            self._move_up_process = None
        if isinstance(self._move_down_process, subprocess.Popen):
            self._move_down_process.kill()
            self._move_down_process = None
        

