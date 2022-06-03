import os

mode = 0
volume = 100

with open("./database/mode.txt", "r") as modeFile:
    modeLine = modeFile.readline()
    if isinstance(modeLine, str):
        if modeLine != "":
            mode = int(modeLine)

with open("./database/sound-volume.txt", "r") as volumeFile:
    volumeLine = volumeFile.readline()
    if isinstance(volumeLine, str):
        volumeFile.seek(0)
        if volumeLine != "":
            volumeFile.seek(0)
            volume = int(volumeLine)

if mode == 1:
    os.system(f"play -v {volume / 100} ./audio/systemAudio/start-mode-expert.ogg")
if mode == 2:
    os.system(f"play -v {volume / 100} ./audio/systemAudio/start-mode-intermediary.ogg")
if mode == 3:
    os.system(f"play -v {volume / 100} ./audio/systemAudio/start-mode-tutorial.ogg")