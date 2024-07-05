from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_button_click_1(event):
    print("button_1 clicked")

def on_button_click_2(event):
    print("button_2 clicked")

def on_button_press_1(event):
    canvas.itemconfig(button_1_canvas, image=button_1_pressed_photo)
    canvas.move(button_1_canvas, 2, 2)

def on_button_release_1(event):
    canvas.itemconfig(button_1_canvas, image=button_1_photo)
    canvas.move(button_1_canvas, -2, -2)
    on_button_click_1(event)

def on_button_press_2(event):
    canvas.itemconfig(button_2_canvas, image=button_2_pressed_photo)
    canvas.move(button_2_canvas, 2, 2)

def on_button_release_2(event):
    canvas.itemconfig(button_2_canvas, image=button_2_photo)
    canvas.move(button_2_canvas, -2, -2)
    on_button_click_2(event)

window = Tk()
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

# Načtení obrázků pro tlačítka
button_image_1_path = relative_to_assets("button_1.png")
button_image_1 = Image.open(button_image_1_path).convert("RGBA")
button_1_photo = ImageTk.PhotoImage(button_image_1)

button_image_1_pressed_path = relative_to_assets("button_1_pressed.png")
button_image_1_pressed = Image.open(button_image_1_pressed_path).convert("RGBA")
button_1_pressed_photo = ImageTk.PhotoImage(button_image_1_pressed)

button_image_2_path = relative_to_assets("button_2.png")
button_image_2 = Image.open(button_image_2_path).convert("RGBA")
button_2_photo = ImageTk.PhotoImage(button_image_2)

button_image_2_pressed_path = relative_to_assets("button_2_pressed.png")
button_image_2_pressed = Image.open(button_image_2_pressed_path).convert("RGBA")
button_2_pressed_photo = ImageTk.PhotoImage(button_image_2_pressed)

# Vytvoření tlačítek jako obrázky na canvasu
button_1_canvas = canvas.create_image(144.5, 442.5, image=button_1_photo, anchor="center")
button_2_canvas = canvas.create_image(398.5, 442.5, image=button_2_photo, anchor="center")

# Bind událostí pro tlačítka
canvas.tag_bind(button_1_canvas, "<Button-1>", on_button_press_1)
canvas.tag_bind(button_1_canvas, "<ButtonRelease-1>", on_button_release_1)

canvas.tag_bind(button_2_canvas, "<Button-1>", on_button_press_2)
canvas.tag_bind(button_2_canvas, "<ButtonRelease-1>", on_button_release_2)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    259.0,
    196.00000000000006,
    image=image_image_2
)

window.resizable(False, False)
window.mainloop()
