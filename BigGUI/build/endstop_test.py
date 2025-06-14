from gpiozero import Button
from signal import pause

button = Button(12)  # nahraď 17 za reálný GPIO pin
button.when_pressed = lambda: print("Pressed!")

pause()
