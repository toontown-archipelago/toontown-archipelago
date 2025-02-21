from toontown.toonbase import ToontownGlobals
from panda3d.core import DecalEffect, VirtualFileSystem
import json
import random

class MusicManager:

    def __init__(self):
        fileSystem = VirtualFileSystem.getGlobalPtr()
        self.musicJson = json.loads(fileSystem.readFile(ToontownGlobals.musicJsonFilePath, True))
        self.currentMusic = {}
        self.currentMusicInfo = {}
        self.randomMusicInfo = {}
        self.storedMusicInfo = {}
    
    def playMusic(self, json_code, looping=True, volume=1.0, interrupt=True, time=0.0, refresh=False):
        """
        Play a music track from the music json file.
        :param json_code: The json code for the music track.
        :param looping: Whether the music should loop.
        :param volume: The volume of the music.
        :param interrupt: Whether to interrupt the current music.
        :param time: The time to start the music at.
        """
        old_code = json_code
        # we've got music and we're interrupting, kill
        if self.currentMusic and interrupt:
            self.stopMusic()
        if json_code in list(self.randomMusicInfo.keys()) and base.randomMusic and not refresh:
            json_code = self.randomMusicInfo[json_code]
            # Storing the info for normal music for an area, so we have reference when disabling music rando
            self.storedMusicInfo = {}
            self.storedMusicInfo[old_code] = {"looping": looping, "volume": volume, "interrupt": interrupt,
                                                "time": time}
        if json_code in self.musicJson['global_music']:
            json_code_path = random.choice(self.musicJson['global_music'][json_code])
            self.currentMusic[json_code] = base.loader.loadMusic(json_code_path)
            self.currentMusic[json_code].setLoop(looping)
            self.currentMusic[json_code].setVolume(volume)
            self.currentMusic[json_code].setTime(time)
            self.currentMusicInfo[json_code] = {"looping": looping, "volume": volume, "interrupt": interrupt, 
                                                 "time": time}
            base.playMusic(self.currentMusic[json_code], looping=looping, interrupt=interrupt, volume=volume, time=time
                            )

    # Used when we are disabling music randomizer
    def getNormalMusicInfo(self):
        if self.storedMusicInfo:
            return self.storedMusicInfo
        return None

    # Used on launch to set random music for the session
    def setRandomizedMusic(self):
        music_keys = list(self.musicJson['global_music'].keys())
        music_keys_copy = music_keys.copy()
        for key in music_keys:
            new_key = random.choice(music_keys_copy)
            music_keys_copy.remove(new_key)
            self.randomMusicInfo[key] = new_key

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
        # We need to update the current time for this music
        self.updateTime(json_code)
        return self.currentMusicInfo[json_code]["time"]

    def updateTime(self, json_code):
        self.currentMusicInfo[json_code]["time"] = self.currentMusic[json_code].getTime()
        
    def getCurMusic(self):
        return self.currentMusic
    
    def getCurMusicInfo(self):
        # We need to update the current times for all music
        for code in list(self.currentMusicInfo.keys()):
            self.updateTime(code)
        return self.currentMusicInfo
    
    def setLoop(self, value):
        """
        Set the looping value for all current music tracks.
        
        :param value: The value to set.
        """
        for music in list(self.currentMusic.keys()):
            self.currentMusic[music].setLoop(value)
            self.currentMusicInfo[music]["looping"] = value
    
    def setSpecificLoop(self, json_code, value):
        """
        Set the looping value for a specific music track.
        
        :param json_code: The json code for the music track.
        :param value: The value to set.
        """
        if json_code in list(self.currentMusic.keys()):
            self.currentMusic[json_code].setLoop(value)
            self.currentMusicInfo[json_code]["looping"] = value            
            
    def getVolume(self):
        """
        Retrieve the volume of the current music track.
        """
        return self.currentMusic[list(self.currentMusic.keys())[0]].getVolume()
    
    def getSpecifcVolume(self, json_code):
        """
        Get the volume of a specific music track.
        
        :param json_code: The json code for the music track.
        """
        if json_code in list(self.currentMusic.keys()):
            return self.currentMusic[json_code].getVolume()
        return None
    
    def getSpecifcPlayRate(self, json_code):
        """
        Get the play rate of a specific music track.
        
        :param json_code: The json code for the music track.
        """
        if json_code in list(self.currentMusic.keys()):
            return self.currentMusic[json_code].getPlayRate()
        return None

            
    def setSpecifcPlayRate(self, json_code, rate):
        """
        Set the play rate of a specific music track.
        """
        if json_code in list(self.currentMusic.keys()):
            self.currentMusic[json_code].setPlayRate(rate)
            self.currentMusicInfo[json_code]["rate"] = rate
            
    
    def setPlayRate(self, rate):
        """
        Set the play rate of the current music.
        """
        for music in list(self.currentMusic.keys()):
            self.currentMusic[music].setPlayRate(rate)
            self.currentMusicInfo[music]["rate"] = rate