from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, PhotoImage, StringVar
from PIL import Image, ImageTk
from stepper import Stepper_motor
from threading import Thread
import RPi.GPIO as GPIO
import re 
import camera
import cv2
import time
from serial_read import SerialReader
from multiprocessing import Process, Queue

from constants import *
from Endstop import Endstop

'''
START SERIAL READERS
    * used to connect real time MCUs to Raspberry Pi
    * MCUs sends IRC information over USB
'''

# Hnaci kolo

serial_reader_hnaci_kolo = SerialReader(USB_IRC_HNACI_KOLO, SERIAL_BAUDRATE)
# Pripojeni a odpojeni Serialu (bypass chyby, kdy se serial otevre az na druhy pokus)
serial_reader_hnaci_kolo.start_reading()
time.sleep(1)
serial_reader_hnaci_kolo.stop_reading()
time.sleep(1)
# Zahajeni komunikace naostro
serial_reader_hnaci_kolo.start_reading()

# Hnane kolos
serial_reader_hnane_kolo = SerialReader(USB_IRC_HNANE_KOLO, SERIAL_BAUDRATE)
serial_reader_hnane_kolo.start_reading()
time.sleep(1)
serial_reader_hnane_kolo.stop_reading()
time.sleep(1)
serial_reader_hnane_kolo.start_reading()

'''
CREATE MOTORS
'''

big_motor = Stepper_motor(STEP_PIN_BIG_MOTOR,
                          DIR_PIN_BIG_MOTOR,
                          ENABLE_PIN_BIG_MOTOR,
                          SPEED_BIG_MOTOR,
                          STEPS_BIG_MOTOR,
                          PREVODOVY_POMER_BIG_MOTOR,
                          SEKVENCE_VELIKOST_NATOCENI,
                          ENDSTOP_VELIKOST_CUKNUTI)

small_motor = Stepper_motor(STEP_PIN_SMALL_MOTOR,
                          DIR_PIN_SMALL_MOTOR,
                          ENABLE_PIN_SMALL_MOTOR,
                          SPEED_SMALL_MOTOR,
                          STEPS_SMALL_MOTOR,
                          PREVODOVY_POMER_SMALL_MOTOR,
                          SEKVENCE_VELIKOST_NATOCENI,
                          ENDSTOP_VELIKOST_CUKNUTI)


'''
Takes path as string.
Returns path object which points to location specified by ASSETS_PATH/path
'''
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

''' 
Used for checking hmotnost entry and osova vzdalenost entry.
Must be either:
    * numeric value
    * empty string so it is possible to leave the text box
'''
def validate_numeric_input(new_value):
    if new_value == "" or new_value.replace('.', '', 1).isdigit() or new_value.replace(',', '', 1).isdigit():
        return True
    return False

'''
GUI START
'''
window = Tk()
window.geometry("2560x1440")
window.configure(bg="#FFFFFF")

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    window.state = not window.state  # Just toggling the boolean
    window.attributes("-fullscreen", window.state)
    return "break"

# Function to end fullscreen mode
def end_fullscreen(event=None):
    window.state = False
    window.attributes("-fullscreen", False)
    return "break"

# Proměnná pro uchování hodnoty natočení páky
natoceni_paky = StringVar()
natoceni_paky.set("Čekám")  # Původní hodnota

# Proměnná pro uchování hodnoty natočení kola
natoceni_kola = StringVar()
natoceni_kola.set("Čekám")  # Původní hodnota

# Proměnná pro uchování hodnoty natočení páky hlavní
natoceni_paky_hlavni = StringVar()
natoceni_paky_hlavni.set("Čekám")  # Původní hodnota

# Aktualizace hodnoty natočení páky
def update_angle():
    natoceni_paky.set(serial_reader_hnaci_kolo.get_formatted_angle())
    natoceni_kola.set(serial_reader_hnane_kolo.get_formatted_angle())
    natoceni_paky_hlavni.set(natoceni_paky.get())
    window.after(100, update_angle)  # Aktualizace každých 100 ms

# Vynulovani paky
def zero_angle():
    current_angle_paka = float(natoceni_paky.get())
    serial_reader_hnaci_kolo.zero_angle(current_angle_paka)
    current_angle_kolo = float(natoceni_kola.get())
    serial_reader_hnane_kolo.zero_angle(current_angle_kolo)

