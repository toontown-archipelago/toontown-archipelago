"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State

from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI


class DistributedMinigameTemplateAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        super().__init__(air, minigameId)

        self.gameFSM = ClassicFSM('DistributedMinigameTemplateAI',
                                  [
                                      State('inactive',
                                            self.enterInactive,
                                            self.exitInactive,
                                            ['play']),
                                      State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup']),
                                      State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            ['inactive']),
                                  ],
                                  # Initial State
                                  'inactive',
                                  # Final State
                                  'inactive',
                                  )

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    def generate(self):
        self.notify.debug("generate")
        super().generate()

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        super().delete()

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        super().setGameReady()
        # all of the players have checked in
        # they will now be shown the rules

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        super().setGameStart(timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        super().setGameAbort()

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        super().gameOver()

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # when the game is done, call gameOver()
        self.gameOver()

    def exitPlay(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
