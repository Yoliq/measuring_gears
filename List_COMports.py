from tkinter import Tk
from tkinter import ttk
import serial.tools.list_ports

def open_serial_connection():
    selected_port = combo.get().split()[0]  # Získání prvního slova z názvu portu (např. "COM6")
    ser = serial.Serial(selected_port, 9600)
    # Můžeš provést další operace s ser

def update_ports():
    ports = serial.tools.list_ports.comports()
    ports_list = [str(port) for port in ports]
    combo["values"] = ports_list

window = Tk()
window.title("Select COM Port")

# Vytvoření rozbalovacího menu pro COM porty
combo_frame = ttk.Frame(window)
combo_frame.pack(padx=20, pady=20)

combo_label = ttk.Label(combo_frame, text="Vyberte COM port:")
combo_label.pack(side="left")

combo = ttk.Combobox(combo_frame, state="readonly")
combo.pack(side="left", padx=10)

update_ports()  # Načíst dostupné COM porty

refresh_button = ttk.Button(window, text="Obnovit", command=update_ports)
refresh_button.pack(pady=10)

connect_button = ttk.Button(window, text="Připojit", command=open_serial_connection)
connect_button.pack(pady=10)

window.mainloop()