'''
CREATE ENDSTOPS
'''
endstop_paka = Endstop(ENDSTOP_PIN,
                        big_motor,
                        ENDSTOP_OFFSET,
                        serial_reader_hnaci_kolo,
                        serial_reader_hnane_kolo,
                        natoceni_paky,
                        natoceni_kola,
                        natoceni_paky_hlavni)

# Zahájení aktualizace hodnoty natočení páky
update_angle()

def start_motor_sequence(motor, direction):
    if direction == "up":
        motor.sekvence_up(SEKVENCE_VELIKOST_NATOCENI)
    else:
        motor.sekvence_down(SEKVENCE_VELIKOST_NATOCENI)

def home(event):
    print("Home button pressed")
    Thread(target=big_motor.start_motor, args=(GPIO.LOW,)).start()

'''
Camera code
'''

def update_frame(queue):
    if not queue.empty():
        frame = queue.get()
        if frame is not None:
            frame = cv2.resize(frame, (704, 461))
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            canvas.create_image(cmx, cmy, image=photo, anchor=tk.NW)
            window.photo = photo
    window.after(33, update_frame, queue)  # Cca 30 fps

def start_recording():
    recording_queue.put(True)

def stop_recording():
    recording_queue.put(False)

def on_closing():
    recording_queue.put(False)  # Zastavit nahrávání, pokud běží
    process.terminate()  # Ukončit proces kamery
    process.join()  # Počkat na ukončení procesu
    window.destroy()

# Inicializace kamery a spuštění náhledu při spuštění programu
cam = camera.Camera()

'''
SHORTCUTS DEFINITION
'''
window.protocol("WM_DELETE_WINDOW", on_closing)
window.bind("<F11>", toggle_fullscreen)
window.bind("<Escape>", end_fullscreen)
window.bind("<Button-3>", end_fullscreen)  # Bind right mouse button


# Initially start in fullscreen mode
window.state = True
window.attributes("-fullscreen", True)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=1440,
    width=2560,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(1280.0, 720.0, image=image_image_1)

