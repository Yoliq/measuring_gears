
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\danie\Documents\Robotwin - Python\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    21.0,
    576.0,
    384.0,
    685.0,
    fill="#D9D9D9",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    492.0,
    477.0,
    image=image_image_1
)

canvas.create_rectangle(
    486.0,
    458.0000024087358,
    604.9999939544578,
    641.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    97.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    590.0,
    25.0,
    721.0,
    73.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    758.0,
    25.0,
    861.0,
    73.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    871.0,
    25.0,
    924.0,
    73.0,
    fill="#000000",
    outline="")

canvas.create_text(
    21.0,
    0.0,
    anchor="nw",
    text="OVLÁDÁNÍ STAVU",
    fill="#000000",
    font=("RobotoRoman Bold", 48 * -1)
)

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
    x=21.0,
    y=128.0,
    width=207.0,
    height=130.0
)

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
    x=304.0,
    y=128.0,
    width=207.0,
    height=130.0
)

canvas.create_rectangle(
    263.9999932684457,
    191.0,
    266.0,
    347.0,
    fill="#D9D4AB",
    outline="")

canvas.create_rectangle(
    232.0,
    191.0,
    298.0,
    193.0,
    fill="#D9D4AB",
    outline="")

canvas.create_rectangle(
    232.0,
    309.0,
    266.0,
    311.0,
    fill="#D9D4AB",
    outline="")

canvas.create_rectangle(
    809.0,
    504.0,
    1022.0,
    599.0,
    fill="#BFBFBF",
    outline="")

canvas.create_rectangle(
    21.0,
    270.0,
    228.0,
    361.0,
    fill="#D9D4AB",
    outline="")

canvas.create_text(
    809.0,
    509.0,
    anchor="nw",
    text="Osová vzdálenost",
    fill="#393939",
    font=("RobotoRoman Bold", 24 * -1)
)

canvas.create_text(
    16.0,
    273.0,
    anchor="nw",
    text="Natočení motoru",
    fill="#393939",
    font=("RobotoRoman Bold", 24 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=941.0,
    y=548.0,
    width=45.0,
    height=45.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=54.0,
    y=304.0,
    width=45.0,
    height=45.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=838.0,
    y=548.0,
    width=45.0,
    height=45.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=325.0,
    y=623.0,
    width=45.0,
    height=45.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=151.0,
    y=304.0,
    width=45.0,
    height=45.0
)

canvas.create_rectangle(
    721.0,
    555.0,
    809.0,
    555.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    624.5603014464227,
    507.8981316272941,
    720.560302734375,
    554.8981323242188,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    558.0,
    168.0,
    681.0,
    214.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    424.0,
    639.0,
    547.0,
    685.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    558.0,
    279.0,
    681.0,
    325.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    558.0,
    168.0,
    681.0,
    214.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    424.0,
    639.0,
    547.0,
    685.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    558.0,
    279.0,
    699.0,
    325.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    687.0,
    186.0,
    758.0,
    214.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    558.0,
    128.0,
    593.0,
    163.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    568.0,
    171.0,
    anchor="nw",
    text="Natočení páky",
    fill="#000000",
    font=("RobotoRoman Bold", 16 * -1)
)

canvas.create_text(
    434.0,
    642.0,
    anchor="nw",
    text="Natočení kola",
    fill="#000000",
    font=("RobotoRoman Bold", 16 * -1)
)

canvas.create_text(
    568.0,
    282.0,
    anchor="nw",
    text="Hmotnost záváží",
    fill="#000000",
    font=("RobotoRoman Bold", 16 * -1)
)

canvas.create_text(
    694.0,
    190.0,
    anchor="nw",
    text="Nulovat",
    fill="#000000",
    font=("RobotoRoman Bold", 16 * -1)
)

canvas.create_rectangle(
    568.0,
    192.0,
    597.0,
    210.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    434.0,
    663.0,
    463.0,
    681.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    568.0,
    303.0,
    644.0,
    321.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    600.0,
    193.0,
    anchor="nw",
    text="°",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_text(
    466.0,
    664.0,
    anchor="nw",
    text="°",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_text(
    645.0,
    304.0,
    anchor="nw",
    text="[kg]",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_rectangle(
    524.0,
    191.0,
    524.0000079991847,
    374.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    687.0,
    373.9999998211533,
    717.0,
    374.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    558.0,
    219.0,
    681.0,
    245.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    558.0,
    219.0,
    681.0,
    245.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    568.0,
    223.0,
    597.0,
    241.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    600.0,
    224.0,
    anchor="nw",
    text="°",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=1083.0,
    y=16.0,
    width=177.0,
    height=66.0
)

canvas.create_rectangle(
    590.0,
    25.0,
    748.0,
    73.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    879.0,
    30.0,
    917.0,
    68.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    566.0,
    136.0,
    586.0,
    156.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1025.0,
    504.0,
    1148.0,
    550.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    809.0,
    602.0,
    932.0,
    648.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    1025.0,
    553.0,
    1148.0,
    599.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    1025.0,
    504.0,
    1238.0,
    550.0,
    fill="#BFBFBF",
    outline="")

canvas.create_rectangle(
    809.0,
    602.0,
    1022.0,
    648.0,
    fill="#BFBFBF",
    outline="")

canvas.create_rectangle(
    1025.0,
    553.0,
    1238.0,
    599.0,
    fill="#BFBFBF",
    outline="")

canvas.create_text(
    1034.0,
    505.0,
    anchor="nw",
    text="Vzdálenost (lankový snímač)",
    fill="#000000",
    font=("RobotoRoman Bold", 15 * -1)
)

canvas.create_text(
    818.0,
    603.0,
    anchor="nw",
    text="Zadej osovou vzdálenost",
    fill="#000000",
    font=("RobotoRoman Bold", 15 * -1)
)

canvas.create_text(
    1034.0,
    554.0,
    anchor="nw",
    text="Vzdálenost (laserový snímač)",
    fill="#000000",
    font=("RobotoRoman Bold", 15 * -1)
)

canvas.create_rectangle(
    1035.0,
    528.0,
    1111.0,
    546.0,
    fill="#BFBFBF",
    outline="")

canvas.create_rectangle(
    819.0,
    626.0,
    895.0,
    644.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1035.0,
    577.0,
    1111.0,
    595.0,
    fill="#BFBFBF",
    outline="")

canvas.create_text(
    1112.0,
    529.0,
    anchor="nw",
    text="mm",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_text(
    896.0,
    627.0,
    anchor="nw",
    text="[mm]",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_text(
    1112.0,
    578.0,
    anchor="nw",
    text="mm",
    fill="#000000",
    font=("RobotoRoman Regular", 16 * -1)
)

canvas.create_rectangle(
    374.0,
    188.99999618530273,
    442.0000020981468,
    237.0000029723744,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    90.99999790185319,
    188.9999970276256,
    159.0,
    237.00000381469727,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    162.0,
    317.99999809265137,
    186.00000078680506,
    336.0000010490733,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    64.99999921319493,
    317.9999989509267,
    89.0,
    336.00000190734863,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    838.0,
    114.0,
    1263.0,
    403.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    848.0,
    122.0,
    anchor="nw",
    text="GRAF (?)",
    fill="#000000",
    font=("RobotoRoman Bold", 24 * -1)
)

canvas.create_rectangle(
    521.0,
    189.0,
    558.0,
    191.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    684.0,
    302.0,
    718.0,
    304.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    714.0,
    301.0,
    716.0000031472202,
    375.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    848.0,
    151.0,
    1251.0,
    391.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    35.0,
    588.0,
    314.0,
    673.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
