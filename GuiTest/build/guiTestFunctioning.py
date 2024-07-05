from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import ttk
import serial
import serial.tools.list_ports

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\FS\DP\Code\Python\GuiTest\build\assets\frame0")

ser = None

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#ser = serial.Serial('COM6', 9600)  # Upravte COM6 podle vašeho připojení
def open_serial_connection():
    global ser
    selected_port = combo.get().split()[0]  # Získání prvního slova z názvu portu (např. "COM6")
    ser = serial.Serial(selected_port, 9600)
    # Můžeš provést další operace s ser

def update_ports():
    ports = serial.tools.list_ports.comports()
    ports_list = [str(port) for port in ports]
    combo["values"] = ports_list
        
def send_command(command):
    if ser is not None:
        ser.write(command.encode() + b'\n')
        
def forward(event):
    send_command('FORWARD')

def backward(event):
    send_command('BACKWARD')

def stop(event):
    send_command('STOP')

window = Tk()
window.title("Řízení krokáře")

window.geometry("550x550")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 550,
    width = 550,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    275.0,
    275.00000000000006,
    image=image_image_1
)

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

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=84.0,
    y=382.00000000000006,
    width=121.0,
    height=133.0
)

button_1.bind("<ButtonPress>", forward)
button_1.bind("<ButtonRelease>", stop)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=338.0,
    y=382.00000000000006,
    width=121.0,
    height=133.0
)

button_2.bind("<ButtonPress>", backward)
button_2.bind("<ButtonRelease>", stop)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    259.0,
    196.00000000000006,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()