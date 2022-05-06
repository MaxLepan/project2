from datetime import datetime
import os
from time import time
from simple_websocket_server import WebSocketServer, WebSocket
from classes.ProtocolReader import ProtocolReader
from classes.AudioStoring import AudioStoring
from classes.ButtonRec import ButtonRec
from classes.ButtonDelete import ButtonDelete
from classes.ButtonCamera import ButtonCamera


class Stockage:

    def __init__(self):
        self.pattern = 0
        self.mode = 1,
        self.volume = 100


class SimpleEcho(WebSocket):

    stockage = Stockage()
    buttonRec = ButtonRec()
    buttonDelete = ButtonDelete()
    buttonCamera = ButtonCamera("./img/photo_analyse.png")
    patternSaved = False
    recMode = False 
    
    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        modeFile = open("./database/mode.txt", "r")
        SimpleEcho.stockage.mode = int(modeFile.readline())
        volumeFile = open("./database/sound-volume.txt", "r")
        SimpleEcho.stockage.volume = int(volumeFile.readline())

        print(SimpleEcho.stockage.mode)
        # Takes photoAudio
        if sensor == "button17":
            SimpleEcho.buttonCamera.action(SimpleEcho.stockage.mode)
            SimpleEcho.stockage.pattern = ButtonCamera.pattern            
            print(SimpleEcho.stockage.pattern)
            SimpleEcho.patternSaved = True

        # Send pattern to save message
        elif sensor == "button18":
            
            if value == "on":
                if (SimpleEcho.patternSaved):
                    SimpleEcho.buttonRec.action_button_on(SimpleEcho.stockage.mode, SimpleEcho.stockage.pattern)
                else:
                    os.system(f"play -v {SimpleEcho.stockage.volume/100} audio/systemAudio/claque.ogg")
            if value == "off":
                SimpleEcho.buttonRec.action_button_off(SimpleEcho.stockage.mode)

        # Deletes audio file
        elif sensor == "button4":
            if (SimpleEcho.patternSaved):
                SimpleEcho.buttonDelete.action(SimpleEcho.stockage.mode, SimpleEcho.stockage.pattern)
            else:
                os.system(f"play -v {SimpleEcho.stockage.volume/100} audio/systemAudio/claque.ogg")
            print("button4")
        
    def connected(self):
        print(self.address, 'connected')
        #SimpleEcho.volumeControl.start()
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8080, SimpleEcho)
print("server online")
server.serve_forever()

# button = subprocess.Popen(["python", "bouton.py"])
# print("All online")