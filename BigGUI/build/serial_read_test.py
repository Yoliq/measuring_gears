import tkinter as tk
from tkinter import StringVar
import serial
import threading
from time import sleep

# Nahraďte '/dev/ttyUSB0' skutečným sériovým portem
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Globální proměnná pro offset
offset = 0.0

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
    global offset
    ser = init_serial_connection()
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    angle = float(line)
                    adjusted_angle = angle - offset
                    formatted_angle = f"{adjusted_angle:.2f}"
                    angle_var.set(formatted_angle)
                except ValueError:
                    pass  # Pokud nelze převést na float, ignorujeme chybu
        except UnicodeDecodeError:
            pass  # Ignorovat chyby dekódování a pokračovat

def zero_angle():
    global offset
    try:
        current_angle = float(angle_var.get())
        offset += current_angle  # Adjust offset by the current angle
    except ValueError:
        pass  # Pokud není možné získat aktuální úhel, ignorujeme chybu

# Vytvoření Tkinter okna
window = tk.Tk()
window.title("Zobrazení úhlu IRC")
window.geometry("400x200")

angle_var = StringVar()
angle_var.set("Čekám na data...")

label = tk.Label(window, text="Aktuální úhel (stupně):", font=("Arial", 16))
label.pack(pady=20)

angle_label = tk.Label(window, textvariable=angle_var, font=("Arial", 24))
angle_label.pack(pady=20)

# Tlačítko pro nulování
zero_button = tk.Button(window, text="Nulovat", command=zero_angle, font=("Arial", 16))
zero_button.pack(pady=10)

# Zahájení čtení sériových dat
serial_thread = threading.Thread(target=read_serial)
serial_thread.daemon = True
serial_thread.start()

window.mainloop()
