import json
from .Audio import audio


class AudioStoring:

    def __init__(self, file, uid):
        self.file = file
        self.uid = str(uid)
        self.list_obj = []
        volumeFile = open("./database/sound-volume.txt", "r")
        self.volume = int(volumeFile.readline())
        self.audio = audio

    def store(self):

        audio = {self.uid: self.file}

        with open("./audio/audioStorage.json") as file:

            self.list_obj = json.load(file)
        
        if len(self.list_obj["audioFiles"]) > 0:
            for item in self.list_obj["audioFiles"]:
                print(item)
                if item.get(self.uid):
                    item[self.uid] = self.file
                    break
                else:
                    self.list_obj["audioFiles"].append(audio)
                    break
        else:
            self.list_obj["audioFiles"].append(audio)

        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))


    def deleteAudio(self):
        if self.uid == 4:
            self.audio.play_audio("audio/systemAudio/nothingToDelete.ogg", self.volume)
            return 
        with open("./audio/audioStorage.json") as file:

            self.list_obj = json.load(file)
        print(self.list_obj["audioFiles"])
        if len(self.list_obj["audioFiles"]) > 0:
            itemFound = False
            for item in self.list_obj["audioFiles"]:
                if item.get(self.uid):
                    index = self.list_obj["audioFiles"].index(item)
                    del self.list_obj["audioFiles"][index]
                    self.audio.play_audio("audio/systemAudio/validation.ogg", self.volume)
                    itemFound = True
                    break
            if itemFound == False:
                print("no mess del")
                self.audio.play_audio("audio/systemAudio/nothingToDelete.ogg", self.volume)
                
        with open("./audio/audioStorage.json", "w") as file:
            json.dump(self.list_obj, file, indent=4, separators=(',', ': '))

        
        
# Uncomment to run tests
#audio_storing = AudioStoring("./audio/audioFiles/audio.ogg", 4)
#audio_storing.store()
#audio_storing.delete()