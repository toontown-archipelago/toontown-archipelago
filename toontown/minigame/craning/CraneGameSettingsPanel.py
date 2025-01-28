from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import ToonHead
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame import MinigameGlobals

PLAYER_COLOR = (0.7, 0.9, 0.7, 1.0)  # Light green for players
SPECTATOR_COLOR = (0.9, 0.7, 0.7, 1.0)  # Light red for spectators
SPOT_BORDER_COLOR = (0.8, 0.8, 0.8, 1.0)  # Light gray border

class CraneGameSettingsPanel(DirectFrame):
    def __init__(self, gameTitle, doneEvent):
        DirectFrame.__init__(self, relief=None, 
                           geom=DGG.getDefaultDialogGeom(),
                           geom_color=ToontownGlobals.GlobalDialogColor[:3] + (0.8,),
                           geom_scale=(1.75, 1, 1.25),
                           pos=(0, 0, 0))
        
        self.initialiseoptions(CraneGameSettingsPanel)
        self.doneEvent = doneEvent
        self.gameTitle = gameTitle
        self.playerSpots = []
        self.selectedSpot = None
        self.isLeader = True  # Will be set based on if player is first to join
        self.toonHeads = {}  # Store toon head nodes
        self.TIMEOUT = MinigameGlobals.rulesDuration  # Default 16 seconds
        
        self.load()
        
    def load(self):
        # Create the main panel frame
        self.frame = DirectFrame(parent=self,
                               relief=None,
                               pos=(0, 0, 0),
                               scale=1.0)
                               
        # Create title text
        self.titleText = DirectLabel(parent=self.frame,
                                   relief=None,
                                   text=self.gameTitle,
                                   text_scale=0.1,
                                   text_fg=(0.2, 0.2, 0.2, 1),
                                   pos=(0, 0, 0.6))
                                   
        # Create player spots
        self.playerSpots = []
        self.toonHeads = {}
        
        # Calculate grid layout
        spotWidth = 0.35  # Width of each spot
        spotHeight = 0.35  # Increased height
        verticalSpacing = 0.1  # Reduced vertical spacing
        horizontalSpacing = 0.05  # Horizontal spacing between spots
        
        # Create two rows of four spots
        for i in range(8):
            row = i // 4  # 0 for first row, 1 for second row
            col = i % 4   # 0-3 for position in row
            
            xPos = (col - 1.5) * (spotWidth + horizontalSpacing)
            yPos = 0.3 - (row * (spotHeight + verticalSpacing))
            
            # All spots start as player spots by default
            spot = self.createPlayerSpot(i, True, xPos, yPos, spotWidth, spotHeight)
            self.playerSpots.append(spot)
            
        # Find the minigame instance
        for obj in base.cr.doId2do.values():
            if isinstance(obj, DistributedMinigame):
                # Set leader status based on local toon being first in avIdList
                self.isLeader = base.localAvatar.doId == obj.avIdList[0]
                # Assign players to spots based on their order in avIdList
                for i, avId in enumerate(obj.avIdList):
                    if i < len(self.playerSpots):  # Make sure we don't exceed available spots
                        toon = base.cr.doId2do.get(avId)
                        if toon:
                            self.occupySpot(i, toon)
                break
                
        # Create play button with better styling
        self.playButton = DirectButton(parent=self.frame,
                                     relief=DGG.RAISED,
                                     frameColor=(0.8, 0.8, 0.9, 1),
                                     frameSize=(-0.2, 0.2, -0.05, 0.05),
                                     text='Play',
                                     text_scale=0.06,
                                     text_fg=(0.2, 0.2, 0.2, 1),
                                     pos=(0, 0, -0.5),
                                     command=self.handlePlay)
                                     
        # If not leader, hide play button and auto-send ready
        if not self.isLeader:
            self.playButton.hide()
            messenger.send(self.doneEvent)
            
        # Create timer
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self.frame)
        self.timer.setScale(0.4)
        self.timer.setPos(0.997, 0, 0.064)
        self.timer.hide()
        
        # Accept enter key to start game (only for leader)
        if self.isLeader:
            self.accept('enter', self.handlePlay)

    def createPlayerSpot(self, index, isPlayer, xPos, yPos, width, height):
        # Create main frame with border
        frame = DirectFrame(parent=self,
                          relief=DGG.RAISED,
                          borderWidth=(0.01, 0.01),
                          frameColor=PLAYER_COLOR if isPlayer else SPECTATOR_COLOR,
                          frameSize=(-width/2, width/2, -height/2, height/2),
                          pos=(xPos, 0, yPos))
                          
        # Only leader can toggle player/spectator status
        if self.isLeader:
            button = DirectButton(parent=frame,
                                relief=None,
                                frameSize=(-width/2 + 0.01, width/2 - 0.01, -height/2 + 0.01, height/2 - 0.01),
                                command=self.handleSpotToggle,
                                extraArgs=[index])
                                
        # Label showing if it's a player or spectator spot
        label = DirectLabel(parent=frame,
                          text='Player' if isPlayer else 'Spectator',
                          text_scale=0.06,
                          text_fg=(0.2, 0.2, 0.2, 1),
                          text_pos=(0, height/4))
                          
        # Name label (empty until occupied)
        nameLabel = DirectLabel(parent=frame,
                              text='',
                              text_scale=0.05,
                              text_fg=(0.2, 0.2, 0.2, 1),
                              text_pos=(0, -height/3),
                              text_wordwrap=width*20)
                              
        # Create a separate frame for the toon head
        headFrame = DirectFrame(parent=frame,
                              relief=None,
                              pos=(0, 0, 0))
                              
        return {'frame': frame,
                'label': label,
                'nameLabel': nameLabel,
                'headFrame': headFrame,
                'occupied': False,
                'isPlayer': isPlayer}
                
    def handleSpotToggle(self, spotIndex):
        # Only leader can toggle spots
        if not self.isLeader:
            return
            
        spot = self.playerSpots[spotIndex]
        spot['isPlayer'] = not spot['isPlayer']
        spot['label']['text'] = 'Player' if spot['isPlayer'] else 'Spectator'
        spot['frame']['frameColor'] = PLAYER_COLOR if spot['isPlayer'] else SPECTATOR_COLOR
        
        # Send message to server about the change
        messenger.send('spotStatusChanged', [spotIndex, spot['isPlayer']])
        
    def updateSpotStatus(self, spotIndex, isPlayer):
        if spotIndex >= len(self.playerSpots):
            return
            
        spot = self.playerSpots[spotIndex]
        spot['isPlayer'] = isPlayer
        spot['label']['text'] = 'Player' if isPlayer else 'Spectator'
        spot['frame']['frameColor'] = PLAYER_COLOR if isPlayer else SPECTATOR_COLOR
        
    def createToonHead(self, toon):
        head = ToonHead.ToonHead()
        head.setupHead(toon.style, forGui=1)
        head.setH(180)
        head.setScale(0.13)  # Slightly increased scale
        head.setDepthTest(True)
        head.setDepthWrite(True)
        head.setBin('gui-popup', 0)  # Ensure head renders on top
        return head
        
    def occupySpot(self, index, toon):
        if index >= len(self.playerSpots):
            return
            
        # Clear any existing head in this spot
        self.clearSpot(index)
            
        spot = self.playerSpots[index]
        spot['occupied'] = True
        spot['nameLabel']['text'] = toon.getName()
        spot['frame']['relief'] = DGG.SUNKEN
        
        # Create and position new head
        head = self.createToonHead(toon)
        head.reparentTo(spot['headFrame'])
        head.setPos(0, 5.5, 0.05)  # Adjusted Z position and moved forward
        self.toonHeads[index] = head
        
    def clearSpot(self, index):
        if index >= len(self.playerSpots):
            return
            
        spot = self.playerSpots[index]
        spot['occupied'] = False
        spot['nameLabel']['text'] = ''
        spot['frame']['relief'] = DGG.RAISED
        
        # Remove toon head if it exists
        if index in self.toonHeads:
            if self.toonHeads[index]:
                self.toonHeads[index].removeNode()
                self.toonHeads[index] = None
            del self.toonHeads[index]
        
    def handlePlay(self):
        # Only leader can start the game
        if not self.isLeader:
            return
            
        # Verify we have required players
        playerCount = sum(1 for spot in self.playerSpots if spot['occupied'] and spot['isPlayer'])
        if playerCount >= 1:  # Changed from < 1 to >= 1 since we want at least 1 player
            messenger.send(self.doneEvent)
        
    def cleanup(self):
        # Stop timer and cleanup
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.timer.destroy()
            del self.timer
        
        # Cleanup toon heads
        for index in list(self.toonHeads.keys()):
            self.clearSpot(index)
        self.toonHeads = {}
        
        if hasattr(self, 'playerSpots') and self.playerSpots:
            for spot in self.playerSpots:
                if spot['frame']:
                    spot['frame'].destroy()
        self.playerSpots = None
        
        # Remove enter key handler
        self.ignore('enter')
        
        # Call parent's destroy
        DirectFrame.destroy(self)