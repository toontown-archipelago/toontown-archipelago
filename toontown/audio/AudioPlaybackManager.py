class AudioPlaybackManager:
     
     def __init__(self, musicManager):
        self.musicManager = musicManager
        self.currentSong = None

     def playSong(self, song, looping = 0, interrupt = 1, volume = None, time = 0.0):
        """
        Plays a song by song object
        """
        self.currentSong = song
        base.playMusic(self.currentSong, looping = looping, volume = volume, time = time)
    


     def getSong(self):
        """
        Returns the current song
        """
        return self.currentSong
    
     def getTime(self):
        """
        Returns the current time of the song
        """
        return self.currentSong.getTime()
     
     def setTime(self, time):
        """
        Sets the time of the current song
        """
        self.currentSong.setTime(time)
