import os
from .Camera import Camera
from .AudioGetter import AudioGetter
from .Audio import Audio
from .AudioStoring import AudioStoring
from .ProtocolReader import ProtocolReader
from .Micro import Micro
import subprocess
import time


class ExpertMode:

    def __init__(self, file):
        self.camera = Camera(file)
        self.volume = 100
        self.micro = Micro()
        self.audio = Audio()
        self.recording = False

    def getVolume(self):
        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                self.volume = int(volumeLine)

    def action(self, button, patternSaved, pattern):
        protocol = ProtocolReader(button)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        self.getVolume()

        if sensor == "button18" and patternSaved:
            self.recButtonSend(value, pattern)
        if sensor == "button17":
            self.cameraButtonSend()
        if sensor == "button4" and patternSaved:
            self.delButtonSend(value, pattern)


    def recButtonSend(self, value, pattern):
        if value == "on":
            print("ui")
            audioGet = AudioGetter(pattern)
            audioFile = audioGet.get_audio()
            if "noMessageRecorded" in audioFile:
                self.recording = True
                self.getVolume()
                self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)
                self.micro.start_recording(pattern)
            else:
                self.getVolume()
                self.audio.play_audio("audio/systemAudio/claque.ogg", self.volume)
        elif value == "off" and self.recording:
            print("nope")
            self.micro.stop_recording()
            self.recording = False
            self.getVolume()
            self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)

    def delButtonSend(self):
        print("boo del")

    def cameraButtonSend(self):
        print("ici")
        led = subprocess.Popen(["python", "./led.py"])
        self.camera.take_photo()
        time.sleep(2)
        led.terminate()
        


""" expertMode = ExpertMode("boo.png")
expertMode.action("button17:on", False, 0)
expertMode.action("button18:on", True, 1)
expertMode.action("button18:off", True, 1)
 """