canvas.create_rectangle(0.0, 0.0, 2560.0, 146.0, fill="#E5E377", outline="")

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(939.0, 940.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(1157.0, 1092.999996786646, image=image_image_3)

canvas.create_text(
    34.0,
    25.0,
    anchor="nw",
    text="OVLÁDÁNÍ STANOVIŠTĚ",
    fill="#000000",
    font=("Arial", 90 * -1, "bold")
)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(373.0, 416.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(181.0, 462.0, image=image_image_5)

# TODO jsou tu potreba ty eventy?
def on_button_press(event, button_canvas, pressed_photo, button_name):
    canvas.itemconfig(button_canvas, image=pressed_photo)
    canvas.move(button_canvas, 4, 4)
    print(f"{button_name} clicked")

def on_button_release(event, button_canvas, photo, button_name):
    canvas.itemconfig(button_canvas, image=photo)
    canvas.move(button_canvas, -4, -4)
    print(f"{button_name} released")

# Tlacitko 1 Natoceni motoru nahoru
button_image_1_path = relative_to_assets("button_1.png")
button_image_1_pressed_path = relative_to_assets("button_1_pressed.png")
button_image_1 = Image.open(button_image_1_path).convert("RGBA")
button_1_photo = ImageTk.PhotoImage(button_image_1)
button_1_pressed = Image.open(button_image_1_pressed_path).convert("RGBA")
button_1_pressed_photo = ImageTk.PhotoImage(button_1_pressed)
button_1_canvas = canvas.create_image(57, 435, image=button_1_photo, anchor="nw")

canvas.tag_bind(button_1_canvas, "<Button-1>", lambda event: (on_button_press(event, button_1_canvas, button_1_pressed_photo, "Button 1"), big_motor.on_button_press_forward(event)))
canvas.tag_bind(button_1_canvas, "<ButtonRelease-1>", lambda event: (on_button_release(event, button_1_canvas, button_1_photo, "Button 1"), big_motor.on_button_release_forward(event)))

# Tlacitko 2 Natoceni motoru dolu
button_image_2_path = relative_to_assets("button_2.png")
button_image_2_pressed_path = relative_to_assets("button_2_pressed.png")
button_image_2 = Image.open(button_image_2_path).convert("RGBA")
button_2_photo = ImageTk.PhotoImage(button_image_2)
button_2_pressed = Image.open(button_image_2_pressed_path).convert("RGBA")
button_2_pressed_photo = ImageTk.PhotoImage(button_2_pressed)
button_2_canvas = canvas.create_image(200, 435, image=button_2_photo, anchor="nw")

canvas.tag_bind(button_2_canvas, "<Button-1>", lambda event: (on_button_press(event, button_2_canvas, button_2_pressed_photo, "Button 2"), big_motor.on_button_press_backward(event)))
canvas.tag_bind(button_2_canvas, "<ButtonRelease-1>", lambda event: (on_button_release(event, button_2_canvas, button_2_photo, "Button 2"), big_motor.on_button_release_backward(event)))

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(1350.0, 888.9998418521883, image=image_image_6)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(1567.0, 897.0, image=image_image_7)

# Tlacitko 3 OS+
button_image_3_path = relative_to_assets("button_3.png")
button_image_3_pressed_path = relative_to_assets("button_3_pressed.png")
button_image_3 = Image.open(button_image_3_path).convert("RGBA")
button_3_photo = ImageTk.PhotoImage(button_image_3)
button_3_pressed = Image.open(button_image_3_pressed_path).convert("RGBA")
button_3_pressed_photo = ImageTk.PhotoImage(button_3_pressed)
button_3_canvas = canvas.create_image(1417, 880, image=button_3_photo, anchor="nw")

canvas.tag_bind(button_3_canvas, "<Button-1>", lambda event: (on_button_press(event, button_3_canvas, button_3_pressed_photo, "Button 3"), small_motor.on_button_press_backward(event)))
canvas.tag_bind(button_3_canvas, "<ButtonRelease-1>", lambda event: (on_button_release(event, button_3_canvas, button_3_photo, "Button 3"), small_motor.on_button_release_backward(event)))

# Tlacitko 4 OS-
button_image_4_path = relative_to_assets("button_4.png")
button_image_4_pressed_path = relative_to_assets("button_4_pressed.png")
button_image_4 = Image.open(button_image_4_path).convert("RGBA")
button_4_photo = ImageTk.PhotoImage(button_image_4)
button_4_pressed = Image.open(button_image_4_pressed_path).convert("RGBA")
button_4_pressed_photo = ImageTk.PhotoImage(button_4_pressed)
button_4_canvas = canvas.create_image(1624, 880, image=button_4_photo, anchor="nw")

canvas.tag_bind(button_4_canvas, "<Button-1>", lambda event: (on_button_press(event, button_4_canvas, button_4_pressed_photo, "Button 4"), small_motor.on_button_press_forward(event)))
canvas.tag_bind(button_4_canvas, "<ButtonRelease-1>", lambda event: (on_button_release(event, button_4_canvas, button_4_photo, "Button 4"), small_motor.on_button_release_forward(event)))

# Tlacitko 5 HOME
button_image_5_path = relative_to_assets("button_5.png")
button_image_5_pressed_path = relative_to_assets("button_5_pressed.png")
button_image_5 = Image.open(button_image_5_path).convert("RGBA")
button_5_photo = ImageTk.PhotoImage(button_image_5)
button_5_pressed = Image.open(button_image_5_pressed_path).convert("RGBA")
button_5_pressed_photo = ImageTk.PhotoImage(button_5_pressed)
button_5_canvas = canvas.create_image(945, 169, image=button_5_photo, anchor="nw")

canvas.tag_bind(button_5_canvas, "<Button-1>", lambda event: (on_button_press(event, button_5_canvas, button_5_pressed_photo, "Home"), home(event)))
canvas.tag_bind(button_5_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_5_canvas, button_5_photo, "Home"))

# Tlacitko 6 NULOVAT
button_image_6_path = relative_to_assets("button_6.png")
button_image_6_pressed_path = relative_to_assets("button_6_pressed.png")
button_image_6 = Image.open(button_image_6_path).convert("RGBA")
button_6_photo = ImageTk.PhotoImage(button_image_6)
button_6_pressed = Image.open(button_image_6_pressed_path).convert("RGBA")
button_6_pressed_photo = ImageTk.PhotoImage(button_6_pressed)
button_6_canvas = canvas.create_image(1220, 166, image=button_6_photo, anchor="nw")

canvas.tag_bind(button_6_canvas, "<Button-1>", lambda event: (on_button_press(event, button_6_canvas, button_6_pressed_photo, "Button 6"), zero_angle()))
canvas.tag_bind(button_6_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_6_canvas, button_6_photo, "Button 6"))

