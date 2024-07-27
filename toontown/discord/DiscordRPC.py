import time 
from ctypes import *
from direct.task import Task 
from pypresence import Presence
from pypresence.exceptions import PyPresenceException
from direct.directnotify import DirectNotifyGlobal

clientId  = "1255381622128377998"
LOGO = "https://avatars.githubusercontent.com/u/164748629"

class DiscordRPC(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordRPC')
    zone2imgdesc = { # A dict of ZoneID -> An image and a description
        1000: ["https://static.wikia.nocookie.net/toontown/images/6/65/Donalds_Dock.png", "In Donald's Dock"],
        1100: ["https://static.wikia.nocookie.net/toontown/images/e/e7/Barnacle_Boulevard_Tunnel.jpg", "On Barnacle Boulevard"],
        1200: ["https://static.wikia.nocookie.net/toontown/images/9/91/Seaweed_Street_Tunnel.jpg", "On Seaweed Street"],
        1300: ["https://static.wikia.nocookie.net/toontown/images/0/06/Lighthouse_Lane_Tunnel.jpg", "On Lighthouse Lane"],

        2000: ["https://static.wikia.nocookie.net/toontown/images/9/93/Toontown_Central.png", "In Toontown Central"],
        2100: ["https://static.wikia.nocookie.net/toontown/images/4/40/Silly_Street_Tunnel.jpg", "On Silly Street"],
        2200: ["https://static.wikia.nocookie.net/toontown/images/9/98/Loopy_Lane_Tunnel.jpg", "On Loopy Lane"],
        2300: ["https://static.wikia.nocookie.net/toontown/images/c/cc/Punchline_Place_Tunnel.jpg", "On Punchline Place"],

        3000: ["https://static.wikia.nocookie.net/toontown/images/5/57/The_Brrrgh.png", "In The Brrrgh"],
        3100: ["https://static.wikia.nocookie.net/toontown/images/f/fd/Walrus_Way_Tunnel.jpg", "On Walrus Way"],
        3200: ["https://static.wikia.nocookie.net/toontown/images/3/35/Sleet_Street_Tunnel.jpg", "On Sleet Street"],
        3300: ["https://static.wikia.nocookie.net/toontown/images/e/e9/Polar_Place_Tunnel.jpg", "On Polar Place"],

        4000: ["https://static.wikia.nocookie.net/toontown/images/6/61/Minnies_Melodyland.png", "In Minnie's Melodyland"],
        4100: ["https://static.wikia.nocookie.net/toontown/images/d/d0/Alto_Avenue_Tunnel.jpg", "On Alto Avenue"],
        4200: ["https://static.wikia.nocookie.net/toontown/images/4/4c/Baritone_Boulevard_Tunnel.jpg/", "On Baritone Boulevard"],
        4300: ["https://static.wikia.nocookie.net/toontown/images/5/5e/Tenor_Terrace_Tunnel.jpg", "On Tenor Terrace"],

        5000: ["https://static.wikia.nocookie.net/toontownrewritten/images/8/81/Daisy_Gardens.jpg", "In Daisy Gardens"],
        5100: ["https://static.wikia.nocookie.net/toontown/images/d/dc/Elm_Street_Tunnel.jpg", "On Elm Street"],
        5200: ["https://static.wikia.nocookie.net/toontown/images/4/41/Maple_Street_Tunnel.jpg", "On Maple Street"],
        5300: ["https://static.wikia.nocookie.net/toontown/images/d/d3/Oak_Street_Tunnel.jpg", "On Oak Street"],

        6000: ["https://static.wikia.nocookie.net/toontown/images/8/88/Chip_n_Dales_Acorn_Acres.png", "At Chip 'n Dale's Acorn Acres"],


        8000: ["https://static.wikia.nocookie.net/toontownrewritten/images/1/10/Goofy_Speedway.png", "In Goofy Speedway"],

        9000: ["https://static.wikia.nocookie.net/toontown/images/9/9c/Donalds_Dreamland.png", "In Donald's Dreamland"],
        9100: ["https://static.wikia.nocookie.net/toontown/images/c/c7/Lullaby_Lane_Tunnel.jpg", "On Lullaby Lane"],
        9200: ["https://static.wikia.nocookie.net/toontown/images/e/ec/Pajama_Place_Tunnel.jpg", "On Pajama Place"],
        10000: ["https://static.wikia.nocookie.net/toontown/images/6/61/Bossbot_Headquarters.png", "At Bossbot HQ"],
        10100: ["https://static.wikia.nocookie.net/toontown/images/2/2b/Bossbot_Clubhouse.png", "In The CEO Clubhouse"],
        10200: ["https://static.wikia.nocookie.net/toontown/images/2/2b/Bossbot_Clubhouse.png", "In The CEO Clubhouse"],
        10500: ["https://static.wikia.nocookie.net/toontown/images/f/f6/Bbhqfrontthree.png", "In The Front One"],
        10600: ["https://www.toontowncentral.com/gallery/data/986/Middle_6.jpg", "In The Middle Two"],
        10700: ["https://i.ytimg.com/vi/DaMcp3S74lI/maxresdefault.jpg", "In The Back Three"],

        11000: ["https://static.wikia.nocookie.net/toontownrewritten/images/8/8a/Sellbot_Headquarters.jpg/", "At Sellbot HQ"],
        11100: ["https://static.wikia.nocookie.net/toontown/images/c/c0/SBHQ_lobby_1.jpg", "In The Sellbot HQ Lobby"],
        11200: ["https://static.wikia.nocookie.net/toontown/images/a/aa/Sellbot_Factory.png", "In The Sellbot HQ Factory Exterior"],
        11500: ["https://static.wikia.nocookie.net/toontown/images/a/aa/Sellbot_Factory.png", "In The Sellbot Front Factory"],
        11600: ["https://static.wikia.nocookie.net/toontown/images/a/aa/Sellbot_Factory.png", "In The Sellbot Side Factory"],

        12000: ["https://static.wikia.nocookie.net/toontown/images/f/fe/Cashbot_Headquarters.png", "At Cashbot HQ"],
        12100: ["https://spikesrewrittenguide.com/images/cogs/cashbots/cbhq_vault.PNG", "In The Cashbot HQ Lobby"],
        12500: ["https://static.wikia.nocookie.net/toontown/images/b/b7/Coin_Mint.png", "In The Cashbot Coin Mint"],
        12600: ["https://static.wikia.nocookie.net/toontown/images/b/b7/Coin_Mint.png", "In The Cashbot Dollar Mint"],
        12700: ["https://static.wikia.nocookie.net/toontown/images/4/48/Bullions.jpg", "In The Cashbot Bullion Mint"],

        13000: ["https://static.wikia.nocookie.net/toontown/images/5/5f/Lawbot_Headquarters.png", "At Lawbot HQ"],
        13100: ["https://static.wikia.nocookie.net/toontown/images/c/c8/Screenshot-Wed-Jul-31-13-17-19-2013-5711.jpg", "In The Courthouse Lobby"],
        13200: ["https://static.wikia.nocookie.net/toontown/images/d/d1/District_Attorneys_Office.png", "In The DA's Office Lobby"],
        13300: ["https://static.wikia.nocookie.net/toontown/images/d/d1/District_Attorneys_Office.png", "In The Lawbot Office A"],
        13400: ["https://static.wikia.nocookie.net/toontown/images/d/d1/District_Attorneys_Office.png", "In The Lawbot Office B"],
        13500: ["https://static.wikia.nocookie.net/toontown/images/d/d1/District_Attorneys_Office.png", "In The Lawbot Office C"],
        13600: ["https://static.wikia.nocookie.net/toontown/images/d/d1/District_Attorneys_Office.png", "In The Lawbot Office D"],



        17000: ['https://static.wikia.nocookie.net/toontown/images/f/f7/Chip_n_Dales_MiniGolf.png', "In Chip 'n Dale's MiniGolf"]

    }


    def __init__(self):
        self.discordRPC = None
        if base.wantRichPresence:
            self.enable()
        else:
            self.disable()
        self.updateTask = None
        self.details = "Loading" # text next to photo
        self.image = LOGO
        self.imageTxt = 'Toontown Archipelago' #Hover text for main image 
        self.state = '   ' #Displayed underneath details, used for boarding groups
        self.smallTxt = 'Loading'
        self.partySize = 1
        self.maxParty = 1

    def stopBoarding(self):
        if not base.wantRichPresence:
            return
        self.state = '  '
        self.partySize = 1
        self.maxParty = 1
        self.setData()

    def allowBoarding(self, size):
        if not base.wantRichPresence:
            return 
        self.state = 'In a boarding group'
        self.partySize = 1
        self.maxParty = size
        self.setData()

    def setBoarding(self, size):
        if not base.wantRichPresence:
            return 
        self.PartySize = size
        self.setData()

    def setData(self, details=None, image=None, imageTxt=None):
        if not base.wantRichPresence:
            return
        if details is None:
            details = self.details
        if image is None:
            image = self.image
        if imageTxt is None:
            imageTxt = self.imageTxt
        smallTxt = self.smallTxt
        state = self.state
        party = self.partySize
        maxSize = self.maxParty
        if self.discordRPC is not None:
            self.discordRPC.update(state=state,details=details , large_image=image, large_text=imageTxt, small_text=smallTxt, party_size=[party, maxSize])
    
    def setLaff(self, hp, maxHp):
        if not base.wantRichPresence:
            return
        self.state = '{0}: {1}/{2}'.format(base.localAvatar.getName(), hp, maxHp)
        self.setData()

    def updateTasks(self, task):
        if not base.wantRichPresence:
            return 
        self.updateTask = True
        self.setData()
        return task.again
    
    def avChoice(self):
        if not base.wantRichPresence:
            return
        self.image = LOGO
        self.details = 'Picking a Toon.'
        self.state = '  '
        self.setData()

    def launching(self):
        if not base.wantRichPresence:
            return
        self.image = LOGO
        self.details = 'Loading...'
        self.setData()

    def making(self):
        if not base.wantRichPresence:
            return  
        self.image = LOGO
        self.details = 'Making a Toon.'
        self.setData()

    def startTasks(self):
        if not base.wantRichPresence:
            return
        taskMgr.doMethodLater(10, self.updateTasks, 'UpdateTask')



    def vp(self):
        if not base.wantRichPresence:
            return
        self.image = 'https://static.wikia.nocookie.net/toontown-corporate-clash/images/9/92/VP.png/'
        self.details = 'Fighting the VP.'
        self.setData()

    def cfo(self):
        self.image = 'https://static.wikia.nocookie.net/toontown-corporate-clash/images/3/37/CFO.png'
        self.details = 'Fighting the CFO.'
        self.setData()

    def cj(self):
        self.image = 'https://static.wikia.nocookie.net/toontown-corporate-clash/images/3/31/Cj1.png'
        self.details = 'Fighting the CJ.'
        self.setData()

    def ceo(self):
        self.image = 'https://static.wikia.nocookie.net/toontown/images/e/e4/CeoPic.png'
        self.details = 'Fighting the CEO.'

    def setZone(self,zone): # Set image and text based on the zone
        if not isinstance(zone, int):
            return
        zone -= zone % 100
        data = self.zone2imgdesc.get(zone,None)
        if data:
            self.image = data[0]
            self.details = data[1]
            self.setData()
        else:
            self.notify.warning(f'Could not find image and description for zone {zone % 100}.')
        

    def enable(self):
        clientId = "1255381622128377998"
        try:
            if self.discordRPC is None:
                self.discordRPC = Presence(clientId)
                try:
                    self.discordRPC.connect()
                except PermissionError as e:
                    self.notify.warning(f"Failed to connect to Discord RPC: {e}")
                    self.discordRPC = None
        except PyPresenceException:
            self.notify.warning("Discord not found for this client.")
            self.discordRPC = None

    def disable(self):
        if self.discordRPC is not None:
            try:
                self.discordRPC.clear()
                if self.discordRPC is not None:
                    self.discordRPC.close()
            except PyPresenceException:
                self.notify.warning('Discord not open or invalid client id')
            self.discordRPC = None
            self.updateTask = None