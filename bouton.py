import time
import websocket
import os
import RPi.GPIO as GPIO
from classes.ProtocolBuilder import ProtocolBuilder
from classes.Micro import Micro
from classes.Audio import Audio
from datetime import datetime
from classes.ButtonRec import ButtonRec

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print(GPIO.input(17))
ws = websocket.create_connection("ws://localhost:8080")

micro = Micro()
audio = Audio()
buttonRec = ButtonRec()
DelMode = False
deleteTime = datetime.now()
saveMode = False
recTime = datetime.now()

while True:
    volume = 100
    volumeFile = open("./database/sound-volume.txt", "r")
    volumeLine = volumeFile.readline()
    if isinstance(volumeLine, str):
            if volumeLine != "":
                volumeFile.seek(0)
                volume = int(volumeLine)
    time_now = datetime.now() - deleteTime
    if int(time_now.total_seconds()) > 5:
        DelMode = False
    # Takes photo
    if GPIO.input(17) == GPIO.HIGH:
        print("pushed")
        protocol = ProtocolBuilder("button17", "HIGH")
        ws.send(protocol.buildProtocol())
        time.sleep(2)

    # Start audio recording
    if GPIO.input(18) == GPIO.HIGH:
        if (saveMode):
            delta = datetime.now() - recTime
            if int(delta.total_seconds()) > 0.20:
                protocol = ProtocolBuilder("button18", "on")
                ws.send(protocol.buildProtocol())
                saveMode = False
                while GPIO.input(18) == GPIO.HIGH:
                    time.sleep(0.1)
        else:
            saveMode = True
            recTime = datetime.now()

    # Stops audio recording
    if GPIO.input(18) == GPIO.LOW:
        if saveMode:
            print("lezgo")
            saveMode = False
            protocol = ProtocolBuilder("button18", "shortClick")
            ws.send(protocol.buildProtocol()) 
        else:
            protocol = ProtocolBuilder("button18", "off")
            ws.send(protocol.buildProtocol()) 

    # Delete audio file
    if GPIO.input(4) == GPIO.HIGH:
        if DelMode:
            print("pushed")
            protocol = ProtocolBuilder("button4", "HIGH")
            ws.send(protocol.buildProtocol())
            time.sleep(2)
            DelMode = False
        else:
            protocol = ProtocolBuilder("button4", "1")
            ws.send(protocol.buildProtocol())
            DelMode = True
            deleteTime = datetime.now()
            time.sleep(0.2)

    time.sleep(0.2)
    