# Tlacitko 7 STOP
button_image_7_path = relative_to_assets("button_7.png")
button_image_7_pressed_path = relative_to_assets("button_7_pressed.png")
button_image_7 = Image.open(button_image_7_path).convert("RGBA")
button_7_photo = ImageTk.PhotoImage(button_image_7)
button_7_pressed = Image.open(button_image_7_pressed_path).convert("RGBA")
button_7_pressed_photo = ImageTk.PhotoImage(button_7_pressed)
button_7_canvas = canvas.create_image(2269, 17, image=button_7_photo, anchor="nw")

canvas.tag_bind(button_7_canvas, "<Button-1>", lambda event: (on_button_press(event, button_7_canvas, button_7_pressed_photo, "STOP"), big_motor.stop_motor(), small_motor.stop_motor()))
canvas.tag_bind(button_7_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_7_canvas, button_7_photo, "STOP"))

# Tlacitko 8 ULOZIT
button_image_8_path = relative_to_assets("button_8.png")
button_image_8_pressed_path = relative_to_assets("button_8_pressed.png")
button_image_8 = Image.open(button_image_8_path).convert("RGBA")
button_8_photo = ImageTk.PhotoImage(button_image_8)
button_8_pressed = Image.open(button_image_8_pressed_path).convert("RGBA")
button_8_pressed_photo = ImageTk.PhotoImage(button_8_pressed)
button_8_canvas = canvas.create_image(1953, 28, image=button_8_photo, anchor="nw")

canvas.tag_bind(button_8_canvas, "<Button-1>", lambda event: on_button_press(event, button_8_canvas, button_8_pressed_photo, "Button 8"))
canvas.tag_bind(button_8_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_8_canvas, button_8_photo, "Button 8"))

image_image_17 = PhotoImage(file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(340.0, 1288.0, image=image_image_17)

# Tlacitko 9 NAPOVEDA
button_image_9_path = relative_to_assets("button_9.png")
button_image_9_pressed_path = relative_to_assets("button_9_pressed.png")
button_image_9 = Image.open(button_image_9_path).convert("RGBA")
button_9_photo = ImageTk.PhotoImage(button_image_9)
button_9_pressed = Image.open(button_image_9_pressed_path).convert("RGBA")
button_9_pressed_photo = ImageTk.PhotoImage(button_9_pressed)
button_9_canvas = canvas.create_image(534, 1272, image=button_9_photo, anchor="nw")

canvas.tag_bind(button_9_canvas, "<Button-1>", lambda event: on_button_press(event, button_9_canvas, button_9_pressed_photo, "Button 9"))
canvas.tag_bind(button_9_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_9_canvas, button_9_photo, "Button 9"))

#Kamera
image_image_20 = PhotoImage(file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(2164.5106201171875, 1073.0, image=image_image_20)
cmx=1810.98
cmy=867.06-17
cam_window = canvas.create_rectangle(cmx, cmy, cmx+704.05, cmy+460.9, fill="gray", outline="")


# Tlacitko 10 SEKVENCE UP
button_image_10_path = relative_to_assets("button_10.png")
button_image_10_pressed_path = relative_to_assets("button_10_pressed.png")
button_image_10 = Image.open(button_image_10_path).convert("RGBA")
button_10_photo = ImageTk.PhotoImage(button_image_10)
button_10_pressed = Image.open(button_image_10_pressed_path).convert("RGBA")
button_10_pressed_photo = ImageTk.PhotoImage(button_10_pressed)
button_10_canvas = canvas.create_image(26, 182, image=button_10_photo, anchor="nw")

canvas.tag_bind(button_10_canvas, "<Button-1>", lambda event: (on_button_press(event, button_10_canvas, button_10_pressed_photo, "Button 10"), Thread(target=start_motor_sequence, args=(big_motor, "up")).start()))
canvas.tag_bind(button_10_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_10_canvas, button_10_photo, "Button 10"))

