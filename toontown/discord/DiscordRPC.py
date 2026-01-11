import time
from ctypes import *
from direct.task import Task
from pypresence import Presence
from pypresence.exceptions import PipeClosed, ServerError
from pypresence.exceptions import PyPresenceException
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import threading
from toontown.toonbase import ToontownGlobals
clientId  = "1255381622128377998"
LOGO = "toontown-logo"

class DiscordRPC(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordRPC')
    zone2imgdesc = {  # A dict of ZoneID -> An image and a description
        ToontownGlobals.DonaldsDock: ["donalds_dock", "In Donald's Dock"],
        ToontownGlobals.BarnacleBoulevard: ["barnacle_boulevard_tunnel", "On Barnacle Boulevard"],
        ToontownGlobals.SeaweedStreet: ["seaweed_street_tunnel", "On Seaweed Street"],
        ToontownGlobals.LighthouseLane: ["lighthouse_lane_tunnel", "On Lighthouse Lane"],

        ToontownGlobals.ToontownCentral: ["toontown_central", "In Toontown Central"],
        ToontownGlobals.SillyStreet: ["silly_street_tunnel", "On Silly Street"],
        ToontownGlobals.LoopyLane: ["loopy_lane_tunnel", "On Loopy Lane"],
        ToontownGlobals.PunchlinePlace: ["punchline_place_tunnel", "On Punchline Place"],

        ToontownGlobals.TheBrrrgh: ["the_brrrgh", "In The Brrrgh"],
        ToontownGlobals.WalrusWay: ["walrus_way_tunnel", "On Walrus Way"],
        ToontownGlobals.SleetStreet: ["sleet_street_tunnel", "On Sleet Street"],
        ToontownGlobals.PolarPlace: ["polar_place_tunnel", "On Polar Place"],

        ToontownGlobals.MinniesMelodyland: ["minnies_melodyland", "In Minnie's Melodyland"],
        ToontownGlobals.AltoAvenue: ["alto_avenue_tunnel", "On Alto Avenue"],
        ToontownGlobals.BaritoneBoulevard: ["baritone_boulevard_tunnel", "On Baritone Boulevard"],
        ToontownGlobals.TenorTerrace: ["tenor_terrace_tunnel", "On Tenor Terrace"],

        ToontownGlobals.DaisyGardens: ["daisy_gardens", "In Daisy Gardens"],
        ToontownGlobals.ElmStreet: ["elm_street_tunnel", "On Elm Street"],
        ToontownGlobals.MapleStreet: ["maple_street_tunnel", "On Maple Street"],
        ToontownGlobals.OakStreet: ["oak_street_tunnel", "On Oak Street"],

        ToontownGlobals.OutdoorZone: ["chip_n_dales_acorn_acres", "At Chip 'n Dale's Acorn Acres"],

        ToontownGlobals.GoofySpeedway: ["goofy_speedway", "In Goofy Speedway"],

        ToontownGlobals.DonaldsDreamland: ["donalds_dreamland", "In Donald's Dreamland"],
        ToontownGlobals.LullabyLane: ["lullaby_lane_tunnel", "On Lullaby Lane"],
        ToontownGlobals.PajamaPlace: ["pajama_place_tunnel", "On Pajama Place"],

        ToontownGlobals.BossbotHQ: ["bossbot_hq", "At Bossbot HQ"],
        ToontownGlobals.BossbotLobby: ["bossbot_clubhouse", "In The CEO Clubhouse"],
        ToontownGlobals.BossbotCountryClubIntA: ["bossbot_hq_the_front_one", "In The Front One"],
        ToontownGlobals.BossbotCountryClubIntB: ["bossbot_hq_the_middle_two", "In The Middle Two"],
        ToontownGlobals.BossbotCountryClubIntC: ["bossbot_hq_the_back_three", "In The Back Three"],

        ToontownGlobals.SellbotHQ: ["sellbot_hq", "At Sellbot HQ"],
        ToontownGlobals.SellbotLobby: ["sellbot_hq_lobby", "In The Sellbot HQ Lobby"],
        ToontownGlobals.SellbotFactoryExt: ["sellbot_factory", "In The Sellbot HQ Factory Exterior"],
        ToontownGlobals.SellbotFactoryInt: ["sellbot_factory_front", "In The Sellbot Front Factory"],
        ToontownGlobals.SellbotFactoryIntS: ["sellbot_factory_side", "In The Sellbot Side Factory"],

        ToontownGlobals.CashbotHQ: ["cashbot_hq", "At Cashbot HQ"],
        ToontownGlobals.CashbotLobby: ["cashbot_hq_vault", "In The Cashbot HQ Lobby"],
        ToontownGlobals.CashbotMintIntA: ["cashbot_hq_coin_mint", "In The Cashbot Coin Mint"],
        ToontownGlobals.CashbotMintIntB: ["cashbot_hq_dollar_mint", "In The Cashbot Dollar Mint"],
        ToontownGlobals.CashbotMintIntC: ["cashbot_hq_bullion_mint", "In The Cashbot Bullion Mint"],

        ToontownGlobals.LawbotHQ: ["lawbot_hq", "At Lawbot HQ"],
        ToontownGlobals.LawbotLobby: ["lawbot_hq_courthouse_lobby", "In The Courthouse Lobby"],
        ToontownGlobals.LawbotOfficeExt: ["district_attorneys_office", "In The DA's Office Lobby"],
        ToontownGlobals.LawbotOfficeInt: ["da_office_a", "In The Lawbot Office A"],
        ToontownGlobals.LawbotStageIntB: ["da_office_b", "In The Lawbot Office B"],
        ToontownGlobals.LawbotStageIntC: ["da_office_c", "In The Lawbot Office C"],
        ToontownGlobals.LawbotStageIntD: ["da_office_d", "In The Lawbot Office D"],

        ToontownGlobals.GolfZone: ["chip_n_dales_minigolf", "In Chip 'n Dale's MiniGolf"]
    }

    def __init__(self):
        self.discordRPC = None
        if base.wantRichPresence:
            self.enable()
        else:
            self.disable()
        self.updateTask = None
        self.details = "Loading"  # text next to photo
        self.image = LOGO
        self.imageTxt = 'Toontown Archipelago'  #Hover text for main image
        self.state = '   '  #Displayed underneath details, used for boarding groups
        self.smallTxt = 'Loading'
        self.partySize = 1
        self.maxParty = 1
        self.discordTask = None

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
            try:
                self.discordRPC.update(state=state, details=details, large_image=image, large_text=imageTxt,
                                       small_text=smallTxt, party_size=[party, maxSize])
            except (PipeClosed, BrokenPipeError, ServerError, OSError):
                # schedule a task to try to reconnect to the discord
                self.discordRPC = None
                self.notify.warning('Discord RPC connection lost, trying to reconnect in 30 seconds.')
                self.discordTask = threading.Timer(30, self.reconnectDiscord)
                self.discordTask.start()
            except RuntimeError as e:
                if str(e) == "This event loop is already running":
                    self.notify.warning("This event loop is already running")
                else:
                    self.notify.warning(f"Runtime Error: {e}")

    def reconnectDiscord(self):
        self.enable()
        # timer is done
        self.discordTask = None

    def setLaff(self, hp, maxHp):
        if not base.wantRichPresence:
            return
        self.state = '{0}: {1}/{2}'.format(base.localAvatar.getName(), hp, maxHp)
        self.setData()

    def updateTasks(self):
        try:
            if not base.wantRichPresence:
                return
        except NameError: # If the base is not defined, then the game is shutting down
            # cancel the task
            self.updateTask.cancel()
            return
        self.setData()
        # schedule the next update
        self.updateTask = threading.Timer(10, self.updateTasks)
        self.updateTask.start()

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

    def sleeping(self):
        if not base.wantRichPresence:
            return
        self.image = LOGO
        self.details = 'Sleeping...'
        self.imageTxt='AFK'
        self.setData()

    def startTasks(self):
        if not base.wantRichPresence:
            return
        self.updateTask = threading.Timer(10, self.updateTasks)
        self.updateTask.start()

    def vp(self):
        if not base.wantRichPresence:
            return
        self.image = 'vp'
        self.details = 'Fighting the VP.'
        self.setData()

    def cfo(self):
        if not base.wantRichPresence:
            return
        self.image = 'cfo'
        self.details = 'Fighting the CFO.'
        self.setData()

    def cj(self):
        if not base.wantRichPresence:
            return
        self.image = 'cj'
        self.details = 'Fighting the CJ.'
        self.setData()

    def ceo(self):
        if not base.wantRichPresence:
            return
        self.image = 'ceo'
        self.details = 'Fighting the CEO.'
        self.setData()

    def setZone(self, zone):  # Set image and text based on the zone
        if not isinstance(zone, int):
            return
        zone -= zone % 100
        data = self.zone2imgdesc.get(zone, None)
        if data:
            self.image = data[0]
            self.details = data[1]
            self.setData()
        else:
            self.notify.warning(f'Could not find image and description for zone {zone % 100}.')

    def enable(self):
        try:
            if self.discordRPC is None:
                self.discordRPC = Presence(clientId)
                try:
                    self.discordRPC.connect()
                except PermissionError as e:
                    self.notify.warning(f"Failed to connect to Discord RPC: {e}")
                    self.discordRPC = None
                except ConnectionError:
                    self.notify.debug("Failed to connect to Discord RPC: Connection Error, trying to reconnect in 30 seconds.")
                    self.discordRPC = None
                    # schedule a task to try again later
                    self.discordTask = threading.Timer(30, self.reconnectDiscord)
                    self.discordTask.start()

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
            if self.updateTask is not None:
                self.updateTask.cancel()
                self.updateTask = None
            if self.discordTask is not None:
                self.discordTask.cancel()
                self.discordTask = None

