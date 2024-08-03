import serial
from time import sleep
import threading

class SerialReader:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.offset = 0.0
        self.angle = 0.0
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

    def read_serial(self):
        while self.reading:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    self.angle = float(line) - self.offset
            except (ValueError, serial.SerialException, UnicodeDecodeError) as e:
                print(f"Error reading serial data: {e}")

    def start_reading(self):
        self._connect()
        read_thread = threading.Thread(target=self.read_serial)
        read_thread.daemon = True
        read_thread.start()

    def stop_reading(self):
        self.reading = False
        self._disconnect()

    def zero_angle(self, current_angle):
        self.offset += current_angle

    def get_angle(self):
        return self.angle

    def get_formatted_angle(self):
        return f"{self.angle:.2f}"
