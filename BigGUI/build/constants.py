
from pathlib import Path

# Output path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

# Serial communication
SERIAL_BAUDRATE = 115200
USB_IRC_HNANE_KOLO = '/dev/ttyUSB0'
USB_IRC_HNACI_KOLO = '/dev/ttyUSB1'

# Stepper motor
STEP_PIN_BIG_MOTOR = 17
DIR_PIN_BIG_MOTOR = 27
ENABLE_PIN_BIG_MOTOR = 22
SPEED_BIG_MOTOR = 500
STEPS_BIG_MOTOR = 400
PREVODOVY_POMER_BIG_MOTOR = 105.23

STEP_PIN_SMALL_MOTOR = 16
DIR_PIN_SMALL_MOTOR = 20
ENABLE_PIN_SMALL_MOTOR = 21
SPEED_SMALL_MOTOR = 1000
STEPS_SMALL_MOTOR = 400
PREVODOVY_POMER_SMALL_MOTOR = 105.23

SEKVENCE_VELIKOST_NATOCENI = 45 # degree
ENDSTOP_VELIKOST_CUKNUTI = 1.5 # degree

# IRC
'''
Handled by MCUs (ESP32). Values are sent over USB line.
'''

# Endstop switch
ENDSTOP_PIN = 12
ENDSTOP_OFFSET = 25.18 # degree

# Lankovy snimac vzdalenosti
LANKOVY_SNIMAC_KOREKCE = 0
USB_ARDUINO_LENGTH = '/dev/ttyACM0'
SERIAL_BAUDRATE_ARD = 115200

# Laserovy snimac vzdalenosti
'''
Info z Arduina o snímači: 
Adafruit VL53L1X sensor demo
VL53L1X sensor OK!
Sensor ID: 0xEACC
Ranging started
Timing budget (ms): 50
'''
LASEROVY_SNIMAC_KOREKCE = 0
