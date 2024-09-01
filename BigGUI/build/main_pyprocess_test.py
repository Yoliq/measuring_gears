import subprocess
import sys
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

def run_motor_process():
    # Running hello.py in a separate process and passing the name as an argument
    process = subprocess.Popen(['python', 'stepper_pyprocess.py'])
    return process

if __name__ == "__main__":
    # Stepper motor
    STEP_PIN_BIG_MOTOR = 17
    DIR_PIN_BIG_MOTOR = 27

    # Enable pin
    ENABLE_PIN_BIG_MOTOR = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENABLE_PIN_BIG_MOTOR, GPIO.OUT)
    GPIO.output(ENABLE_PIN_BIG_MOTOR, GPIO.LOW)
        # Setup DIR and EN pins
    GPIO.setup(DIR_PIN_BIG_MOTOR, GPIO.OUT)
    GPIO.setup(STEP_PIN_BIG_MOTOR, GPIO.OUT)

    while True:
        ready = input("Are you ready? Motor wil start moving. Input Y/N:")
        if ready == 'y':
            motor_process = run_motor_process()
            break
        
    while True:
        end = input("Ready to kill process? Y/N:")
        if end == 'y':
            motor_process.kill()
            print("Process killed")
            break
