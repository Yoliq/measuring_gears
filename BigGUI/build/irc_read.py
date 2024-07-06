import RPi.GPIO as GPIO
import time

# Pin definitions
ZeroPin = 2  # GPIO pin for Z channel (zero detection)
COSPin = 3   # GPIO pin for A channel (cos signal) 
SINPin = 4   # GPIO pin for B channel (sin signal)  

# variables
ENC_STOP = 0
ENC_CLOCKWISE_ROTATION = 1
ENC_COUNTERCLOCKWISE_ROTATION = 2

encoder_state = ENC_STOP
encoder_position = 0
encoder_oldpos = 0

def setup():
    global encoder_state, encoder_position, encoder_oldpos
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

    # Define pins for input and output
    GPIO.setup(SINPin, GPIO.IN)

    # set internal pull-up resistor for interrupt pin
    GPIO.setup(COSPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ZeroPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # set interrupt service routine to COSPin and 'RISING' edge 
    GPIO.add_event_detect(COSPin, GPIO.RISING, callback=encoder_isr)

    # set interrupt service routine to ZeroPin and 'HIGH' level 
    GPIO.add_event_detect(ZeroPin, GPIO.RISING, callback=zero_detection_isr)

def loop():
    global encoder_state, encoder_position, encoder_oldpos
    while True:
        # Detect Encoder Stop
        if encoder_oldpos == encoder_position:
            encoder_state = ENC_STOP

        # output encoder incremental and status
        print("Encoder position:", encoder_position, ", Encoder state:", end=" ")
        
        if encoder_state == ENC_CLOCKWISE_ROTATION:
            print("Clockwise Rotation")
        elif encoder_state == ENC_COUNTERCLOCKWISE_ROTATION:
            print("Counter-Clockwise Rotation")
        else:
            print("Stop")
        
        encoder_oldpos = encoder_position
        time.sleep(0.5)

def encoder_isr(channel):
    global encoder_state, encoder_position
    if GPIO.input(SINPin) == GPIO.LOW:
        # clockwise rotation
        encoder_state = ENC_CLOCKWISE_ROTATION
        encoder_position += 1
    else:
        # counter-clockwise rotation
        encoder_state = ENC_COUNTERCLOCKWISE_ROTATION
        encoder_position -= 1

def zero_detection_isr(channel):
    global encoder_position
    # detect pulse on zero channel
    encoder_position = 0

if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
