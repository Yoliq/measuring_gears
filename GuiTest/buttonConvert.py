import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def create_pressed_image(image):
    pressed_image = image.copy()
    pixels = pressed_image.load()

    for y in range(pressed_image.height):
        for x in range(pressed_image.width):
            r, g, b, a = pixels[x, y]
            r = int(r * 0.8)
            g = int(g * 0.8)
            b = int(b * 0.8)
            pixels[x, y] = (r, g, b, a)
    
    return pressed_image

def open_files():
    file_paths = filedialog.askopenfilenames(
        title="Vyberte obrázky",
        filetypes=[("PNG files", "*.png")])
    
    if file_paths:
        for file_path in file_paths:
            image = Image.open(file_path).convert("RGBA")
            pressed_image = create_pressed_image(image)
            
            base, ext = os.path.splitext(file_path)
            save_path = base + "_pressed" + ext
            pressed_image.save(save_path)
        
        messagebox.showinfo("Úspěch", f"Stisknuté verze obrázků byly uloženy.")

root = tk.Tk()
root.title("Generátor stisknutého efektu obrázku")

# Zvýšení velikosti okna
canvas = tk.Canvas(root, height=400, width=800, bg='#80c1ff')
canvas.pack()

frame = tk.Frame(root, bg='#80c1ff')
frame.place(relx=0.5, rely=0.5, anchor='center')

# Zvýšení velikosti textu a tlačítka
label = tk.Label(frame, text="Stiskněte tlačítko pro výběr obrázků k převodu", bg='#80c1ff', font=("Helvetica", 16))
label.pack(pady=20)

button = tk.Button(frame, text="Vybrat obrázky", command=open_files, font=("Helvetica", 16))
button.pack(pady=20)

root.mainloop()
