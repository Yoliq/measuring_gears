import time
import serial

arduinoData=serial.Serial('com6',230400)
time.sleep(1)

while True:
    while (arduinoData.inWaiting()==0): #čeká na data z arduina
        pass
    dataPacket=arduinoData.readline()   #přečte data z arduina 
    dataPacket=str(dataPacket, 'utf-8') #ořeže bordel z arduina jen na zprávu 
    dataPacket=dataPacket.strip('\r\n') #smaže mezeru mezi řádky 
    splitPacket=dataPacket.split(",")   #rozdělí textový data z arduina podle čárek a udělá z toho čísla 
    x=float(splitPacket[0])             #vytvoří proměnnou x z první pozice spliPacket
    y=float(splitPacket[1])
    z=float(splitPacket[2])
    print("X= ",x, "Y=",y,"Z=",z)       #zobrazí data z arduina


