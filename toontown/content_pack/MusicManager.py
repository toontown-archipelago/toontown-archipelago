from toontown.toonbase import ToontownGlobals
from panda3d.core import DecalEffect, VirtualFileSystem
from direct.interval.IntervalGlobal import *
import json
import random

class MusicManager:

    def __init__(self):
        fileSystem = VirtualFileSystem.getGlobalPtr()
        self.musicJson = json.loads(fileSystem.readFile(ToontownGlobals.musicJsonFilePath, True))
        self.previousMusic = None
        self.currentMusic = {}
        self.currentMusicInfo = {}
        self.randomMusicInfo = {}
        self.storedMusicInfo = {}
        self.lastPlayedTrack = {}
    
    def playMusic(self, json_code, looping=True, volume=1.0, interrupt=True, time=0.0, refresh=False, randomToggle=False):
        if self.previousMusic == json_code and not randomToggle:
            return
        if self.currentMusic and interrupt:
            self.stopMusic()
        possible_paths = self.musicJson.get('global_music', {}).get(json_code, [])
        self.storedMusicInfo = {
            json_code: {"looping": looping, "volume": volume, "interrupt": interrupt, "time": time, "path": possible_paths}
        }
        self.previousMusic = json_code
        if getattr(base, 'randomMusic', False):
            pool = self._getTrackPool()
            allowed_tracks = [t for t in pool if t != self.lastPlayedTrack.get(json_code)]
            if not allowed_tracks:
                allowed_tracks = pool
            json_code_path = random.choice(allowed_tracks)
            self.lastPlayedTrack[json_code] = json_code_path
        else:
            if possible_paths:
                json_code_path = random.choice(possible_paths)
            else:
                return
        self.currentMusic[json_code] = base.loader.loadMusic(json_code_path)
        self.currentMusic[json_code].setLoop(looping)
        self.currentMusic[json_code].setVolume(volume)
        self.currentMusic[json_code].setTime(time)
        self.currentMusicInfo[json_code] = {"looping": looping, "volume": volume, "interrupt": interrupt, "time": time, "path": [json_code_path]}
        base.playMusic(self.currentMusic[json_code], looping=looping, interrupt=interrupt, volume=volume, time=time)
        if getattr(base, 'randomMusic', False):
            track_name = self._getTrackName(json_code_path)
            if getattr(base, 'localAvatar', None):
                from toontown.archipelago.definitions import color_profile
                from libotp.nametag.WhisperGlobals import WhisperType
                base.localAvatar.displayWhisper(0, "Now Playing: " + track_name, WhisperType.WTSystem, colorProfileOverride=color_profile.PURPLE)

    def _getTrackPool(self):
        in_game_paths = []
        for paths in self.musicJson.get('global_music', {}).values():
            for p in paths:
                if p not in in_game_paths:
                    in_game_paths.append(p)
        import os
        custom_paths = []
        custom_dir = "resources/custom_music"
        if os.path.exists(custom_dir):
            try:
                for f in os.listdir(custom_dir):
                    if f.lower().endswith((".ogg", ".mp3", ".wav", ".flac", ".wma", ".aac", ".m4a", ".opus")):
                        custom_paths.append(os.path.join(custom_dir, f).replace("\\", "/"))
            except Exception:
                pass
        style = getattr(base, 'randomMusicStyle', 'Mix')
        if style == 'Custom Only':
            if custom_paths:
                return custom_paths
            return in_game_paths
        elif style == 'Mix':
            return custom_paths + in_game_paths
        else:
            return in_game_paths

    def _getTrackName(self, track_path):
        title = self._getAudioTitle(track_path)
        if title:
            return title
        import os
        filename = os.path.basename(track_path)
        name_without_ext = os.path.splitext(filename)[0]
        return name_without_ext.replace('_', ' ').replace('-', ' ').strip().title()

    def _getAudioTitle(self, file_path):
        import os
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.ogg', '.flac'):
            return self._getOggTitle(file_path)
        elif ext == '.mp3':
            return self._getMp3Title(file_path)
        return None

    def _getMp3Title(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read(16384)
            idx = data.find(b'TIT2')
            if idx != -1:
                if len(data) >= idx + 11:
                    size_bytes = data[idx+4:idx+8]
                    frame_size = int.from_bytes(size_bytes, byteorder='big')
                    if 0 < frame_size < 1024:
                        encoding = data[idx+10]
                        raw_bytes = data[idx+11 : idx+11+frame_size-1]
                        if encoding == 0:
                            title = raw_bytes.decode('iso-8859-1', errors='ignore')
                        elif encoding == 1:
                            title = raw_bytes.decode('utf-16', errors='ignore')
                        elif encoding == 2:
                            title = raw_bytes.decode('utf-16-be', errors='ignore')
                        elif encoding == 3:
                            title = raw_bytes.decode('utf-8', errors='ignore')
                        else:
                            title = raw_bytes.decode('utf-8', errors='ignore')
                        title = title.replace('\x00', '').strip()
                        if title:
                            return title
            with open(file_path, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                if file_size >= 128:
                    f.seek(-128, 2)
                    tag = f.read(3)
                    if tag == b'TAG':
                        title_bytes = f.read(30)
                        title = title_bytes.decode('iso-8859-1', errors='ignore').replace('\x00', '').strip()
                        if title:
                            return title
        except Exception:
            pass
        return None

    def _getOggTitle(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read(16384)
            idx = data.lower().find(b'title=')
            if idx != -1:
                start = idx + 6
                title_bytes = bytearray()
                for i in range(start, min(start + 128, len(data))):
                    b = data[i]
                    if 32 <= b <= 126 or b >= 128:
                        title_bytes.append(b)
                    else:
                        break
                title_str = title_bytes.decode('utf-8', errors='ignore').strip()
                if title_str:
                    return title_str
        except Exception:
            pass
        return None

    # Used when we are disabling music randomizer
    def getNormalMusicInfo(self):
        if self.storedMusicInfo:
            return self.storedMusicInfo
        return None

    def setRandomizedMusic(self):
        self.lastPlayedTrack = {}

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

    def lerpPlayRate(self, json_key, to_data, duration):
        self.currentMusicInfo[json_key]["rate"] = to_data
        return LerpFunctionInterval(self.currentMusic[json_key].setPlayRate, fromData=self.getSpecifcPlayRate(json_key), toData=to_data, duration=duration)

    def lerpVolume(self, json_key, to_data, duration):
        self.currentMusicInfo[json_key]["volume"] = to_data
        return LerpFunctionInterval(self.currentMusic[json_key].setVolume, fromData=self.getVolume(), toData=to_data, duration=duration)