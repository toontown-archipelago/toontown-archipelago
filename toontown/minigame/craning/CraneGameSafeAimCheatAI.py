import math
import random
import typing

from direct.directnotify import DirectNotifyGlobal

from toontown.toonbase import ToontownGlobals

if typing.TYPE_CHECKING:
    from toontown.minigame.craning.DistributedCraneGameAI import DistributedCraneGameAI


class CraneGameSafeAimCheatAI:

    notify = DirectNotifyGlobal.directNotify.newCategory("CraneGameSafeAimCheatAI")

    """
    Activated via magic words when cheats are enabled for a crane game minigame.
    Teleports safes to the first crane every so often when active.
    """
    def __init__(self, game: "DistributedCraneGameAI"):
        self.game = game
        self.numSafesWanted = 0
        self.enabled = False

    def isEnabled(self) -> bool:
        return self.enabled

    def enable(self, safes: int = 4):
        self.numSafesWanted = safes
        self.__stopCheckNearby()
        self.__pauseTimer()
        self.__checkNearby()
        self.enabled = True
        self.notify.debug(f'Enabled cheat with {self.numSafesWanted} safes')

    def disable(self):
        self.__stopCheckNearby()
        self.enabled = False
        self.notify.debug('Cleaned up cheat')

    def __pauseTimer(self):
        self.notify.debug("Pausing timer")
        taskMgr.remove(self.game.uniqueName('times-up-task'))
        craneTime = globalClock.getFrameTime()
        actualTime = craneTime - self.game.battleThreeStart
        self.game.d_updateTimer(actualTime)

    def __findToon(self):
        participants = self.game.getParticipantsNotSpectating()
        if len(participants) <= 0:
            return None
        return participants[0]

    def __checkNearby(self, task=None):
        # Prevent helmets, stun CFO, destroy goons
        self.game.getBoss().stopHelmets()
        self.game.getBoss().b_setAttackCode(ToontownGlobals.BossCogDizzy)

        self.notify.debug(f"Deleting {len(self.game.goons)} goons")
        for goon in self.game.goons:
            goon.request('Off')
            goon.requestDelete()

        nearbyDistance = 22

        # Get the toon's position
        toon = self.__findToon()
        if not toon:
            self.notify.warning('Unable to find toon nearby. Trying again in 4 seconds...')
            taskName = self.game.uniqueName('CheckNearbySafes')
            taskMgr.doMethodLater(4, self.__checkNearby, taskName)
            return

        toonX = toon.getX()
        toonY = toon.getY()
        self.notify.debug(f"Found toon at x={toonX} y={toonY}")

        # Count nearby safes
        nearbySafes = []
        farSafes = []
        farDistances = []
        self.notify.debug(f"Checking {len(self.game.safes)} safes")
        for safe in self.game.safes:
            # Safe on his head doesn't count and is not a valid target to move
            if self.game.getBoss().heldObject is safe:
                self.notify.debug(f"Safe {safe.doId} is being worn, skipping")
                continue

            safeX = safe.getPos().x
            safeY = safe.getPos().y

            distance = math.sqrt((toonX - safeX) ** 2 + (toonY - safeY) ** 2)
            if distance <= nearbyDistance:
                nearbySafes.append(safe)
            else:
                farDistances.append(distance)
                farSafes.append(safe)

        # Sort the possible safes by their distance away from us
        farSafes = [x for y, x in sorted(zip(farDistances, farSafes), reverse=True)]
        self.notify.debug(f'There are {len(farSafes)} safes far away from target toon')

        # If there's not enough nearby safes, relocate far ones
        if len(nearbySafes) < self.numSafesWanted:
            self.notify.debug(f"Need more safes, teleporting {self.numSafesWanted - len(nearbySafes)} safes to toon")
            self.__relocateSafes(farSafes, self.numSafesWanted - len(nearbySafes), toonX, toonY)

        # Schedule this to be done again in 1s unless the user stops it
        self.notify.debug(f"Scheduling another check in 4 seconds")
        taskName = self.game.uniqueName('CheckNearbySafes')
        taskMgr.doMethodLater(4, self.__checkNearby, taskName)

    def __stopCheckNearby(self):
        taskName = self.game.uniqueName('CheckNearbySafes')
        taskMgr.remove(taskName)

    def __relocateSafes(self, farSafes, numRelocate, toonX, toonY):
        for safe in farSafes[:numRelocate]:
            randomDistance = 22 * random.random()
            randomAngle = 2 * math.pi * random.random()
            newX = toonX + randomDistance * math.cos(randomAngle)
            newY = toonY + randomDistance * math.sin(randomAngle)
            while not self.__isLocationInBounds(newX, newY):
                randomDistance = 22 * random.random()
                randomAngle = 2 * math.pi * random.random()
                newX = toonX + randomDistance * math.cos(randomAngle)
                newY = toonY + randomDistance * math.sin(randomAngle)

            safe.move(newX, newY, 0, 360 * random.random())

    # Probably a better way to do this but o well
    # Checking each line of the octogon to see if the location is outside
    def __isLocationInBounds(self, x, y):
        if x > 165.7:
            return False
        if x < 77.1:
            return False
        if y > -274.1:
            return False
        if y < -359.1:
            return False

        if y - 0.936455 * x > -374.901:
            return False
        if y + 0.973856 * x < -254.118:
            return False
        if y - 1.0283 * x < -496.79:
            return False
        if y + 0.884984 * x > -155.935:
            return False

        return True
