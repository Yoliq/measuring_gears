from pathlib import Path
from tkinter import *
from PIL import Image, ImageDraw, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def button_1_action():
    print("button_1 clicked")

def button_2_action():
    print("button_2 clicked")

def create_rounded_rectangle_image(width, height, radius, color):
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([(0, 0), (width, height)], radius, fill=color)
    return ImageTk.PhotoImage(image)

window = Tk()
window.geometry("550x550")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=550,
    width=550,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(275.0, 275.0, image=image_image_1)

# Create rounded rectangle images for buttons
rounded_image_1 = create_rounded_rectangle_image(121, 133, 30, "#98FB98")
rounded_image_2 = create_rounded_rectangle_image(121, 133, 30, "#D3D3D3")

button_1 = Button(
    window,
    image=rounded_image_1,
    text="+",
    font=("Arial", 24),
    compound="center",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    command=button_1_action,
    relief="flat"
)
button_1.place(
    x=84.0,
    y=382.0,
    width=121.0,
    height=133.0
)

button_2 = Button(
    window,
    image=rounded_image_2,
    text="-",
    font=("Arial", 24),
    compound="center",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    command=button_2_action,
    relief="flat"
)
button_2.place(
    x=338.0,
    y=382.0,
    width=121.0,
    height=133.0
)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(275.0, 175.0, image=image_image_2)

window.resizable(False, False)
window.mainloop()
