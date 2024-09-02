import sys
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

def spin_motor(step_pin: int,
                speed: int,
                steps: int,
                prevodovy_pomer: float,
                angle=float):
    
    steps_wanted = steps / 360 * prevodovy_pomer * angle
    steps_taken = 0

    while steps_taken <= steps_wanted:
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(1/speed)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(1/speed)
        steps_taken += 1

def setup(dir_pin: int, enable_pin: int, step_pin: int):
    GPIO.setmode(GPIO.BCM)
    
    # Setup DIR and EN pins
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.setup(dir_pin, GPIO.OUT)
    GPIO.setup(enable_pin, GPIO.OUT)
    if GPIO.input(dir_pin) == GPIO.LOW:
        GPIO.output(dir_pin, GPIO.HIGH) # set direction if needed
    if GPIO.input(enable_pin) == GPIO.HIGH:
        GPIO.output(enable_pin, GPIO.LOW)  # enable driver if needed

if __name__ == "__main__":
    # Ensure that the script is provided a name as an argument
    if len(sys.argv) > 7:
        dir_pin = int(sys.argv[1])
        enable_pin = int(sys.argv[2])
        step_pin = int(sys.argv[3])
        speed = int(sys.argv[4])
        steps = int(sys.argv[5])
        prevodovy_pomer = float(sys.argv[6])
        angle = float(sys.argv[7])

    else:
        raise ValueError(f"Not all arguments provided in subprocess call: {sys.argv}")
    
    print('motor setup start')
    setup(dir_pin, enable_pin, step_pin) # setup motor
    print('motor setup end')
    
    print(f"Motor is spinning")
    spin_motor(step_pin, speed, steps, prevodovy_pomer, angle) # spin motor
    print('Motor spinning finished')