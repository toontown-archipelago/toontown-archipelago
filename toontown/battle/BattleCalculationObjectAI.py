from direct.showbase.DirectObject import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.MessengerGlobal import messenger
from toontown.toonbase.ToontownBattleGlobals import *

class BattleCalculationObjectAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleCalculationObjectAI')
    
    def __init__(self, battle):
        self.children = {}
        self.battle = battle
    
    def addChild(self, name, obj):
        self.children[name] = obj
    
    def removeChild(self, name):
        del self.children[name]