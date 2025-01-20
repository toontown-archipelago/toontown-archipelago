import math
import random
from math import pi

from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.gui import DirectGuiGlobals
from direct.gui.DirectFrame import DirectFrame
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence
from direct.showbase.MessengerGlobal import messenger
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec4, Point3, BitMask32, TransparencyAttrib

from toontown.battle import MovieUtil
from toontown.coghq import GameSprite3D
from toontown.golf import BuildGeometry
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.MinigameAvatarScorePanel import MinigameAvatarScorePanel
from toontown.minigame.golfgreen import GolfGreenConstants
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toonbase.ToontownTimer import ToontownTimer


class DistributedGolfGreenGame(DistributedMinigame):
    # define constants that you won't want to tweak here

    def __init__(self, cr):
        super().__init__(cr)
        self.scorePanels = {}

        self.blankColor = Vec4(1.0, 1.0, 1.0, 1.0)
        self.fullColor = Vec4(0.6, 0.6, 0.6, 1.0)
        self.neighborColor = Vec4(0.8, 0.8, 0.8, 1.0)
        self.outColor = Vec4(0.0, 0.0, 0.0, 0.0)
        self.blackColor = Vec4(0.0, 0.0, 0.0, 1.0)
        self.sprites = []
        self.controlSprite = None
        self.standbySprite = None
        self.colorGridFlag = 0
        self.boardIndex = None
        self.board = None
        self.attackPattern = None
        self.tooLowFlag = 0
        self.toonPoints = (Point3(3.0, 13.0, 0.0),
                           Point3(6.0, 13.0, 0.0),
                           Point3(-3.0, 13.0, 0.0),
                           Point3(-6.0, 13.0, 0.0))
        self.flagNextLevel = 0
        self.wildIndex = 8
        self.bombIndex = 7
        self.sizeMult = 1.4
        self.cellSizeX = 1.0 * self.sizeMult
        self.cellSizeZ = self.cellSizeX * 0.8
        self.radiusBall = 0.5 * self.cellSizeX
        self.gridDimX = 9
        self.gridDimZ = 15
        self.minX = -1.0 * (self.gridDimX + 0.3751) * 0.5 * self.cellSizeX
        self.minZ = -self.gridDimZ * 0.1 * self.cellSizeZ
        self.newBallX = 0.0
        self.newBallZ = self.minZ + 0.1 * self.sizeMult
        self.rangeX = (self.gridDimX + 0.5) * self.cellSizeX
        self.rangeZ = self.gridDimZ * self.cellSizeZ
        self.maxX = self.minX + self.rangeX
        self.maxZ = self.minZ + self.rangeZ
        self.sizeX = self.rangeX
        self.sizeZ = self.rangeZ
        self.isActive = 0
        self.giftId = None
        self.holdGiftId = None
        self.rollTrack = None
        self.zGap = 0.092
        self.screenSizeX = base.a2dRight - base.a2dLeft
        self.screenSizeZ = base.a2dTop - base.a2dBottom
        self.XtoZ = self.screenSizeX / (self.screenSizeZ * (1.0 - self.zGap * 1.0))
        self.countTimeOld = None
        self.countDownRunning = 0
        self.timer = None
        self.hasEntered = 0
        self.trackClosed = 0
        self.running = 0
        self.finished = 0

        self.gameFSM = ClassicFSM(self.__class__.__name__,
                                  [
                                      State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                      State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup']),
                                      State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            []),
                                  ],
                                  # Initial State
                                  'off',
                                  # Final State
                                  'cleanup',
                                  )

        # it's important for the final state to do cleanup;
        # on disconnect, the ClassicFSM will be forced into the
        # final state. All states (except 'off') should
        # be prepared to transition to 'cleanup' at any time.

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    def getTitle(self):
        return TTLocalizer.GolfGreenGameTitle

    def getInstructions(self):
        return TTLocalizer.GolfGreenGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return GolfGreenConstants.GAME_DURATION

    def load(self):
        self.notify.debug("load")
        super().load()
        # load resources and create objects here
        rng = random.Random()
        rng.seed(self.getDoId())
        musicName = rng.choice(
            ['phase_12/audio/bgm/Bossbot_Factory_v1.ogg', 'phase_12/audio/bgm/Bossbot_Factory_v2.ogg',
             'phase_12/audio/bgm/Bossbot_Factory_v3.ogg'])
        self.music = base.loader.loadMusic(musicName)

        self.geom = loader.loadModel("phase_12/models/bossbotHQ/BossbotGreenRoom_A")
        self.geom.reparentTo(render)

        self.baseNode = render.attachNewNode('GolfGreenGameBase')
        self.frame = self.baseNode.attachNewNode('GolfGreenGameFrame')
        self.spriteNode = self.frame.attachNewNode('GolfGreenGameSpriteNode')
        self.frame.setScale(1.0)
        self.frame.setP(90)
        self.spriteNotchPos = 0
        self.frame.setY(10.0)
        self.frame.setZ(2.0)
        self.spriteNode.setY(0.5)
        self.hasChanged = 0
        self.squareNode = self.frame.attachNewNode('GolfGreenGameBase')
        groundCircle = loader.loadModel('phase_12/models/bossbotHQ/bust_a_cog_golf_green')
        groundCircle.reparentTo(self.baseNode)
        groundCircle.setScale(0.24)
        self.groundFlag = loader.loadModel('phase_12/models/bossbotHQ/bust_a_cog_golf_flag')
        self.groundFlag.reparentTo(self.baseNode)
        self.groundFlag.setScale(0.5)
        self.groundFlag.setH(-45)
        self.groundFlag.setPos(3.0, 4.0, 0.0)
        groundSquare = BuildGeometry.addSquareGeom(self.squareNode, self.sizeX, self.sizeZ,
                                                   color=Vec4(0.4, 0.4, 0.4, 0.5))
        self.centerZ = (self.minZ + self.maxZ) * 0.5
        self.squareNode.setZ((self.minZ + self.maxZ) * 0.5)
        self.squareNode.setP(-90)
        groundCircle.setDepthWrite(False)
        groundCircle.setDepthTest(True)
        groundCircle.setBin('ground', 1)
        groundSquare[0].setDepthWrite(False)
        groundSquare[0].setDepthTest(False)
        groundSquare[0].setBin('ground', 2)
        self.squareNode.hide()

        model = loader.loadModel('phase_5.5/models/gui/package_delivery_panel')
        model1 = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        self.model = model
        self.model1 = model1
        self.soundFire = base.loader.loadSfx('phase_6/audio/sfx/Golf_Hit_Ball.ogg')
        self.soundLand = base.loader.loadSfx('phase_4/audio/sfx/MG_maze_pickup.ogg')
        self.soundBurst = base.loader.loadSfx('phase_5/audio/sfx/Toon_bodyfall_synergy.ogg')
        self.soundBomb = base.loader.loadSfx('phase_4/audio/sfx/MG_cannon_fire_alt.ogg')
        self.soundLose = base.loader.loadSfx('phase_11/audio/sfx/LB_capacitor_discharge_3.ogg')
        self.soundWin = base.loader.loadSfx('phase_4/audio/sfx/MG_pairing_match_bonus_both.ogg')
        self.soundDone = base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_back.ogg')
        self.soundMove = base.loader.loadSfx('phase_3.5/audio/sfx/SA_shred.ogg')
        self.focusPoint = self.baseNode.attachNewNode('GolfGreenGameFrame')
        self.backBoard = loader.loadModel('phase_12/models/bossbotHQ/bust_a_cog_background')
        self.backBoard.setCollideMask(BitMask32.allOff())
        self.backBoard.reparentTo(self.frame)
        self.backBoard.setScale(0.3, 0.2, 0.25)
        self.backBoard.setHpr(0, -90, 0)
        self.backBoard.setPos(0, -1.5, 8.0)
        self.backBoard.hide()

        self.aimbase = loader.loadModel('phase_12/models/bossbotHQ/bust_a_cog_shooter')
        self.aimbase.setHpr(90, 0, 90)
        self.aimbase.setScale(0.3, 0.3, 0.15)
        self.aimbase.reparentTo(self.frame)
        self.aimbase.setPos(0.0, 0.0, self.minZ + 0.1)
        self.aimer = self.aimbase.attachNewNode('GolfGreenGameBase')
        aimer = self.aimbase.find('**/moving*')
        aimer.reparentTo(self.aimer)
        aimer.setPos(0.0, 0.0, 0.0)
        self.aimbase.hide()

        self.frame2D = DirectFrame(scale=1.1, relief=DirectGuiGlobals.FLAT, frameSize=(-0.1,
                                                                                       0.1,
                                                                                       -0.1,
                                                                                       -0.1),
                                   frameColor=(0.737, 0.573, 0.345, 0.3))
        self.bonusBoard = DirectFrame(parent=self.frame2D, relief=None, image_pos=(0, 0, 0.0),
                                      image_scale=(0.4, 1, 0.4), image_color=(1, 1, 1, 1), pos=(0.0, 1.5, 0.67),
                                      scale=1.0, text='You gotsa bonus fool!', text_font=ToontownGlobals.getSignFont(),
                                      text0_fg=(1, 1, 1, 1), text0_shadow=(0.0, 0.0, 0.0, 1), text_scale=0.055,
                                      text_pos=(0, -0.1), textMayChange=1)
        self.bonusBoard.hide()

    def unload(self):
        self.notify.debug("unload")
        super().unload()
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

        self.geom.removeNode()
        del self.geom

        self.music.stop()
        del self.music

        self.soundFire = None
        self.soundLand = None
        self.soundBurst = None
        self.soundBomb = None
        self.soundLose = None
        self.soundWin = None
        self.soundDone = None
        self.soundMove = None
        self.baseNode.removeNode()
        del self.baseNode
        self.stopCountDown()
        self.__stop()
        self.ignoreAll()
        self.frame2D.destroy()

    def onstage(self):
        self.notify.debug("onstage")
        super().onstage()
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...

        # the base class parents the toons to hidden, so consider
        # calling it last
        super().offstage()

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        super().handleDisabledAvatar(avId)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if super().setGameReady():
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        for index, avId in enumerate(self.avIdList):
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                toon.setPos(self.toonPoints[index])
                toon.setHpr(180, 0, 0)
                toon.loop('neutral')

        base.playMusic(self.music, looping=1, volume=1)

        self.__setCamera()

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        super().setGameStart(timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        self.gameFSM.request("play")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")
        spacing = .4
        for i in range(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = MinigameAvatarScorePanel(avId, avName)
            scorePanel.setScale(.9)
            scorePanel.setPos(.75 - spacing * ((len(self.avIdList) - 1) - i), 0.0, .875)
            # make the panels slightly transparent
            scorePanel.makeTransparent(.75)
            self.scorePanels[avId] = scorePanel

        self.timer = ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(GolfGreenConstants.GAME_DURATION)
        self.timer.countdown(GolfGreenConstants.GAME_DURATION, self.timerExpired)

        self.setup()

        self.backBoard.show()
        self.aimbase.show()
        self.squareNode.show()
        self.standbySprite.nodeObj.show()
        self.groundFlag.hide()
        self.isActive = 1
        self.__setCamera()
        self.spriteNode.show()
        base.setCellsAvailable([base.bottomCells[1], base.bottomCells[2], base.bottomCells[3]], 0)

    def timerExpired(self):
        self.notify.debug('local timer expired')
        self.gameOver()

    def exitPlay(self):
        self.timer.destroy()
        del self.timer

        for panel in self.scorePanels.values():
            panel.cleanup()

        self.scorePanels = {}

        taskMgr.remove('GolfGreenGameTask')
        self.stopCountDown()
        self.ignore('mouse1')
        for sprite in self.sprites:
            sprite.delete()

        self.sprites = []
        self.controlSprite = None
        self.running = 0
        self.backBoard.hide()
        self.aimbase.hide()
        self.squareNode.hide()
        self.groundFlag.show()
        self.isActive = 0
        if self.standbySprite:
            self.standbySprite.nodeObj.hide()
        base.setCellsAvailable([base.bottomCells[1], base.bottomCells[2], base.bottomCells[3]], 1)

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    """
    stuff
    """

    def updateSpritePos(self):
        if self.spriteNode.isEmpty():
            return
        self.spriteNode.setZ(-self.spriteNotchPos * self.cellSizeZ)
        self.colorGridFlag = 1

    def lerpSpritePos(self):
        if self.spriteNode.isEmpty():
            return
        x = self.spriteNode.getX()
        y = self.spriteNode.getY()
        self.rollTrack = Sequence(
            LerpPosInterval(self.spriteNode, 0.5, Point3(x, y, -self.spriteNotchPos * self.cellSizeZ)))
        if self.controlSprite:
            if not self.controlSprite.isActive:
                pass
        self.colorGridFlag = 1
        self.rollTrack.start()
        if self.soundMove:
            self.soundMove.play()
        messenger.send('wakeup')

    def findLowestSprite(self):
        lowest = 100
        for sprite in self.sprites:
            if sprite.gridPosZ:
                if sprite.gridPosZ < lowest:
                    lowest = sprite.gridPosZ

        return lowest

    def setup(self):
        self.updateSpritePos()
        self.spriteNode.setY(self.radiusBall)
        thing = self.model.find('**/item_board')
        self.block = self.model1.find('**/minnieCircle')
        self.colorRed = (1, 0, 0, 1)
        self.colorBlue = (0, 0, 1, 1)
        self.colorGreen = (0, 1, 0, 1)
        self.colorGhostRed = (1, 0, 0, 0.5)
        self.colorGhostBlue = (0, 0, 1, 0.5)
        self.colorGhostGreen = (0, 1, 0, 0.5)
        self.colorWhite = (1, 1, 1, 1)
        self.colorBlack = (0, 0, 0, 1.0)
        self.colorShadow = (0, 0, 0, 0.5)
        self.lastTime = None
        self.running = 0
        self.massCount = 0
        self.foundCount = 0
        self.controlOffsetX = 0.0
        self.controlOffsetZ = 0.0
        self.grid = []
        for countX in range(0, self.gridDimX):
            newRow = []
            for countZ in range(self.gridDimZ):
                offset = 0
                margin = self.cellSizeX * 0.4375
                if countZ % 2 == 0:
                    offset = self.cellSizeX * 0.5
                newCell = [None,
                           countX * self.cellSizeX + self.minX + offset + margin,
                           countZ * self.cellSizeZ + self.minZ,
                           countX,
                           countZ,
                           None]
                groundCircle = loader.loadModel('phase_12/models/bossbotHQ/bust_a_cog_hole')
                groundCircle.reparentTo(self.spriteNode)
                if groundCircle is None:
                    import pdb
                    pdb.set_trace()
                groundCircle.setTransparency(TransparencyAttrib.MAlpha)
                groundCircle.setPos(newCell[1], -self.radiusBall, newCell[2])
                groundCircle.setScale(1.2)
                groundCircle.setR(90)
                groundCircle.setH(-90)
                newCell[5] = groundCircle
                newCell[5].setColorScale(self.blankColor)
                newRow.append(newCell)

            self.grid.append(newRow)

        self.cogSprite = self.addUnSprite(self.block, posX=0.25, posZ=0.5)
        self.cogSprite.setColor(self.colorShadow)
        self.cogSprite.nodeObj.hide()
        self.standbySprite = self.addUnSprite(self.block, posX=0.0, posZ=-3.0)
        self.standbySprite.setColor(self.colorShadow)
        self.standbySprite.spriteBase.reparentTo(self.frame)
        self.standbySprite.spriteBase.setY(self.radiusBall)
        self.standbySprite.nodeObj.hide()
        self.boardData = [
            ((1, 0, 0),
             (4, 0, 1),
             (6, 0, 2),
             (1, 1, 0)),
            ((1, 0, 1),
             (4, 0, 1),
             (6, 0, 1),
             (1, 1, 1)),
            ((1, 0, 2),
             (4, 0, 2),
             (6, 0, 2),
             (1, 1, 2))
        ]
        self.attackPatterns = [(0, 1, 2), (0, 0, 1, 1, 2, 2), (0, 1, 0, 2)]
        self.winCounter = 0
        self.matchList = []
        self.newBallTime = 5.0
        self.newBallCountUp = 0.0
        self.cogX = 0
        self.cogZ = 0
        self.aimRadian = 0.0
        self.ballLoaded = 0.0
        self.countDown = GolfGreenConstants.DRAG_BOARD_FWD_TIME

    def show(self):
        self.frame.show()

    def hide(self):
        self.frame.hide()

    def __handleExit(self):
        self.__acceptExit()

    def startBoard(self, board, attackPattern):
        if self.finished:
            return
        self.clearGrid()
        self.board = board
        self.attackPattern = attackPattern
        self.attackCounter = 0
        self.spriteNotchPos = 0
        self.countDown = GolfGreenConstants.DRAG_BOARD_FWD_TIME
        self.tooLowFlag = 0
        for ball in self.board:
            newSprite = self.addSprite(self.block, found=1, color=ball[2])
            self.placeIntoGrid(newSprite, ball[0], self.gridDimZ - 1 - ball[1])

        self.colorGridFlag = 1
        self.tooLowFlag = 0
        self.startCountDown()
        self.updateSpritePos()
        self.killSprite(self.controlSprite)
        self.accept('mouse1', self.__handleMouseClick)
        self.__run()

    def startCountDown(self):
        if self.countDownRunning == 0:
            taskMgr.add(self.doCountDown, 'GolfGreenGame countdown')
            self.countDownRunning = 1

    def stopCountDown(self):
        taskMgr.remove('GolfGreenGame countdown')
        self.countDownRunning = 0
        self.countTimeOld = None
        return

    def doCountDown(self, task):
        currentTime = base.clock.getFrameTime()
        if self.countTimeOld is None:
            self.countTimeOld = currentTime
        if currentTime - self.countTimeOld < 1.0:
            return task.cont

        self.countTimeOld = currentTime
        self.countDown -= 1
        if self.countDown in [3, 2, 1]:
            for sprite in self.sprites:
                sprite.warningBump()

        elif self.countDown == 0:
            self.countDown = GolfGreenConstants.DRAG_BOARD_FWD_TIME
            self.spriteNotchPos += 1
            self.lerpSpritePos()
            self.checkForTooLow()
        return task.cont

    def checkForTooLow(self):
        low = self.findLowestSprite()
        if low <= self.spriteNotchPos:
            self.doFail()

    def doFail(self):
        self.tooLowFlag = 1
        taskMgr.doMethodLater(1.0, self.failBoard, 'finishing Failure')
        for sprite in self.sprites:
            sprite.setColorType(4)

        self.__stop()
        self.ignore('mouse1')

    def failBoard(self, task=None):
        self.__finishBoard(win=False)

    def __handleWin(self):
        self.__handleExit()

    def __finishBoard(self, win: bool):
        if self.rollTrack:
            self.rollTrack.finish()
        self.countDown = GolfGreenConstants.DRAG_BOARD_FWD_TIME
        if win:
            if self.soundWin:
                self.soundWin.play()
        elif self.soundLose:
            self.soundLose.play()
            self.giftId = None
        self.attackPattern = None
        self.stopCountDown()
        self.clearGrid()
        self.spriteNotchPos = 0
        self.updateSpritePos()
        self.__stop()
        self.ignore('mouse1')
        self.sendUpdate('requestBoard', [win])

    def __acceptExit(self, buttonValue=None):
        import pdb
        pdb.set_trace()
        if hasattr(self, 'frame'):
            self.hide()
            self.unload()
        camera.reparentTo(base.localAvatar)
        base.localAvatar.startUpdateSmartCamera()

    def __removeGame(self):
        self.spriteNode.removeNode()

    def findGrid(self, x, z, force=0):
        currentClosest = None
        currentDist = 10000000
        for countX in range(self.gridDimX):
            for countZ in range(self.gridDimZ):
                testDist = self.testPointDistanceSquare(x, z, self.grid[countX][countZ][1],
                                                        self.grid[countX][countZ][2])
                if self.grid[countX][countZ][0] is None and testDist < currentDist and (
                        force or self.hasNeighbor(countX, countZ) is not None):
                    currentClosest = self.grid[countX][countZ]
                    self.closestX = countX
                    self.closestZ = countZ
                    currentDist = testDist

        return currentClosest

    def hasNeighbor(self, cellX, cellZ):
        gotNeighbor = None
        if cellZ % 2 == 0:
            if self.testGridfull(self.getValidGrid(cellX - 1, cellZ)):
                gotNeighbor = cellZ
            elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ)):
                gotNeighbor = cellZ
            elif self.testGridfull(self.getValidGrid(cellX, cellZ + 1)):
                gotNeighbor = cellZ + 1
            elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ + 1)):
                gotNeighbor = cellZ + 1
            elif self.testGridfull(self.getValidGrid(cellX, cellZ - 1)):
                gotNeighbor = cellZ - 1
            elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ - 1)):
                gotNeighbor = cellZ - 1
        elif self.testGridfull(self.getValidGrid(cellX - 1, cellZ)):
            gotNeighbor = cellZ
        elif self.testGridfull(self.getValidGrid(cellX + 1, cellZ)):
            gotNeighbor = cellZ
        elif self.testGridfull(self.getValidGrid(cellX, cellZ + 1)):
            gotNeighbor = cellZ + 1
        elif self.testGridfull(self.getValidGrid(cellX - 1, cellZ + 1)):
            gotNeighbor = cellZ + 1
        elif self.testGridfull(self.getValidGrid(cellX, cellZ - 1)):
            gotNeighbor = cellZ - 1
        elif self.testGridfull(self.getValidGrid(cellX - 1, cellZ - 1)):
            gotNeighbor = cellZ - 1
        return gotNeighbor

    def clearFloaters(self):
        self.grounded = []
        self.unknown = []
        groundZ = self.gridDimZ - 1
        for indexX in range(0, self.gridDimX):
            gridCell = self.grid[indexX][groundZ]
            if gridCell[0]:
                self.grounded.append((indexX, groundZ))

        for column in self.grid:
            for cell in column:
                if cell[0] is not None:
                    cellData = (cell[3], cell[4])
                    if cellData not in self.grounded:
                        self.unknown.append(cellData)

        lastUnknownCount = 0
        while len(self.unknown) != lastUnknownCount:
            lastUnknownCount = len(self.unknown)
            for cell in self.unknown:
                if self.hasGroundedNeighbor(cell[0], cell[1]):
                    self.unknown.remove(cell)
                    self.grounded.append(cell)

        for entry in self.unknown:
            gridEntry = self.grid[entry[0]][entry[1]]
            sprite = gridEntry[0]
            self.killSprite(sprite)

        return

    def explodeBombs(self):
        didBomb = 0
        for column in self.grid:
            for cell in column:
                if cell[0] is not None:
                    if cell[0].colorType == self.bombIndex:
                        self.killSprite(cell[0])
                        didBomb += 1

        if didBomb:
            self.soundBomb.play()
        return

    def hasGroundedNeighbor(self, cellX, cellZ):
        gotNeighbor = None
        if cellZ % 2 == 0:
            if (cellX - 1, cellZ) in self.grounded:
                gotNeighbor = cellZ
            elif (cellX + 1, cellZ) in self.grounded:
                gotNeighbor = cellZ
            elif (cellX, cellZ + 1) in self.grounded:
                gotNeighbor = cellZ + 1
            elif (cellX + 1, cellZ + 1) in self.grounded:
                gotNeighbor = cellZ + 1
            elif (cellX, cellZ - 1) in self.grounded:
                gotNeighbor = cellZ - 1
            elif (cellX + 1, cellZ - 1) in self.grounded:
                gotNeighbor = cellZ - 1
        elif (cellX - 1, cellZ) in self.grounded:
            gotNeighbor = cellZ
        elif (cellX + 1, cellZ) in self.grounded:
            gotNeighbor = cellZ
        elif (cellX, cellZ + 1) in self.grounded:
            gotNeighbor = cellZ + 1
        elif (cellX - 1, cellZ + 1) in self.grounded:
            gotNeighbor = cellZ + 1
        elif (cellX, cellZ - 1) in self.grounded:
            gotNeighbor = cellZ - 1
        elif (cellX - 1, cellZ - 1) in self.grounded:
            gotNeighbor = cellZ - 1
        return gotNeighbor

    def clearMatchList(self, typeClear=0):
        self.soundBurst.play()
        for entry in self.matchList:
            gridEntry = self.grid[entry[0]][entry[1]]
            sprite = gridEntry[0]
            if typeClear == self.wildIndex:
                self.questionSprite(sprite)
            elif typeClear == 0:
                pass
            self.killSprite(sprite)

    def shakeList(self, neighbors):
        for entry in neighbors:
            gridEntry = self.grid[entry[0]][entry[1]]
            sprite = gridEntry[0]
            self.shakeSprite(sprite)

    def createMatchList(self, x, z):
        self.matchList = []
        self.fillMatchList(x, z)

    def matchWild(self, x, z, color):
        spriteType = self.getColorType(x, z)
        if not self.getBreakable(x, z):
            return 0
        elif spriteType != -1 and spriteType == self.wildIndex:
            return 1
        elif spriteType != -1 and color == self.wildIndex:
            return 1
        else:
            return 0

    def bombNeighbors(self, cellX, cellZ):
        self.soundBomb.play()
        self.matchList = []
        if cellZ % 2 == 0:
            if self.getColorType(cellX - 1, cellZ) != -1:
                self.addToMatchList(cellX - 1, cellZ)
            if self.getColorType(cellX + 1, cellZ) != -1:
                self.addToMatchList(cellX + 1, cellZ)
            if self.getColorType(cellX, cellZ + 1) != -1:
                self.addToMatchList(cellX, cellZ + 1)
            if self.getColorType(cellX + 1, cellZ + 1) != -1:
                self.addToMatchList(cellX + 1, cellZ + 1)
            if self.getColorType(cellX, cellZ - 1) != -1:
                self.addToMatchList(cellX, cellZ - 1)
            if self.getColorType(cellX + 1, cellZ - 1) != -1:
                self.addToMatchList(cellX + 1, cellZ - 1)
        else:
            if self.getColorType(cellX - 1, cellZ) != -1:
                self.addToMatchList(cellX - 1, cellZ)
            if self.getColorType(cellX + 1, cellZ) != -1:
                self.addToMatchList(cellX + 1, cellZ)
            if self.getColorType(cellX, cellZ + 1) != -1:
                self.addToMatchList(cellX, cellZ + 1)
            if self.getColorType(cellX - 1, cellZ + 1) != -1:
                self.addToMatchList(cellX - 1, cellZ + 1)
            if self.getColorType(cellX, cellZ - 1) != -1:
                self.addToMatchList(cellX, cellZ - 1)
            if self.getColorType(cellX - 1, cellZ - 1) != -1:
                self.addToMatchList(cellX - 1, cellZ - 1)

    def addToMatchList(self, posX, posZ):
        if self.getBreakable(posX, posZ) > 0:
            self.matchList.append((posX, posZ))

    def getNeighbors(self, cellX, cellZ):
        neighborList = []
        if cellZ % 2 == 0:
            if self.getColorType(cellX - 1, cellZ) != -1:
                neighborList.append((cellX - 1, cellZ))
            if self.getColorType(cellX + 1, cellZ) != -1:
                neighborList.append((cellX + 1, cellZ))
            if self.getColorType(cellX, cellZ + 1) != -1:
                neighborList.append((cellX, cellZ + 1))
            if self.getColorType(cellX + 1, cellZ + 1) != -1:
                neighborList.append((cellX + 1, cellZ + 1))
            if self.getColorType(cellX, cellZ - 1) != -1:
                neighborList.append((cellX, cellZ - 1))
            if self.getColorType(cellX + 1, cellZ - 1) != -1:
                neighborList.append((cellX + 1, cellZ - 1))
        else:
            if self.getColorType(cellX - 1, cellZ) != -1:
                neighborList.append((cellX - 1, cellZ))
            if self.getColorType(cellX + 1, cellZ) != -1:
                neighborList.append((cellX + 1, cellZ))
            if self.getColorType(cellX, cellZ + 1) != -1:
                neighborList.append((cellX, cellZ + 1))
            if self.getColorType(cellX - 1, cellZ + 1) != -1:
                neighborList.append((cellX - 1, cellZ + 1))
            if self.getColorType(cellX, cellZ - 1) != -1:
                neighborList.append((cellX, cellZ - 1))
            if self.getColorType(cellX - 1, cellZ - 1) != -1:
                neighborList.append((cellX - 1, cellZ - 1))
        return neighborList

    def fillMatchList(self, cellX, cellZ):
        if (cellX, cellZ) in self.matchList:
            return
        self.matchList.append((cellX, cellZ))
        colorType = self.grid[cellX][cellZ][0].colorType
        if colorType == 4:
            return
        if cellZ % 2 == 0:
            if self.getColorType(cellX - 1, cellZ) == colorType or self.matchWild(cellX - 1, cellZ, colorType):
                self.fillMatchList(cellX - 1, cellZ)
            if self.getColorType(cellX + 1, cellZ) == colorType or self.matchWild(cellX + 1, cellZ, colorType):
                self.fillMatchList(cellX + 1, cellZ)
            if self.getColorType(cellX, cellZ + 1) == colorType or self.matchWild(cellX, cellZ + 1, colorType):
                self.fillMatchList(cellX, cellZ + 1)
            if self.getColorType(cellX + 1, cellZ + 1) == colorType or self.matchWild(cellX + 1, cellZ + 1, colorType):
                self.fillMatchList(cellX + 1, cellZ + 1)
            if self.getColorType(cellX, cellZ - 1) == colorType or self.matchWild(cellX, cellZ - 1, colorType):
                self.fillMatchList(cellX, cellZ - 1)
            if self.getColorType(cellX + 1, cellZ - 1) == colorType or self.matchWild(cellX + 1, cellZ - 1, colorType):
                self.fillMatchList(cellX + 1, cellZ - 1)
        else:
            if self.getColorType(cellX - 1, cellZ) == colorType or self.matchWild(cellX - 1, cellZ, colorType):
                self.fillMatchList(cellX - 1, cellZ)
            if self.getColorType(cellX + 1, cellZ) == colorType or self.matchWild(cellX + 1, cellZ, colorType):
                self.fillMatchList(cellX + 1, cellZ)
            if self.getColorType(cellX, cellZ + 1) == colorType or self.matchWild(cellX, cellZ + 1, colorType):
                self.fillMatchList(cellX, cellZ + 1)
            if self.getColorType(cellX - 1, cellZ + 1) == colorType or self.matchWild(cellX - 1, cellZ + 1, colorType):
                self.fillMatchList(cellX - 1, cellZ + 1)
            if self.getColorType(cellX, cellZ - 1) == colorType or self.matchWild(cellX, cellZ - 1, colorType):
                self.fillMatchList(cellX, cellZ - 1)
            if self.getColorType(cellX - 1, cellZ - 1) == colorType or self.matchWild(cellX - 1, cellZ - 1, colorType):
                self.fillMatchList(cellX - 1, cellZ - 1)

    def testGridfull(self, cell):
        if not cell:
            return 0
        elif cell[0] is not None:
            return 1
        else:
            return 0
        return

    def getValidGrid(self, x, z):
        if x < 0 or x >= self.gridDimX:
            return None
        elif z < 0 or z >= self.gridDimZ:
            return None
        else:
            return self.grid[x][z]
        return None

    def getColorType(self, x, z):
        if x < 0 or x >= self.gridDimX:
            return -1
        elif z < 0 or z >= self.gridDimZ:
            return -1
        elif self.grid[x][z][0] is None:
            return -1
        else:
            return self.grid[x][z][0].colorType
        return

    def getBreakable(self, x, z):
        if x < 0 or x >= self.gridDimX:
            return -1
        elif z < 0 or z >= self.gridDimZ:
            return -1
        elif self.grid[x][z][0] is None:
            return -1
        else:
            return self.grid[x][z][0].breakable
        return

    def findGridCog(self):
        self.cogX = 0
        self.cogZ = 0
        self.massCount = 0
        for row in self.grid:
            for cell in row:
                if cell[0] is not None:
                    self.cogX += cell[1]
                    self.cogZ += cell[2]
                    self.massCount += 1

        if self.massCount > 0:
            self.cogX = self.cogX / self.massCount
            self.cogZ = self.cogZ / self.massCount
            self.cogSprite.setX(self.cogX)
            self.cogSprite.setZ(self.cogZ)
        return

    def doOnClearGrid(self):
        self.winCounter += 1
        self.clearGrid()
        self.flagNextLevel = 1
        if self.winCounter > 4:
            self.__handleWin()

    def clearGrid(self):
        for row in self.grid:
            for cell in row:
                if cell[0] is not None:
                    self.killSprite(cell[0])
                cell[5].setColorScale(self.blankColor)

        self.killSprite(self.controlSprite)
        return

    def killSprite(self, sprite):
        if sprite is None:
            return
        if sprite.giftId is not None:
            self.giftId = sprite.giftId
        if sprite.foundation:
            self.foundCount -= 1
        if self.controlSprite == sprite:
            self.controlSprite = None
        if sprite in self.sprites:
            self.sprites.remove(sprite)
        if sprite.gridPosX is not None:
            self.grid[sprite.gridPosX][sprite.gridPosZ][0] = None
            self.grid[sprite.gridPosX][sprite.gridPosZ][5].setColorScale(self.blankColor)
            sprite.deathEffect()
        sprite.delete()
        self.hasChanged = 1
        return

    def shakeSprite(self, sprite):
        if sprite is None:
            return
        sprite.shake()
        return

    def questionSprite(self, sprite):
        newSprite = self.addSprite(self.block, found=0, color=1)
        newSprite.setX(sprite.getX())
        newSprite.setZ(sprite.getZ())
        newSprite.wildEffect()

    def colorGrid(self):
        for row in self.grid:
            for cell in row:
                if cell[0] is not None:
                    if cell[0].colorType == 3:
                        cell[5].setColorScale(self.blackColor)
                    else:
                        cell[5].setColorScale(self.fullColor)
                elif cell[4] <= self.spriteNotchPos:
                    cell[5].setColorScale(self.outColor)
                elif self.hasNeighbor(cell[3], cell[4]):
                    cell[5].setColorScale(self.neighborColor)
                else:
                    cell[5].setColorScale(self.blankColor)

        return

    def findPos(self, x, z):
        return (self.grid[x][z][1], self.grid[x][z][2])

    def placeIntoGrid(self, sprite, x, z):
        if self.grid[x][z][0] is None:
            self.grid[x][z][0] = sprite
            sprite.gridPosX = x
            sprite.gridPosZ = z
            sprite.setActive(0)
            newX, newZ = self.findPos(x, z)
            sprite.setX(newX)
            sprite.setZ(newZ)
            if sprite == self.controlSprite:
                self.controlSprite = None
            self.colorGridFlag = 1
            self.hasChanged = 1
            self.findGridCog()
            self.checkForTooLow()
        else:
            self.placeIntoGrid(sprite, x + 1, z - 1)
        return

    def stickInGrid(self, sprite, force=0):
        if sprite.isActive:
            gridCell = self.findGrid(sprite.getX(), sprite.getZ(), force)
            if gridCell:
                colorType = sprite.colorType
                sprite.setActive(0)
                self.soundLand.play()
                self.placeIntoGrid(sprite, gridCell[3], gridCell[4])
                if colorType == self.bombIndex:
                    kapow = MovieUtil.createKapowExplosionTrack(render, sprite.nodeObj.getPos(render))
                    kapow.start()
                    self.bombNeighbors(self.closestX, self.closestZ)
                    allNeighbors = []
                    for entry in self.matchList:
                        neighbors = self.getNeighbors(entry[0], entry[1])
                        for neighbor in neighbors:
                            if neighbor not in allNeighbors and neighbor not in self.matchList:
                                allNeighbors.append(neighbor)

                    self.shakeList(allNeighbors)
                    self.clearMatchList()
                else:
                    self.createMatchList(self.closestX, self.closestZ)
                    if len(self.matchList) >= 3:
                        clearType = 0
                        self.clearMatchList(colorType)
                    else:
                        neighbors = self.getNeighbors(self.closestX, self.closestZ)
                        self.shakeList(neighbors)

    def addSprite(self, image, size=3.0, posX=0, posZ=0, found=0, color=None):
        spriteBase = self.spriteNode.attachNewNode('sprite base')
        size = self.radiusBall * 2.0
        facing = 1
        if color is None:
            colorChoice = random.choice(list(range(0, 3)))
        else:
            colorChoice = color
        newSprite = GameSprite3D.GameSprite(spriteBase, size, colorChoice, found, facing)
        newSprite.setX(posX)
        newSprite.setZ(posZ)
        self.sprites.append(newSprite)
        if found:
            self.foundCount += 1
        return newSprite

    def addControlSprite(self, x=0.0, z=0.0, color=None):
        newSprite = self.addSprite(self.block, posX=x, posZ=z, color=color, found=1)
        newSprite.spriteBase.reparentTo(self.frame)
        newSprite.spriteBase.setPos(0.0, 0.7, -1.54)
        self.controlSprite = newSprite

    def addUnSprite(self, image, size=3.0, posX=0, posZ=0):
        size = self.radiusBall * 2.0
        spriteBase = self.spriteNode.attachNewNode('sprite base')
        newSprite = GameSprite3D.GameSprite(spriteBase, size)
        newSprite.setX(posX)
        newSprite.setZ(posZ)
        return newSprite

    def __handleMouseClick(self):
        if self.ballLoaded and self.controlSprite:
            self.controlSprite.spriteBase.wrtReparentTo(self.spriteNode)
            self.controlSprite.setAccel(14.0, pi * 0.0 - self.aimRadian)
            self.controlSprite.setActive(1)
            self.soundFire.play()
            self.ballLoaded = 0

    def __run(self, cont=1):
        if cont and not self.running:
            taskMgr.add(self.__run, 'GolfGreenGameTask')
            self.running = 1
        if self.lastTime is None:
            self.lastTime = base.clock.getRealTime()
        timeDelta = base.clock.getRealTime() - self.lastTime
        self.lastTime = base.clock.getRealTime()
        self.newBallCountUp += timeDelta
        if base.mouseWatcherNode.hasMouse():
            inputX = base.mouseWatcherNode.getMouseX()
            inputZ = base.mouseWatcherNode.getMouseY()
            outputZ = inputZ + self.screenSizeZ * (0.5 - self.zGap)
            if outputZ <= 0.0:
                outputZ = 0.0001
            if inputX > 0.0:
                self.aimRadian = -1.0 * pi + math.atan(outputZ / (inputX * self.XtoZ))
            elif inputX < 0.0:
                self.aimRadian = math.atan(outputZ / (inputX * self.XtoZ))
            else:
                self.aimRadian = pi * -0.5
            margin = 0.2
            if self.aimRadian >= -margin:
                self.aimRadian = -margin
            elif self.aimRadian <= margin - pi:
                self.aimRadian = margin - pi
            degrees = self.__toDegrees(self.aimRadian)
            self.aimer.setH(degrees)
        self.wallMaxX = self.maxX - self.radiusBall
        self.wallMinX = self.minX + self.radiusBall
        self.wallMaxZ = self.maxZ - self.radiusBall
        self.wallMinZ = self.minZ + self.radiusBall
        if self.controlSprite and self.controlSprite.nodeObj.isEmpty():
            self.controlSprite = None
        if self.giftId:
            self.ballLoaded = 2
            self.updateSpritePos()
            self.standbySprite.holdType = self.giftId
            self.standbySprite.setBallType(self.giftId, 1)
            self.standbySprite.face()
            self.giftId = None
        while self.controlSprite is None and self.attackPattern:
            if self.attackCounter > len(self.attackPattern) - 1:
                self.attackCounter = 0
            if self.standbySprite.holdType is not None:
                color = self.standbySprite.holdType
                self.addControlSprite(self.newBallX, self.newBallZ + self.spriteNotchPos * self.cellSizeZ, color)
            self.ballLoaded = 1
            self.updateSpritePos()
            newColor = self.predictAttackPattern(0)
            self.standbySprite.holdType = newColor
            self.standbySprite.setBallType(newColor, 1)
            self.standbySprite.face()
            self.attackCounter += 1

        self.standbySprite.runColor(timeDelta)
        for sprite in self.sprites:
            if sprite.deleteFlag:
                self.sprites.remove(sprite)
            else:
                sprite.run(timeDelta)
                if sprite.getX() > self.wallMaxX:
                    sprite.setX(self.wallMaxX)
                    sprite.reflectX()
                if sprite.getX() < self.wallMinX:
                    sprite.setX(self.wallMinX)
                    sprite.reflectX()
                if sprite.getZ() > self.wallMaxZ:
                    self.stickInGrid(sprite, 1)
                if sprite.getZ() < self.wallMinZ:
                    pass

        self.__colTest()
        if self.hasChanged and self.running:
            self.clearFloaters()
            self.explodeBombs()
            self.findGridCog()
            spriteCount = 0
            whiteCount = 0
            for row in self.grid:
                for cell in row:
                    if cell[0] is not None:
                        self.cogX += cell[1]
                        self.cogZ += cell[2]
                        spriteCount += 1
                        if cell[0].colorType == 3:
                            whiteCount += 1

            if whiteCount == 0:
                self.__finishBoard(win=True)
                self.flagNextLevel = 0
                self.killSprite(self.controlSprite)
                self.standbySprite.holdType = None
            self.colorGridFlag = 1
        self.hasChanged = 0
        if self.colorGridFlag:
            self.colorGridFlag = 0
            self.colorGrid()
        return Task.cont

    def predictAttackPattern(self, numSteps=1):
        predict = self.attackCounter + numSteps
        predict = predict % len(self.attackPattern)
        return self.attackPattern[predict]

    def __stop(self):
        taskMgr.remove('GolfGreenGameTask')
        self.running = 0

    def __toRadians(self, angle):
        return angle * 2.0 * math.pi / 360.0

    def __toDegrees(self, angle):
        return angle * 360.0 / (2.0 * math.pi)

    def __colTest(self):
        if not hasattr(self, 'tick'):
            self.tick = 0
        self.tick += 1
        if self.tick > 5:
            self.tick = 0
        sizeSprites = len(self.sprites)
        for movingSpriteIndex in range(len(self.sprites)):
            for testSpriteIndex in range(movingSpriteIndex, len(self.sprites)):
                movingSprite = self.getSprite(movingSpriteIndex)
                testSprite = self.getSprite(testSpriteIndex)
                if testSprite and movingSprite:
                    if movingSpriteIndex != testSpriteIndex and (movingSprite.isActive or testSprite.isActive):
                        if self.testDistance(movingSprite.spriteBase, testSprite.spriteBase) < self.radiusBall * 1.65:
                            if not (movingSprite.isActive and testSprite.isActive):
                                if movingSprite.canCollide and testSprite.canCollide:
                                    self.__collide(movingSprite, testSprite)
                        if self.tick == 5:
                            pass

    def getSprite(self, spriteIndex):
        if spriteIndex >= len(self.sprites) or self.sprites[spriteIndex].markedForDeath:
            return None
        else:
            return self.sprites[spriteIndex]

    def testDistance(self, nodeA, nodeB):
        if nodeA.isEmpty() or nodeB.isEmpty():
            return 10000
        distX = nodeA.getX() - nodeB.getX()
        distZ = nodeA.getZ() - nodeB.getZ()
        distC = distX * distX + distZ * distZ
        dist = math.sqrt(distC)
        return dist

    def testPointDistance(self, x1, z1, x2, z2):
        distX = x1 - x2
        distZ = z1 - z2
        distC = distX * distX + distZ * distZ
        dist = math.sqrt(distC)
        if dist == 0:
            dist = 1e-10
        return dist

    def testPointDistanceSquare(self, x1, z1, x2, z2):
        distX = x1 - x2
        distZ = z1 - z2
        distC = distX * distX + distZ * distZ
        if distC == 0:
            distC = 1e-10
        return distC

    def angleTwoSprites(self, sprite1, sprite2):
        x1 = sprite1.getX()
        z1 = sprite1.getZ()
        x2 = sprite2.getX()
        z2 = sprite2.getZ()
        x = x2 - x1
        z = z2 - z1
        angle = math.atan2(-x, z)
        return angle + pi * 0.5

    def angleTwoPoints(self, x1, z1, x2, z2):
        x = x2 - x1
        z = z2 - z1
        angle = math.atan2(-x, z)
        return angle + pi * 0.5

    def __collide(self, move, test):
        test.velX = 0
        test.velZ = 0
        move.velX = 0
        move.velZ = 0
        test.collide()
        move.collide()
        self.stickInGrid(move)
        self.stickInGrid(test)

    def __setCamera(self):
        camera.setPos(0, 0, 0)
        camera.setH(0)
        camera.setP(-70)
        camera.reparentTo(self.focusPoint)
        base.camLens.setMinFov(46.8265)
        self.focusPoint.setPos(0, 12, 27)
        self.focusPoint.setH(180)

    def boardCleared(self, avId):
        self.doFail()

    def scoreData(self, scoreList):
        for avId, score in scoreList:
            p: MinigameAvatarScorePanel = self.scorePanels[avId]
            p.setScore(score)

    def helpOthers(self, avId):
        if avId != localAvatar.doId and self.running:
            self.giftId = 7
            toonName = ''
            toon = base.cr.doId2do[avId]
            if toon:
                toonName = toon.getName()
            self.bonusBoard['text'] = TTLocalizer.GolfGreenGameGotHelp % toonName
            imageBall = loader.loadModel('phase_12/models/bossbotHQ/bust_a_cog_ball_fire')
            imageBall.setHpr(0, 90, 0)
            self.bonusBoard['image'] = imageBall
            self.bonusBoard['image_scale'] = 0.13
            self.bonusBoard.show()
            taskMgr.doMethodLater(4.0, self.hideBonusBoard, 'hide bonus')

    def hideBonusBoard(self, task):
        if self.bonusBoard:
            if not self.bonusBoard.isEmpty():
                self.bonusBoard.hide()
