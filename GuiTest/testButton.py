import tkinter as tk
from PIL import Image, ImageTk
x = 1000
y = 750

# Vytvoření hlavního okna
root = tk.Tk()
root.title("Jednoduché GUI s tlačítkem")
root.geometry(f"{x}x{y}")  # Zvětšení okna na dvojnásobek původní velikosti

# Načtení obrázku pozadí
bg_image_path = "backgrnd.jpeg"
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image.resize((x, y)))

# Vytvoření canvasu
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Nastavení obrázku pozadí na canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Načtení a zvětšení obrázků pro tlačítka
button_plain_image_path = "Button_plain.png"
button_plain_pressed_image_path = "Button_plain_pressed.png"
button_image_path = "Button.png"
button_pressed_image_path = "Button_pressed.png"

button_plain_image = Image.open(button_plain_image_path).convert("RGBA")
button_plain_photo = ImageTk.PhotoImage(button_plain_image.resize((button_plain_image.width*2, button_plain_image.height*2)))

button_plain_pressed_image = Image.open(button_plain_pressed_image_path).convert("RGBA")
button_plain_pressed_photo = ImageTk.PhotoImage(button_plain_pressed_image.resize((button_plain_pressed_image.width*2, button_plain_pressed_image.height*2)))

button_image = Image.open(button_image_path).convert("RGBA")
button_photo = ImageTk.PhotoImage(button_image.resize((button_image.width*2, button_image.height*2)))

button_pressed_image = Image.open(button_pressed_image_path).convert("RGBA")
button_pressed_photo = ImageTk.PhotoImage(button_pressed_image.resize((button_pressed_image.width*2, button_pressed_image.height*2)))

# Funkce pro zpracování kliknutí na tlačítka
def on_button_click_1(event):
    print("Button 1 clicked")

def on_button_click_2(event):
    print("Button 2 clicked")

def on_button_click_3(event):
    print("Button 1 clicked")

def on_button_click_4(event):
    print("Button 2 clicked")    

# Funkce pro stisknutí tlačítka
def on_button_press_1(event):
    canvas.itemconfig(button_1, image=button_plain_pressed_photo)
    canvas.move(button_1, 2, 2)  # Mírný posun tlačítka při stisknutí

def on_button_release_1(event):
    canvas.itemconfig(button_1, image=button_plain_photo)
    canvas.move(button_1, -2, -2)  # Posun zpět při uvolnění
    on_button_click_1(event)

def on_button_press_2(event):
    canvas.itemconfig(button_2, image=button_pressed_photo)
    canvas.move(button_2, 2, 2)  # Mírný posun tlačítka při stisknutí

def on_button_release_2(event):
    canvas.itemconfig(button_2, image=button_photo)
    canvas.move(button_2, -2, -2)  # Posun zpět při uvolnění
    on_button_click_2(event)

def on_button_press_3(event):
    canvas.itemconfig(button_3, image=button_plain_pressed_photo)
    canvas.move(button_3, 4, 4)  # Mírný posun tlačítka při stisknutí

def on_button_release_3(event):
    canvas.itemconfig(button_3, image=button_plain_photo)
    canvas.move(button_3, -4, -4)  # Posun zpět při uvolnění
    on_button_click_2(event)

def on_button_press_4(event):
    canvas.itemconfig(button_4, image=button_pressed_photo)
    canvas.move(button_4, 4, 4)  # Mírný posun tlačítka při stisknutí

def on_button_release_4(event):
    canvas.itemconfig(button_4, image=button_photo)
    canvas.move(button_4, -4, -4)  # Posun zpět při uvolnění
    on_button_click_2(event)

# Vytvoření tlačítek jako obrázky na canvasu
button_1 = canvas.create_image(250, 187, image=button_plain_photo, anchor="center")
button_2 = canvas.create_image(250, 562, image=button_photo, anchor="center")
button_3 = canvas.create_image(750, 187, image=button_plain_photo, anchor="center")
button_4 = canvas.create_image(750, 562, image=button_photo, anchor="center")

# Bind událostí pro tlačítka
canvas.tag_bind(button_1, "<Button-1>", on_button_press_1)
canvas.tag_bind(button_1, "<ButtonRelease-1>", on_button_release_1)

canvas.tag_bind(button_2, "<Button-1>", on_button_press_2)
canvas.tag_bind(button_2, "<ButtonRelease-1>", on_button_release_2)

canvas.tag_bind(button_3, "<Button-1>", on_button_press_3)
canvas.tag_bind(button_3, "<ButtonRelease-1>", on_button_release_3)

canvas.tag_bind(button_4, "<Button-1>", on_button_press_4)
canvas.tag_bind(button_4, "<ButtonRelease-1>", on_button_release_4)

# Spuštění hlavní smyčky aplikace
root.mainloop()
