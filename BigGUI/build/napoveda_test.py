import tkinter as tk

# Seznam konkrétních zpráv
messages = [
    "První zpráva",
    "Druhá zpráva",
    "Třetí zpráva",
    "Čtvrtá zpráva",
    "Pátá zpráva",
    "Šestá zpráva",
    "Sedmá zpráva",
    "Osmá zpráva",
    "Devátá zpráva",
    "Desátá zpráva",
    "Jedenáctá zpráva",
    "Dvanáctá zpráva"
]
current_message_index = 0

# Funkce pro zobrazení další zprávy
def show_next_message():
    global current_message_index
    current_message_index = (current_message_index + 1) % len(messages)
    message_label.config(text=messages[current_message_index])

# Vytvoření hlavního okna
window = tk.Tk()
window.title("Zobrazovač zpráv")

# Vytvoření textového pole
message_label = tk.Label(window, text=messages[current_message_index], font=("Helvetica", 16))
message_label.pack(pady=20)

# Vytvoření tlačítka
next_button = tk.Button(window, text="Další zpráva", command=show_next_message)
next_button.pack(pady=20)

# Spuštění hlavní smyčky
window.mainloop()