from toontown.coghq import CraneLeagueGlobals
from toontown.safezone import DistributedSZTreasureAI, DistributedTreasureAI
from toontown.toonbase import ToontownGlobals


class DistributedCashbotBossTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, boss, goon, style, fx, fy, fz):
        pos = goon.getPos()
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air, boss, pos[0], pos[1], 0)
        self.goonId = goon.doId
        self.style = style
        self.finalPosition = (fx, fy, fz)
        self.responsibleAv = None  # The toonId who spawned this treasure

    def setResponsibleAv(self, avId):
        self.responsibleAv = avId

    def getGoonId(self):
        return self.goonId

    def setGoonId(self, goonId):
        self.goonId = goonId

    def b_setGoonId(self, goonId):
        self.setGoonId(goonId)
        self.d_setGoonId(goonId)

    def d_setGoonId(self, goonId):
        self.sendUpdate('setGoonId', [goonId])

    def getStyle(self):
        return self.style

    def setStyle(self, hoodId):
        self.style = hoodId

    def b_setStyle(self, hoodId):
        self.setStyle(hoodId)
        self.d_setStyle(hoodId)

    def d_setStyle(self, hoodId):
        self.sendUpdate('setStyle', [hoodId])

    def getFinalPosition(self):
        return self.finalPosition

    def setFinalPosition(self, x, y, z):
        self.finalPosition = (x, y, z)

    def b_setFinalPosition(self, x, y, z):
        self.setFinalPosition(x, y, z)
        self.d_setFinalPosition(x, y, z)

    def d_setFinalPosition(self, x, y, z):
        self.sendUpdate('setFinalPosition', [x, y, z])

    def d_setGrab(self, avId):
        DistributedTreasureAI.DistributedTreasureAI.d_setGrab(self, avId)
        if avId in self.air.doId2do:
            av = self.air.doId2do[avId]
            if av.hp > 0 and av.hp < av.maxHp:

                hp = min(self.healAmount, av.maxHp - av.hp)
                goon = self.air.doId2do.get(self.goonId)
                if not goon:
                    av.toonUp(hp)
                    return

                boss = goon.boss
                boss.toonHealedFromTreasure(avId, self.responsibleAv, hp)
                # Are we deducting points?
                if boss.ruleset.TREASURE_POINT_PENALTY:

                    # check if we are tooning up less than heal amount
                    amount = self.healAmount
                    laffMissing = av.maxHp - av.hp
                    if laffMissing < amount:
                        amount = laffMissing

                    # Is there just a flat rate defined?
                    if boss.ruleset.TREASURE_POINT_PENALTY_FLAT_RATE > 0:
                        amount = boss.ruleset.TREASURE_POINT_PENALTY_FLAT_RATE

                    self.sendUpdate('deductScoreboardPoints', [avId, -amount])

                av.toonUp(self.healAmount)


