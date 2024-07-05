import smbus
import time

# I2C adresa MCP3424
address = 0x6A

# Inicializace sběrnice I2C
bus = smbus.SMBus(1)

# Funkce pro čtení konfigurace z MCP3424
def read_config(bus, address):
    try:
        config = bus.read_byte(address)
        return config
    except Exception as e:
        print(f"Failed to read configuration: {e}")
        return None

# Funkce pro zápis konfigurace do MCP3424
def write_config(bus, address, config):
    try:
        bus.write_byte(address, config)
        print(f"Successfully wrote configuration: {config:02X}")
    except Exception as e:
        print(f"Failed to write configuration: {e}")

# Funkce pro čtení dat z MCP3424
def read_adc(bus, address):
    try:
        data = bus.read_i2c_block_data(address, 0x00, 3)  # Přečte 3 byte (24-bit ADC)
        raw_adc = (data[0] << 16) | (data[1] << 8) | data[2]
        if raw_adc & 0x800000:  # Pokud je hodnota negativní
            raw_adc -= 1 << 24
        return raw_adc
    except Exception as e:
        print(f"Failed to read from device: {e}")
        return None

# Nastavení konfigurace (Continuous Conversion Mode, Channel 1, 16-bit Resolution, PGA Gain = 1)
new_config = 0x10  # 0001 0000: Single-ended input, 16-bit resolution, continuous conversion, PGA gain = 1

# Zápis nové konfigurace do MCP3424
write_config(bus, address, new_config)

# Čtení aktuální konfigurace
current_config = read_config(bus, address)
if current_config is not None:
    print(f"Current Configuration: {current_config:02X}")
else:
    print("Failed to read the current configuration.")

# Čtení ADC hodnot v kontinuálním režimu
try:
    while True:
        adc_value = read_adc(bus, address)
        if adc_value is not None:
            print(f"ADC Value: {adc_value}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by User")

# Zavření sběrnice I2C
bus.close()
