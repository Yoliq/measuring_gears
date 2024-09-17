import serial
from time import sleep
import threading

class DualSerialReader:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.lanko_value = 0.0
        self.laser_value = 0.0
        self.reading = False

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            self.reading = True
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")

    def _disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.reading = False
            print(f"Disconnected from {self.port}")

    def _read_serial_data(self):
        while self.reading:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    lanko_str, laser_str = line.split(',')
                    self.lanko_value = float(lanko_str)
                    self.laser_value = float(laser_str)
            except (ValueError, serial.SerialException, UnicodeDecodeError) as e:
                print(f"Error reading serial data: {e}")

    def start_reading(self):
        self._connect()
        read_thread = threading.Thread(target=self._read_serial_data)
        read_thread.daemon = True
        read_thread.start()

    def stop_reading(self):
        self.reading = False
        self._disconnect()

    def get_lanko_value(self):
        return self.lanko_value

    def get_laser_value(self):
        return self.laser_value

    def get_formatted_lanko_value(self):
        return f"{self.lanko_value:.1f}"

    def get_formatted_laser_value(self):
        return f"{self.laser_value:.0f}"
