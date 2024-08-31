from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #zobrazení grafu v tkinteru
import tkinter as tk
import numpy as np
import pandas as pd

# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
fig, ax = plt.subplots(figsize=(7.04, 4.6), dpi=100) # 704x460 pixelů
 
# Tkinter Application
frame = tk.Frame(root)
label = tk.Label(text = "Matplotlib + Tkinter!")
label.config(font=("Courier", 32))
label.pack()

# Nacteni dat z csv
data_do_grafu = pd.read_csv('/home/pi/Petr/measuring_gears/BigGUI/build/csv/Test_csv_1.csv')
data_do_grafu.head()
t = data_do_grafu.iloc[:, 0]
uhel1 = data_do_grafu.iloc[:, 1]
uhel2 = data_do_grafu.iloc[:, 2]

# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.pack(anchor="center", fill=tk.X)

frame.pack() 
# Plot data on Matplotlib Figure
# t = np.arange(0, 2*np.pi, .01)
# ax.plot(t, np.sin(t))
ax.plot(t, uhel1, label='Úhel 1')
ax.plot(t, uhel2, label='Úhel 2')
ax.set_xlabel('Čas [s]')
ax.set_ylabel('Úhel [°]')
ax.legend()
canvas.draw()
 
root.mainloop()