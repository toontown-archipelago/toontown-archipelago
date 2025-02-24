from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.battle import BattlePlace
from toontown.building import Elevator
from toontown.toonbase import ToontownGlobals
from panda3d.core import *
from libotp import *
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.content_pack import MusicManagerGlobals

class CogHQLobby(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('CogHQLobby')

    def __init__(self, hood, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, hood, doneEvent)
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = 'elevatorDone'
        self.fsm = ClassicFSM.ClassicFSM('CogHQLobby', [State.State('start', self.enterStart, self.exitStart, ['walk',
          'tunnelIn',
          'teleportIn',
          'doorIn']),
         State.State('walk', self.enterWalk, self.exitWalk, ['elevator',
          'DFA',
          'doorOut',
          'stopped']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'teleportOut', 'elevator']),
         State.State('doorIn', self.enterDoorIn, self.exitDoorIn, ['walk']),
         State.State('doorOut', self.enterDoorOut, self.exitDoorOut, ['walk']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk']),
         State.State('elevator', self.enterElevator, self.exitElevator, ['walk', 'stopped']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walk']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')

    def load(self):
        self.parentFSM.getStateNamed('cogHQLobby').addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)

    def unload(self):
        self.parentFSM.getStateNamed('cogHQLobby').removeChild(self.fsm)
        BattlePlace.BattlePlace.unload(self)
        self.fsm = None
        return

    def enter(self, requestStatus):
        self.zoneId = requestStatus['zoneId']
        base.discord.setZone(self.zoneId)
        BattlePlace.BattlePlace.enter(self)
        self.fsm.enterInitialState()
        self.music = MusicManagerGlobals.GLOBALS[self.zoneId]['music']
        self.battleMusic = MusicManagerGlobals.GLOBALS[self.zoneId]['battleMusic']
        self.loader.geom.reparentTo(render)
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        NametagGlobals.setMasterArrowsOn(1)
        how = requestStatus['how']
        self.fsm.request(how, [requestStatus])
        self._telemLimiter = TLGatherAllAvs('CogHQLobby', RotationLimitToH)
        base.contentPackMusicManager.playMusic(self.music, looping=1, volume=0.8, interrupt=True)

    def exit(self):
        self._telemLimiter.destroy()
        del self._telemLimiter
        self.fsm.requestFinalState()
        self.ignoreAll()
        if self.loader.geom != None:
            self.loader.geom.reparentTo(hidden)
        BattlePlace.BattlePlace.exit(self)
        return

    def enterWalk(self, teleportIn = 0):
        BattlePlace.BattlePlace.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    def enterElevator(self, distElevator, skipDFABoard = 0):
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed('elevator'), self.elevatorDoneEvent, distElevator)
        if skipDFABoard:
            self.elevator.skipDFABoard = 1
        distElevator.elevatorFSM = self.elevator
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        self.fsm.request('elevator', [distElevator])

    def handleElevatorDone(self, doneStatus):
        self.notify.debug('handling elevator done event')
        where = doneStatus['where']
        if where == 'reject':
            if hasattr(base.localAvatar, 'elevatorNotifier') and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'cogHQBossBattle':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleElevatorDone')

    def enterTeleportIn(self, requestStatus):
        base.localAvatar.setPosHpr(render, 0, 0, 0, 0, 0, 0)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)
