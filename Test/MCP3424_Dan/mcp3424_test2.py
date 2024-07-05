from mcp3424_lib import MCP3424
import smbus
import time
import os

"""
This demo is inspired by
https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/

Initialise the ADC device using the default addresses and sample rate, 
change this value if you have changed the address selection jumpers.
Sample rate can be 12, 14, 16 or 18 bit.
"""

# Inicializace I2C sběrnice
bus = smbus.SMBus(1)

# Inicializace MCP3424 ADC s adresou 0x6A a rozlišením 18 bitů
adc = MCP3424(bus, address=0x6A, rate=18)
adc.set_pga(1)  # Nastavení PGA na 1

while True:
    # Vymazání konzole
    os.system('clear')

    # Čtení napětí z kanálu 1 a výpis na obrazovku
    voltage = adc.read_voltage(1)
    print(f"Channel 1: {voltage * 1000 / 2.047} mV")

    # Čekání 0.5 sekundy před dalším čtením
    time.sleep(0.5)
