from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, PhotoImage
from PIL import Image, ImageTk
from stepper import Stepper_motor
from threading import Thread

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

STEPS_big_motor = 400
STEPS_small_motor = 400

#myMotor = Stepper_motor(STEP/PUL, DIR, ENABLE, Delay, STEPS)
big_motor = Stepper_motor(17, 27, 22, 0.001, STEPS_big_motor)
small_motor = Stepper_motor(16, 20, 21, 0.001, STEPS_small_motor)

uhel_sekvence=90
steps_to_rotate=STEPS_big_motor/360*uhel_sekvence

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

def start_motor_sequence(motor, direction):
    if direction == "up":
        motor.sekvence_up(None)
    else:
        motor.sekvence_down()

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
    font=("Arial BoldMT", 90 * -1)
)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(373.0, 416.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(181.0, 462.0, image=image_image_5)

# Nové funkce pro zpracování tlačítek
#def on_button_click(event, button_name):
#    print(f"{button_name} clicked")

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

canvas.tag_bind(button_3_canvas, "<Button-1>", lambda event: (on_button_press(event, button_3_canvas, button_3_pressed_photo, "Button 3"), small_motor.on_button_press_forward(event)))
canvas.tag_bind(button_3_canvas, "<ButtonRelease-1>", lambda event: (on_button_release(event, button_3_canvas, button_3_photo, "Button 3"), small_motor.on_button_release_forward(event)))

# Tlacitko 4 OS+
button_image_4_path = relative_to_assets("button_4.png")
button_image_4_pressed_path = relative_to_assets("button_4_pressed.png")
button_image_4 = Image.open(button_image_4_path).convert("RGBA")
button_4_photo = ImageTk.PhotoImage(button_image_4)
button_4_pressed = Image.open(button_image_4_pressed_path).convert("RGBA")
button_4_pressed_photo = ImageTk.PhotoImage(button_4_pressed)
button_4_canvas = canvas.create_image(1624, 880, image=button_4_photo, anchor="nw")

canvas.tag_bind(button_4_canvas, "<Button-1>", lambda event: (on_button_press(event, button_4_canvas, button_4_pressed_photo, "Button 4"), small_motor.on_button_press_backward(event)))
canvas.tag_bind(button_4_canvas, "<ButtonRelease-1>", lambda event: (on_button_release(event, button_4_canvas, button_4_photo, "Button 4"), small_motor.on_button_release_backward(event)))

# Tlacitko 5 HOME
button_image_5_path = relative_to_assets("button_5.png")
button_image_5_pressed_path = relative_to_assets("button_5_pressed.png")
button_image_5 = Image.open(button_image_5_path).convert("RGBA")
button_5_photo = ImageTk.PhotoImage(button_image_5)
button_5_pressed = Image.open(button_image_5_pressed_path).convert("RGBA")
button_5_pressed_photo = ImageTk.PhotoImage(button_5_pressed)
button_5_canvas = canvas.create_image(959, 169, image=button_5_photo, anchor="nw")

canvas.tag_bind(button_5_canvas, "<Button-1>", lambda event: on_button_press(event, button_5_canvas, button_5_pressed_photo, "Button 5"))
canvas.tag_bind(button_5_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_5_canvas, button_5_photo, "Button 5"))

# Tlacitko 6 NULOVAT
button_image_6_path = relative_to_assets("button_6.png")
button_image_6_pressed_path = relative_to_assets("button_6_pressed.png")
button_image_6 = Image.open(button_image_6_path).convert("RGBA")
button_6_photo = ImageTk.PhotoImage(button_image_6)
button_6_pressed = Image.open(button_image_6_pressed_path).convert("RGBA")
button_6_pressed_photo = ImageTk.PhotoImage(button_6_pressed)
button_6_canvas = canvas.create_image(1208, 166, image=button_6_photo, anchor="nw")

canvas.tag_bind(button_6_canvas, "<Button-1>", lambda event: on_button_press(event, button_6_canvas, button_6_pressed_photo, "Button 6"))
canvas.tag_bind(button_6_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_6_canvas, button_6_photo, "Button 6"))

image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(1183.0, 324.0, image=image_image_8)

image_image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(1366.0, 591.0, image=image_image_9)

image_image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(957, 315, image=image_image_10)

image_image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(1576.0, 614.0, image=image_image_11)

image_image_12 = PhotoImage(file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(1320.0, 409.0, image=image_image_12)

# Tlacitko 7 STOP
button_image_7_path = relative_to_assets("button_7.png")
button_image_7_pressed_path = relative_to_assets("button_7_pressed.png")
button_image_7 = Image.open(button_image_7_path).convert("RGBA")
button_7_photo = ImageTk.PhotoImage(button_image_7)
button_7_pressed = Image.open(button_image_7_pressed_path).convert("RGBA")
button_7_pressed_photo = ImageTk.PhotoImage(button_7_pressed)
button_7_canvas = canvas.create_image(2269, 17, image=button_7_photo, anchor="nw")

canvas.tag_bind(button_7_canvas, "<Button-1>", lambda event: on_button_press(event, button_7_canvas, button_7_pressed_photo, "Button 7"))
canvas.tag_bind(button_7_canvas, "<ButtonRelease-1>", lambda event: on_button_release(event, button_7_canvas, button_7_photo, "Button 7"))

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

image_image_13 = PhotoImage(file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(1567.0, 1057.0, image=image_image_13)

image_image_14 = PhotoImage(file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(1543.0, 1184.0, image=image_image_14)

image_image_15 = PhotoImage(file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(1543.0, 1300.0, image=image_image_15)

image_image_16 = PhotoImage(file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(2164.5106201171875, 470.0, image=image_image_16)

image_image_17 = PhotoImage(file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(340.0, 1288.0, image=image_image_17)

image_image_18 = PhotoImage(file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(1526.0, 73.0, image=image_image_18)

image_image_19 = PhotoImage(file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(1854.0, 73.0, image=image_image_19)

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

image_image_20 = PhotoImage(file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(2164.5106201171875, 1073.0, image=image_image_20)

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

image_image_21 = PhotoImage(file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(1051.0, 1254.0, image=image_image_21)

canvas.create_text(
     1261.0,
    297.0,
    anchor="nw",  # 'ne' stands for North-East, which aligns the text to the right
    text="20,46",
    fill="#000000",
    font=("Arial", 40 * -1, "bold")  # Correctly specify the font weight
)

canvas.create_text(
    1261.0,
    383.0,
    anchor="nw",
    text="18,46",
    fill="#000000",
    font=("Arial", 40 * -1, "bold")
)

canvas.create_text(
    1129.0,
    1227.0,
    anchor="nw",
    text="20,46",
    fill="#000000",
    font=("RobotoRoman Bold", 40 * -1)
)

image_image_22 = PhotoImage(file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(940.999986493181, 475.0, image=image_image_22)

canvas.create_text(
    1487.0,
    611.0,
    anchor="nw",
    text="40,5",
    fill="#000000",
    font=("RobotoRoman Bold", 36 * -1)
)

canvas.create_text(
    1411.0,
    1295.0,
    anchor="nw",
    text="175,5",
    fill="#000000",
    font=("RobotoRoman Bold", 32 * -1)
)

canvas.create_text(
    1440.0,
    1178.0,
    anchor="nw",
    text="160,5",
    fill="#000000",
    font=("RobotoRoman Bold", 32 * -1)
)

canvas.create_text(
    1457.0,
    1052.0,
    anchor="nw",
    text="150,5",
    fill="#000000",
    font=("RobotoRoman Bold", 36 * -1)
)

#window.resizable(False, False)
window.mainloop()
