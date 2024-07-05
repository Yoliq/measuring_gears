import serial
import tkinter as tk

#figmatoken: figd_9zMnAuskM_Nu-mnWiezHgeIjzcNbLR7LN1cmSLr_

ser = serial.Serial('COM6', 9600)  # Upravte COM6 podle vašeho připojení

def send_command(command):
    ser.write(command.encode() + b'\n')

def forward(event):
    send_command('FORWARD')

def backward(event):
    send_command('BACKWARD')

def stop(event):
    send_command('STOP')

root = tk.Tk()
root.title("Motor Control")

forward_button = tk.Button(root, text="Dopředu")
forward_button.pack(fill=tk.BOTH, expand=True)
forward_button.bind("<ButtonPress>", forward)
forward_button.bind("<ButtonRelease>", stop)

backward_button = tk.Button(root, text="Dozadu")
backward_button.pack(fill=tk.BOTH, expand=True)
backward_button.bind("<ButtonPress>", backward)
backward_button.bind("<ButtonRelease>", stop)

root.mainloop()
