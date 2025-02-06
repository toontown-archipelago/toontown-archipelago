import math
import random
import typing

from direct.directnotify import DirectNotifyGlobal

from toontown.toonbase import ToontownGlobals

if typing.TYPE_CHECKING:
    from toontown.minigame.craning.DistributedCraneGameAI import DistributedCraneGameAI


class CraneGamePracticeCheatAI:

    notify = DirectNotifyGlobal.directNotify.newCategory("CraneGameSafeAimCheatAI")

    # Practice modes
    RNG_MODE = 1
    SAFE_RUSH_PRACTICE = 2
    LIVE_GOON_PRACTICE = 3
    AIM_PRACTICE = 4

    """
    Activated via magic words when cheats are enabled for a crane game minigame.
    Provides various methods of practicing in the crane round.
    """
    def __init__(self, game: "DistributedCraneGameAI"):
        self.game = game
        self.numSafesWanted = 0

        # Practice mode bools
        self.wantRNGMode = False
        self.wantSafeRushPractice = False
        self.wantLiveGoonPractice = False
        self.wantAimPractice = False

        # Practice mode parameters
        self.wantOpeningModifications = False
        self.openingModificationsToonIndex = 0
        self.wantMaxSizeGoons = False
        self.wantStunning = False
        self.wantNoStunning = False
        self.wantFasterGoonSpawns = False
        self.wantAlwaysStunned = False

    def setPracticeParams(self, practiceMode):

        # If we are setting a practice mode, we probably don't want the timer!
        if practiceMode is not None:
            self.__pauseTimer()

        # Get current state of requested mode before disabling all
        if practiceMode == self.RNG_MODE:
            currentState = self.wantRNGMode
        elif practiceMode == self.SAFE_RUSH_PRACTICE:
            currentState = self.wantSafeRushPractice
        elif practiceMode == self.LIVE_GOON_PRACTICE:
            currentState = self.wantLiveGoonPractice
        elif practiceMode == self.AIM_PRACTICE:
            currentState = self.wantAimPractice
        else:
            currentState = False

        # Disable all practice modes
        self.wantRNGMode = False
        self.wantSafeRushPractice = False
        self.wantLiveGoonPractice = False
        self.wantAimPractice = False

        # Disable all practice parameters
        self.wantOpeningModifications = False
        self.wantMaxSizeGoons = False
        self.wantStunning = False
        self.wantNoStunning = False
        self.wantFasterGoonSpawns = False
        self.wantAlwaysStunned = False

        # Toggle the requested mode to opposite of its previous state
        if practiceMode == self.RNG_MODE:
            self.wantRNGMode = not currentState
        elif practiceMode == self.SAFE_RUSH_PRACTICE:
            self.wantSafeRushPractice = not currentState
        elif practiceMode == self.LIVE_GOON_PRACTICE:
            self.wantLiveGoonPractice = not currentState
        elif practiceMode == self.AIM_PRACTICE:
            self.wantAimPractice = not currentState

        # Enable the requested mode's params
        if self.wantRNGMode:
            self.wantOpeningModifications = True
            self.wantMaxSizeGoons = True
        elif self.wantSafeRushPractice:
            self.wantStunning = True
        elif self.wantLiveGoonPractice:
            self.wantNoStunning = True
            self.openingModificationsToonIndex = 0
            self.wantFasterGoonSpawns = True
        elif self.wantAimPractice:
            self.wantAlwaysStunned = True
            self.setupAimMode()

    def setupAimMode(self):
        # Initial setup for aim mode - stun CFO and remove goons
        self.game.getBoss().stopHelmets()
        self.game.getBoss().b_setAttackCode(ToontownGlobals.BossCogDizzy)
        taskMgr.remove(self.game.uniqueName('NextGoon'))
        for goon in self.game.goons:
            goon.request('Off')
            goon.requestDelete()
        self.__pauseTimer()

    def __pauseTimer(self):
        self.notify.debug("Pausing timer")
        taskMgr.remove(self.game.uniqueName('times-up-task'))
        self.game.d_updateTimer()

    def handleSafeDropped(self, safe):
        if not self.wantAimPractice:
            return

        # Get the first toon's position
        players = self.game.getParticipantsNotSpectating()
        if len(players) == 0:
            return
        toon = players[0]

        toonX = toon.getPos().x
        toonY = toon.getPos().y

        # Calculate progressive distance for repositioning
        battleTime = globalClock.getFrameTime() - self.game.battleThreeStart
        repositionDistance = self.game.progressValue(8, 28)  # Start at 8 units, progress to 28 units

        # First count how many safes are already nearby (always check within 35 units)
        checkDistance = 35
        nearbySafes = set()  # Using a set for faster lookup
        for potentialSafe in self.game.safes:
            if potentialSafe.index != 0 and potentialSafe.state in ['Free', 'Initial']:  # Not the helmet safe
                safeX = potentialSafe.getPos().x
                safeY = potentialSafe.getPos().y
                distance = math.sqrt((toonX - safeX) ** 2 + (toonY - safeY) ** 2)
                if distance <= checkDistance:
                    nearbySafes.add(potentialSafe)

        # If we already have enough nearby safes, don't reposition any
        if len(nearbySafes) >= self.numSafesWanted:
            return

        # Find available safes (not grabbed, not dropped, not helmet, not already nearby)
        availableSafes = []
        for potentialSafe in self.game.safes:
            if (potentialSafe.index != 0 and  # Not the helmet safe
                    potentialSafe.state in ['Free', 'Initial'] and  # Only free or initial safes
                    potentialSafe != safe and  # Not the safe that was just dropped
                    potentialSafe not in nearbySafes):  # Not already nearby
                safeX = potentialSafe.getPos().x
                safeY = potentialSafe.getPos().y
                distance = math.sqrt((toonX - safeX) ** 2 + (toonY - safeY) ** 2)
                availableSafes.append((distance, potentialSafe))

        # Sort safes by distance (furthest first)
        availableSafes.sort(reverse=True)

        # Calculate how many safes we need to reposition
        safesNeeded = self.numSafesWanted - len(nearbySafes)
        safesToMove = availableSafes[:safesNeeded]  # Take only as many as we need

        # Reposition each safe
        for _, safeToMove in safesToMove:
            self.repositionSafe(safeToMove, toonX, toonY, repositionDistance)

    def checkSafePosition(self, x, y, safes):
        # Safe radius is approximately 4 units (collision sphere is about 8 units)
        safeRadius = 4.0
        for safe in safes:
            if safe.state not in ['Free', 'Initial']:
                continue
            safeX = safe.getPos().x
            safeY = safe.getPos().y
            distance = math.sqrt((x - safeX) ** 2 + (y - safeY) ** 2)
            if distance < (safeRadius * 2):  # Multiply by 2 to account for both safes' radii
                return False
        return True

    def repositionSafe(self, safe, toonX, toonY, nearbyDistance):
        # Keep trying new angles until we find a position in bounds and not colliding
        maxAttempts = 20
        for _ in range(maxAttempts):
            angle = random.random() * 2.0 * math.pi
            x = toonX + nearbyDistance * math.cos(angle)
            y = toonY + nearbyDistance * math.sin(angle)

            # Check if position is within the octagonal battle area and not colliding with other safes
            if self.isLocationInBounds(x, y) and self.checkSafePosition(x, y, [s for s in self.game.safes if s != safe]):
                z = 0  # Height will be adjusted by physics
                if safe.state == 'Initial':
                    safe.demand('Free')  # Transition from Initial to Free state
                safe.move(x, y, z, 360 * random.random())  # Use move instead of setPos for proper synchronization
                return

        # If we failed to find a valid position after all attempts, try with a smaller radius
        nearbyDistance *= 0.75  # Try with 75% of the distance
        for _ in range(maxAttempts):
            angle = random.random() * 2.0 * math.pi
            x = toonX + nearbyDistance * math.cos(angle)
            y = toonY + nearbyDistance * math.sin(angle)

            if self.isLocationInBounds(x, y) and self.checkSafePosition(x, y, [s for s in self.game.safes if s != safe]):
                z = 0
                if safe.state == 'Initial':
                    safe.demand('Free')
                safe.move(x, y, z, 360 * random.random())
                return

        # If we still can't find a valid position, place it very close to the toon
        nearbyDistance = 5  # Very close radius as last resort
        angle = random.random() * 2.0 * math.pi
        x = toonX + nearbyDistance * math.cos(angle)
        y = toonY + nearbyDistance * math.sin(angle)

        # Final position must be within the octagonal bounds
        if not self.isLocationInBounds(x, y):
            x = toonX
            y = toonY

        z = 0
        if safe.state == 'Initial':
            safe.demand('Free')
        safe.move(x, y, z, 360 * random.random())

    # Probably a better way to do this but o well
    # Checking each line of the octogon to see if the location is outside
    def isLocationInBounds(self, x, y):
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