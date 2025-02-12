from toontown.toonbase import ToontownGlobals
from panda3d.core import DecalEffect, VirtualFileSystem
import json


class MusicManager:

    def __init__(self):
        fileSystem = VirtualFileSystem.getGlobalPtr()
        self.musicJson = json.loads(fileSystem.readFile(ToontownGlobals.musicJsonFilePath, True))
        self.currentMusic = {}
        self.currentMusicInfo = {}

    
    def playMusic(self, json_code, looping=True, volume=1.0, interrupt=True, time=0.0):
        """
        Play a music track from the music json file.
        :param json_code: The json code for the music track.
        :param looping: Whether the music should loop.
        :param volume: The volume of the music.
        :param interrupt: Whether to interrupt the current music.
        :param time: The time to start the music at.
        """
        # we've got music and we're interrupting, kill
        if self.currentMusic and interrupt:
            self.stopMusic()
        if json_code in self.musicJson['global_music']:
            json_code_path = self.musicJson['global_music'][json_code]
            self.currentMusic[json_code] = base.loader.loadMusic(json_code_path)
            self.currentMusic[json_code].setLoop(looping)
            self.currentMusic[json_code].setVolume(volume)
            self.currentMusic[json_code].setTime(time)
            self.currentMusicInfo[json_code] = {"looping": looping, "volume": volume, "interrupt": interrupt, 
                                                 "time": time}
            base.playMusic(self.currentMusic[json_code], looping=looping, interrupt=interrupt, volume=volume, time=time
                            )
    def stopMusic(self):        
        for music in list(self.currentMusic.keys()):
            self.currentMusic[music].stop()
        self.currentMusic = {}
        self.currentMusicInfo = {}

    def stopSpecificMusic(self, json_code):
        if json_code in list(self.currentMusic.keys()):
            self.currentMusic[json_code].stop()
            # using pop just incase we try to stop a specific music that isn't in the dict
            self.currentMusic.pop(json_code, None)
            self.currentMusicInfo.pop(json_code, None)

    def setVolume(self, volume=1.0):
        for music in list(self.currentMusic.keys()):
            self.currentMusic[music].setVolume(volume)
            self.currentMusicInfo[music]["volume"] = volume

    def setSpecificVolume(self, json_code, volume=1.0):
        if json_code in list(self.currentMusic.keys()):
            self.currentMusic[json_code].setVolume(volume)
            self.currentMusicInfo[json_code]["volume"] = volume

    def getTime(self, json_code):
        return self.currentMusicInfo[json_code]["time"]
        
    def getCurMusic(self):
        return self.currentMusic
    
    def getCurMusicInfo(self):
        return self.currentMusicInfo