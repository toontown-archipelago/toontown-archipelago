from toontown.toonbase import ToontownGlobals
from panda3d.core import DecalEffect, VirtualFileSystem
import json


class MusicManager:

    def __init__(self):
        fileSystem = VirtualFileSystem.getGlobalPtr()
        self.musicJson = json.loads(fileSystem.readFile(ToontownGlobals.musicJsonFilePath, True))
        self.currentMusic = {}
    
    def playMusic(self, json_code, looping=True, volume=1.0, interrupt=True):
        # we've got music and we're interrupting, kill
        if self.currentMusic and interrupt:
            self.stopMusic()
        if json_code in self.musicJson['global_music']:
            json_code_path = self.musicJson['global_music'][json_code]
            self.currentMusic[json_code] = base.loader.loadMusic(json_code_path)
            self.currentMusic[json_code].setLoop(looping)
            self.currentMusic[json_code].setVolume(volume)
            if interrupt:
                self.currentMusic[json_code].play()
    
    def stopMusic(self):        
        for music in list(self.currentMusic.keys()):
            self.currentMusic[music].stop()
        self.currentMusic = {}

    def stopSpecificMusic(self, json_code):
        if json_code in list(self.currentMusic.keys()):
            self.currentMusic[json_code].stop()
            # using pop just incase we try to stop a specific music that isn't in the dict
            self.currentMusic.pop(json_code, None)

    def setVolume(self, volume=1.0):
        for music in list(self.currentMusic.keys()):
            self.currentMusic[music].setVolume(volume)

    def setSpecificVolume(self, json_code, volume=1.0):
        if json_code in list(self.currentMusic.keys()):
            self.currentMusic[json_code].setVolume(volume)