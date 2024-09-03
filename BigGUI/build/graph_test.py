from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #zobrazení grafu v tkinteru
import tkinter as tk
from tkinter import Tk, Canvas
import numpy as np
import pandas as pd

# Initialize Tkinter and Matplotlib Figure
window = Tk()
window.geometry("2560x1440")
window.configure(bg='gray')
# Create Canvas
canvas = Canvas(
    window,
    bg="gray",
    height=1440,
    width=2560,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
x_dpi=20
y_dpi=12
w_g=x_dpi*100
h_g=y_dpi*100
x_g=280
y_g=50

# Nacteni dat z csv
data_do_grafu = pd.read_csv('/home/pi/Petr/measuring_gears/BigGUI/build/csv/Test_meření2_2-9.csv')
data_do_grafu.head()
t = data_do_grafu.iloc[:, 0]
uhel1 = data_do_grafu.iloc[:, 1]
uhel2 = data_do_grafu.iloc[:, 2]

fig, ax = plt.subplots(figsize=(x_dpi, y_dpi), dpi=100, tight_layout=True) # 704x460 pixelů
graf_canvas = FigureCanvasTkAgg(fig, master=window)  
graf = graf_canvas.get_tk_widget()
graf.place(x=x_g, y=y_g, width=w_g, height=h_g)

toolbar = NavigationToolbar2Tk(graf_canvas, window, pack_toolbar=False)
toolbar.update()
toolbar.place(x=x_g, y=y_g+h_g, width=w_g, height=30)

ax.plot(t, uhel1, label='Úhel 1')
#ax.plot(t, uhel2, label='Úhel 2')
ax.set_xlabel('Čas [s]')
ax.set_ylabel('Úhel [°]')
ax.legend()
graf_canvas.draw()
 
window.mainloop()