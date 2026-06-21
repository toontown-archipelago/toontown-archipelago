from toontown.estate import GardenKitGlobals

class GardenKitManagerAI:
    def __init__(self, air):
        self.air = air

    def awardGardenKit(self, avId):
        av = self.air.doId2do.get(avId)
        if not av:
            return

        gardenKit = av.getGardenKit()
        shovelSkill = av.getShovelSkill()
        wateringCanSkill = av.getWateringCanSkill()

        if gardenKit == GardenKitGlobals.PRO_GARDEN_KIT:
            return

       # TODO - Implement logic to award the next garden kit
       pass