'''
Knihovna pro rotaci motoru.

Definuje funkci spin_motor(step_pin, dir, speed)

Po spusteni funkce se motor zacne tocit v zadanem smeru dle dir. Motor se ve funkci nezastavi.

Motor musi byt zastaven externe prerusenim skriptu.

Tento skript nesmi pracovat s ENABLE PINEM motoru. ENABLE PIN predpokladam po celou dobu spusteni HIGH.

Je to jako podminka spusteni skriptu.

Skript vrati cislo procesu.
'''

if __name__ == "__main__":
    import RPi.GPIO as GPIO
    import time
    GPIO.setwarnings(False)
    def spin_motor(step_pin: int, dir: str, speed: int):
        while True:
            GPIO.output(step_pin, GPIO.HIGH)
            time.sleep(1/speed)
            GPIO.output(step_pin, GPIO.LOW)
            time.sleep(1/speed)
    
    GPIO.setmode(GPIO.BCM)
    # Setup DIR and EN pins
    GPIO.setup(17, GPIO.OUT)
    SPEED_BIG_MOTOR = 1000
  
    
    print(f"Motor is spinning")
    spin_motor(17, 27, SPEED_BIG_MOTOR)
    print(f"Motor stopped")