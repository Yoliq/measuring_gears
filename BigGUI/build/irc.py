import RPi.GPIO as GPIO
import time

class IRC:
    def __init__(self, cos_pin, sin_pin, zero_pin):
        self.cos_pin = cos_pin
        self.sin_pin = sin_pin
        self.zero_pin = zero_pin
        
        self.ENC_STOP = 0
        self.ENC_CLOCKWISE_ROTATION = 1
        self.ENC_COUNTERCLOCKWISE_ROTATION = 2
        
        self.encoder_state = self.ENC_STOP
        self.encoder_position = 0
        self.encoder_oldpos = 0

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

        # Define pins for input and output
        GPIO.setup(self.sin_pin, GPIO.IN)

        # Set internal pull-up resistor for interrupt pin
        GPIO.setup(self.cos_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.zero_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Set interrupt service routine to COSPin and 'RISING' edge 
        GPIO.add_event_detect(self.cos_pin, GPIO.RISING, callback=self.encoder_isr)

        # Set interrupt service routine to ZeroPin and 'RISING' edge 
        GPIO.add_event_detect(self.zero_pin, GPIO.RISING, callback=self.zero_detection_isr)

    def get_reading(self):
        # Detect Encoder Stop
        if self.encoder_oldpos == self.encoder_position:
            self.encoder_state = self.ENC_STOP
        else:
            self.encoder_state = self.ENC_CLOCKWISE_ROTATION if (self.encoder_position > self.encoder_oldpos) else self.ENC_COUNTERCLOCKWISE_ROTATION
        
        # Save the current position before returning
        self.encoder_oldpos = self.encoder_position
        return self.encoder_position, self.encoder_state

    def encoder_isr(self, channel):
        if GPIO.input(self.sin_pin) == GPIO.LOW:
            # Clockwise rotation
            self.encoder_position += 1
        else:
            # Counter-clockwise rotation
            self.encoder_position -= 1

    def zero_detection_isr(self, channel):
        # Detect pulse on zero channel
        self.encoder_position = 0

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        encoder = IRC(cos_pin=5, sin_pin=6, zero_pin=13)
        while True:
            position, state = encoder.get_reading()
            print(f"Encoder position: {position}, Encoder state: {state}")
            time.sleep(3)
    except KeyboardInterrupt:
        encoder.cleanup()
