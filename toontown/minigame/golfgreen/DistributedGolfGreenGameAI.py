import random

from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.task.TaskManagerGlobal import taskMgr

from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.minigame.golfgreen import GolfGreenConstants


class DistributedGolfGreenGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        super().__init__(air, minigameId)

        self.gameFSM = ClassicFSM(self.__class__.__name__,
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

        # reset scores
        self.scoreDict = {avId: 0 for avId in self.avIdList}

        for avId in self.avIdList:
            self.d_startBoard(avId)

        taskMgr.doMethodLater(GolfGreenConstants.GAME_DURATION, self.timerExpired, self.taskName('gameTimer'))

    def timerExpired(self, task):
        self.notify.debug('timer expired')
        self.gameOver()
        return task.done

    def exitPlay(self):
        taskMgr.remove(self.taskName('gameTimer'))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    """
    stuff
    """

    def requestBoard(self, win: bool):
        senderId = self.air.getAvatarIdFromSender()

        if win:
            self.scoreDict[senderId] += 1
            self.sendScoreData()

            if GolfGreenConstants.WANT_GIFTS:
                self.sendUpdate('helpOthers', [senderId])

        self.d_startBoard(senderId)

    def d_startBoard(self, avId: int) -> None:
        board = random.choice(GolfGreenConstants.BOARD_DATA)

        x = []
        for rowIndex in range(1, len(board)):
            for columnIndex in range(len(board[rowIndex])):
                color = GolfGreenConstants.TRANSLATE_DATA.get(board[rowIndex][columnIndex])
                if color is not None:
                    x.append((len(board[rowIndex]) - (columnIndex + 1), rowIndex - 1, color))

        attackPattern = []
        for ball in board[0]:
            color = GolfGreenConstants.TRANSLATE_DATA.get(ball)
            if color or color == 0:
                place = random.choice(list(range(0, len(attackPattern) + 1)))
                attackPattern.insert(place, color)
                place = random.choice(list(range(0, len(attackPattern) + 1)))
                attackPattern.insert(place, color)

        self.sendUpdateToAvatarId(avId, 'startBoard', [x, attackPattern])

    def sendScoreData(self):
        self.sendUpdate('scoreData', [list(self.scoreDict.items())])
