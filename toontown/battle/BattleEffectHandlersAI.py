from direct.directnotify import DirectNotifyGlobal
from direct.showbase.MessengerGlobal import messenger

from toontown.battle.BattleCalculationObjectAI import BattleCalculationObjectAI
from toontown.toonbase.ToontownBattleGlobals import *

class BattleEffectHandlerAI(BattleCalculationObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleEffectHandlerAI')
    
    def __init__(self, battle, av):
        BattleCalculationObjectAI.__init__(self, battle)
        self.av = av
    
    def addEffect(self, className):
        effect = eval(className)(self.battle, self.av, self)
        self.addChild(effect.children['name'], effect)
    
    def removeEffect(self, name):
        self.removeChild(name)
    
    def tick(self, timing):
        for child in self.children.values():
            if child.children['timing'] == timing:
                child.tick()

class BattleEffectAI(BattleCalculationObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleEffectAI')
    
    def __init__(self, battle, av, handler):
        BattleCalculationObjectAI.__init__(self, battle)
        self.av = av
        self.handler = handler
        self.addChild('timer', 3)
        self.addChild('name', 'default')
        self.addChild('value', 0)
        self.addChild('timing', 0)
    
    def startEffect(self):
        pass
    
    def tick(self):
        self.children['timer'] -= 1
        if self.children['timer'] <= 0:
            if self.children['timer'] != -1:
                self.handler.removeChild(self.children['name'])

class BattleEffectExtraDamageAI(BattleCalculationObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleEffectExtraDamageAI')
    
    def __init__(self, battle, av, handler):
        BattleCalculationObjectAI.__init__(self, battle)
        self.av = av
        self.handler = handler
        self.addChild('timer', 3)
        self.addChild('name', 'damageBonus')
        self.addChild('value', 10)
        self.addChild('timing', 0)
    
    def startEffect(self):
        pass
    
    def tick(self):
        self.children['timer'] -= 1
        if self.children['timer'] <= 0:
            if self.children['timer'] != -1:
                self.handler.removeChild(self.children['name'])


class BattleEffectLureKnockbackAI(BattleCalculationObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleEffectLureKnockbackAI')

    def __init__(self, battle, av, handler):
        BattleCalculationObjectAI.__init__(self, battle)
        self.av = av
        self.handler = handler
        self.addChild('timer', 2)
        self.addChild('name', 'knockbackBonus')
        self.addChild('value', 40)
        self.addChild('timing', 0)

    def startEffect(self):
        pass

    def tick(self):
        self.children['timer'] -= 1
        if self.children['timer'] <= 0:
            if self.children['timer'] != -1:
                self.handler.removeChild(self.children['name'])
