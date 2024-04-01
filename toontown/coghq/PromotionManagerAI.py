from otp.ai.AIBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
import random
from toontown.suit import SuitDNA
from . import CogDisguiseGlobals
from functools import reduce
MeritMultiplier = 5.0

class PromotionManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('PromotionManagerAI')

    def __init__(self, air):
        self.air = air

    def recoverMerits(self, av, cogList, zoneId, multiplier = 1, extraMerits = None):
        avId = av.getDoId()
        meritsRecovered = [0, 0, 0, 0]
        if extraMerits is None:
            extraMerits = [0, 0, 0, 0]

        for i in range(len(extraMerits)):
            if CogDisguiseGlobals.isSuitComplete(av.getCogParts(), i):
                meritsRecovered[i] += extraMerits[i]
                self.notify.debug('recoverMerits: extra merits = %s' % extraMerits[i])

        self.notify.debug('recoverMerits: multiplier = %s' % multiplier)

        for cogDict in cogList:
            dept = SuitDNA.suitDepts.index(cogDict['track'])

            # Virtual cogs don't give merits
            if cogDict['isVirtual']:
                continue

            # Toon needed to participate in the killing of this cog
            if avId not in cogDict['activeToons']:
                continue

            self.notify.debug('recoverMerits: checking against cogDict: %s' % cogDict)

            # Toon needs a disguise to recover merits
            if not CogDisguiseGlobals.isSuitComplete(av.getCogParts(), SuitDNA.suitDepts.index(cogDict['track'])):
                continue

            level = cogDict['level'] if cogDict['level'] is not None else 0
            merits = level * MeritMultiplier
            merits = int(round(merits))
            if cogDict['hasRevives']:
                merits *= 2
            merits = merits * multiplier
            merits = int(round(merits))
            meritsRecovered[dept] += merits
            self.notify.debug('recoverMerits: merits = %s' % merits)

        # We got no merits womp womp
        if sum(meritsRecovered) <= 0:
            return meritsRecovered

        actualCounted = [0, 0, 0, 0]
        merits = av.getCogMerits()
        for i in range(len(meritsRecovered)):
            max = CogDisguiseGlobals.getTotalMerits(av, i)
            if max:
                if merits[i] + meritsRecovered[i] <= max:
                    actualCounted[i] = meritsRecovered[i]
                    merits[i] += meritsRecovered[i]
                else:
                    actualCounted[i] = max - merits[i]
                    merits[i] = max
                av.b_setCogMerits(merits)

        if reduce(lambda x, y: x + y, actualCounted):
            self.air.writeServerEvent('merits', avId, '%s|%s|%s|%s' % tuple(actualCounted))
            self.notify.debug('recoverMerits: av %s recovered merits %s' % (avId, actualCounted))

        return meritsRecovered
