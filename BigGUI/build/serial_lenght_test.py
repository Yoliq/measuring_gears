import tkinter as tk
from tkinter import StringVar
import serial
import threading
from time import sleep

# Nahraďte '/dev/ttyUSB0' skutečným sériovým portem
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

def init_serial_connection():
    for _ in range(5):  # Opakovat 5 pokusů
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            ser.flushInput()
            sleep(1)
            ser.close()
            sleep(1)
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            ser.flushInput()
            return ser
        except serial.SerialException:
            print(f"Pokus o navázání")
            sleep(2)  # Počkat 2 sekundy před dalším pokusem
    raise Exception("Nelze navázat spojení se sériovým portem")

def read_serial():
    ser = init_serial_connection()
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    # Rozdělit příchozí řetězec na dvě části
                    lanko_value, laser_value = map(float, line.split(','))
                    
                    # Nastavení hodnot pro zobrazení
                    lanko_var.set(f"{lanko_value:.1f}")
                    laser_var.set(f"{laser_value:.0f}")
                except ValueError:
                    pass  # Pokud nelze převést na float, ignorujeme chybu
        except UnicodeDecodeError:
            pass  # Ignorovat chyby dekódování a pokračovat

# Vytvoření Tkinter okna
window = tk.Tk()
window.title("Zobrazení hodnot IRC")
window.geometry("400x200")

# Proměnné pro zobrazení
lanko_var = StringVar()
laser_var = StringVar()
lanko_var.set("Čekám na data...")
laser_var.set("Čekám na data...")

# Popisky a štítky pro zobrazení hodnot
label_lanko = tk.Label(window, text="Hodnota lanka (stupně):", font=("Arial", 16))
label_lanko.pack(pady=10)
lanko_label = tk.Label(window, textvariable=lanko_var, font=("Arial", 24))
lanko_label.pack(pady=10)

label_laser = tk.Label(window, text="Hodnota laseru (stupně):", font=("Arial", 16))
label_laser.pack(pady=10)
laser_label = tk.Label(window, textvariable=laser_var, font=("Arial", 24))
laser_label.pack(pady=10)

# Zahájení čtení sériových dat
serial_thread = threading.Thread(target=read_serial)
serial_thread.daemon = True
serial_thread.start()

window.mainloop()