# Tlacitko 11 SEKVENCE DOWN
button_image_11_path = relative_to_assets("button_11.png")
button_image_11_pressed_path = relative_to_assets("button_11_pressed.png")
button_image_11 = Image.open(button_image_11_path).convert("RGBA")
button_11_photo = ImageTk.PhotoImage(button_image_11)
button_11_pressed = Image.open(button_image_11_pressed_path).convert("RGBA")
button_11_pressed_photo = ImageTk.PhotoImage(button_11_pressed)
button_11_canvas = canvas.create_image(406, 182, image=button_11_photo, anchor="nw")

canvas.tag_bind(button_11_canvas, "<Button-1>", lambda event: (on_button_press(event, button_11_canvas, button_11_pressed_photo, "Button 11"), Thread(target=start_motor_sequence, args=(big_motor, "down")).start()))
canvas.tag_bind(button_11_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_11_canvas, button_11_photo, "Button 11"))

image_image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(957, 315, image=image_image_10)

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(1183.0, 324.0, image=image_image_8)

image_image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(1366.0, 591.0, image=image_image_9)

image_image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(1576.0, 614.0, image=image_image_11)

image_image_12 = PhotoImage(file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(1320.0, 409.0, image=image_image_12)

image_image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(1567.0, 1057.0, image=image_image_13)

image_image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(1567, 1184.0, image=image_image_14)

image_image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(1567, 1300.0, image=image_image_15)

image_image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(2164.5106201171875, 470.0, image=image_image_16)

image_image_18 = PhotoImage(file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(1526.0, 73.0, image=image_image_18)

image_image_19 = PhotoImage(file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(1854.0, 73.0, image=image_image_19)

image_image_21 = PhotoImage(file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(1051.0, 1254.0, image=image_image_21)

image_image_22 = PhotoImage(file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(940.999986493181, 475.0, image=image_image_22)

#Natočení páky 1
angle_label_paka = tk.Label(window, textvariable=natoceni_paky, justify='center', bg='#8CDAFF', font=("Arial", 36 * -1, "bold"))
angle_label_paka.place(x=1256, y=300)


#Natočení páky 2
angle_label_paka_hlavni = tk.Label(window, textvariable= natoceni_paky_hlavni, justify='center', bg='#8CDAFF', font=("Arial", 36 * -1, "bold"))
angle_label_paka.place(x=1267-11, y=386)
# canvas.create_text(
#     1267-11,
#     386,
#     anchor="nw",
#     text="318,46",
#     fill="#000000",
#     font=("Arial", 40 * -1, "bold")
# )

#Natočení kola
angle_label_kolo = tk.Label(window, textvariable=natoceni_kola, justify='center', bg='#8CDAFF', font=("Arial", 36 * -1, "bold"))
angle_label_kolo.place(x=1135-11, y=1230)

# canvas.create_text(
#     1135-11,
#     1230,
#     anchor="nw",
#     text="360,46",
#     fill="#000000",
#     font=("Arial", 40 * -1, "bold")
# )

# Funkce pro validaci názvu souboru
def validate_nazev(nazev_value):    
    return not bool(re.search(r'[\/\\:*"?<>|]', nazev_value)) #Povolené znaky: Všechno kromě / \ : * " ? < > |
# Registrace validační funkce
validate_filename_command = window.register(validate_nazev)

# Funkce pro nastavení a odstranění placeholderu
def set_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')

def clear_placeholder(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg='black')

def restore_placeholder(event, entry, placeholder_text):
    if entry.get() == '':
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

#Zadat název
entry_nazev = Entry(window, font=("Arial", 32, "italic"), bd=0, highlightthickness=0, relief="flat", validate="key", validatecommand=(validate_filename_command, "%P"))
entry_nazev.place(x=1319, y=50, width=416)
set_placeholder(entry_nazev, "Zadej název") #Placeholder pro název měření

entry_nazev.bind("<FocusIn>", lambda event: clear_placeholder(event, entry_nazev, "Zadej název"))
entry_nazev.bind("<FocusOut>", lambda event: restore_placeholder(event, entry_nazev, "Zadej název"))

def get_nazev(event=None):
    nazev= entry_nazev.get()
    print(f"Název: {nazev}")
    window.focus_set()

entry_nazev.bind("<Return>", get_nazev)
entry_nazev.bind("<KP_Enter>", get_nazev)

#Zadat datum
entry_datum = Entry(window, font=("Arial", 32, "italic"), bd=0, highlightthickness=0, relief="flat", validate="key", validatecommand=(validate_filename_command, "%P"))
entry_datum.place(x=1754+5, y=50, width=193)
set_placeholder(entry_datum, "Datum") #Placeholder pro název měření

entry_datum.bind("<FocusIn>", lambda event: clear_placeholder(event, entry_datum, "Datum"))
entry_datum.bind("<FocusOut>", lambda event: restore_placeholder(event, entry_datum, "Datum"))

def get_datum(event=None):
    datum= entry_datum.get()
    print(f"Datum: {datum}")
    window.focus_set()

entry_datum.bind("<Return>", get_datum)
entry_datum.bind("<KP_Enter>", get_datum)

#Hmotnost - zadat
entry_var = StringVar()
validate_command = window.register(validate_numeric_input)
entry_hmotnost = Entry(window, font=("Arial", 36*-1, "bold"), bd=0, highlightthickness=0, relief="flat", justify="center", textvariable=entry_var, validate="key", validatecommand=(validate_command, "%P"))
entry_hmotnost.place(x=1425, y=616, width=188)

def get_hmotnost_value(event=None):
    try:
        hmotnost = float(entry_hmotnost.get().replace(',', '.'))  # Převod řetězce na float
        print(f"Hmotnost: {hmotnost}") #Můžeš zkusit přenásobit číslem pro kontrolu, že to je fakt číslo
    except ValueError:
        print("Zadaná hodnota není platné číslo.")
    window.focus_set()  # Přesun fokusu na hlavní okno

entry_hmotnost.bind("<Return>", get_hmotnost_value)
entry_hmotnost.bind("<KP_Enter>", get_hmotnost_value)

# Osová vzdálenost - zadat
entry_os_vzdalenost_var = StringVar()
entry_os_vzdalenost = Entry(window, font=("Arial", 36 * -1, "bold"), bd=0, highlightthickness=0, relief="flat", justify="center", textvariable=entry_os_vzdalenost_var, validate="key", validatecommand=(validate_command, "%P"))
entry_os_vzdalenost.place(x=1416, y=1058, width=164)

def get_os_vzdalenost_value(event=None):
    try:
        os_vzdalenost = float(entry_os_vzdalenost.get().replace(',', '.'))
        print(f"Osová vzdálenost: {os_vzdalenost*10}")
    except ValueError:
        print("Zadaná hodnota není platné číslo.")
    window.focus_set()  # Přesun fokusu na hlavní okno
    
entry_os_vzdalenost.bind("<Return>", get_os_vzdalenost_value)
entry_os_vzdalenost.bind("<KP_Enter>", get_os_vzdalenost_value)

#Lankový snímač
canvas.create_text(
    1475,
    1184,
    anchor="nw",
    text="160,5",
    fill="#000000",
    font=("Arial", 32 * -1, "bold")
)
#Laserový snímač
canvas.create_text(
    1475,
    1301,
    anchor="nw",
    text="175,5",
    fill="#000000",
    font=("Arial", 32 * -1, "bold")
)
def close_window(event=None):
    on_closing()  # Zavolat funkci on_closing pro správné ukončení

'''
Camera shitstorm
'''

def update_frame(queue):
    if not queue.empty():
        frame = queue.get()
        if frame is not None:
            frame = cv2.resize(frame, (704, 461))
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            canvas.create_image(cmx, cmy, image=photo, anchor=tk.NW)
            window.photo = photo
    window.after(33, update_frame, queue)  # Cca 30 fps

# Inicializace fronty a spuštění video procesu
frame_queue = Queue()
recording_queue = Queue()
process = Process(target=camera.video_process, args=(frame_queue, recording_queue))
process.start()

# Inicializace náhledu
window.after(0, update_frame, frame_queue)


# Bind klávesy "Q" pro zavření okna
window.bind("<q>", close_window)

#window.resizable
# (False, False)
window.mainloop()