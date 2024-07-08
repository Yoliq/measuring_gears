'''
All the user defined variables which serve as constants and are used by the project.
Using BCM PIN numbering (see https://toptechboy.com/wp-content/uploads/2022/04/pinout-corrected.jpg)

'''

# TODO I2C communication
I2C_SDA = 2
I2C_SCL = 3

# Big stepper motor to turn gearbox
BIG_MOTOR = {
    'STEP_PIN' : 17,
    'DIR_PIN' : 27,
    'ENABLE_PIN' : 22,
    'SPEED' : 0.001
}

# Small stepper motor for linear movement
SMALL_MOTOR = {
    'STEP_PIN' : 16,
    'DIR_PIN' : 20,
    'ENABLE_PIN' : 21, 
    'SPEED' : 0.001
}

# IRC at big stepper
IRC_BIG_STEPPER = {
    'COS_PIN' : 5,
    'SIN_PIN' : 6,
    'ZERO_PIN' : 13
}

# IRC at Lever part 
IRC_LEVER_PART = {
    'COS_PIN' : 14, # Must be set to GPIO
    'SIN_PIN' : 15, # Must be set to GPIO
    'ZERO_PIN' : 18
}

# Endstop for lever
ENDSTOP_LEVER = 12

# Lidar - communicates via I2C
LIDAR_I2C_ADDRESS = 0x52

# TODO Distance wire sensor via I2C
DISTANCE_WIRE_SENSOR_I2C_ADDRESS = 0

# TODO Camera information

