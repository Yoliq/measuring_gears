from smbus2 import SMBus

# Inicializace sběrnice I2C
bus = SMBus(1)

print("Scanning I2C bus...")

devices = []
for address in range(128):
    try:
        bus.read_byte(address)
        devices.append(hex(address))
    except:
        pass

if devices:
    print("I2C devices found at addresses:", ", ".join(devices))
else:
    print("No I2C devices found")

bus.close()
