from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import Point3, Quat, getModelPath, Filename

from . import PlacerTool3D
from . import ToonGlobals
from . import AccessoryBase

import json

getModelPath().appendDirectory(Filename("resources/"))

class AccessoryPlacer(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.HeadBaseDir = ToonGlobals.HeadBaseDir
        self.TorsoBaseDir = ToonGlobals.TorsoBaseDir
        self.HeadSizes = ToonGlobals.HeadSizes
        self.TorsoSizes = ToonGlobals.TorsoSizes
        self.HeadDict = ToonGlobals.HeadDict
        self.TorsoDict = ToonGlobals.TorsoDict
        self.LegDict = ToonGlobals.LegDict
        self.TorsoTypes = ToonGlobals.TorsoTypes
        self.LegTypes = ToonGlobals.LegTypes
        self.AccessoryBaseDir = AccessoryBase.AccessoryBaseDir
        self.HatModels = AccessoryBase.HatModels
        self.HatTextures = AccessoryBase.HatTextures
        self.GlassesModels = AccessoryBase.GlassesModels
        self.GlassesTextures = AccessoryBase.GlassesTextures
        self.BackpackModels = AccessoryBase.BackpackModels
        self.BackpackTextures = AccessoryBase.BackpackTextures
        self.currHead = None
        self.currHeadIndex = 0
        self.currTorso = None
        self.currTorsoIndex = 0
        self.currLegs = None
        self.currLegsIndex = 0
        self.currBackpack = None
        self.currBackpackIndex = 0
        self.currHat = None
        self.currHatIndex = 0
        self.currGlasses = None
        self.currGlassesIndex = 0
        self.currBackpackPlacer = None
        self.currHatPlacer = None
        self.currGlassesPlacer = None
        self.lastdataHash = None

        base.accept('b', self.togglePlaceBackpack)
        base.accept('h', self.togglePlaceHat)
        base.accept('g', self.togglePlaceGlasses)
        base.accept('o', base.oobe)

        base.disableMouse()
        base.accept('placer-destroyed', self.onPlacerDestroy)
        self.backpackLabel = {'text':  'Backpack: None'}
        self.hatLabel = {'text':  'Hat: None'}
        self.glassesLabel= {'text':  'Glasses: None'}
        self.loadHead()
        camera.setPosHpr(0, 5, 0, 180, 0, 0)
        self.acceptCameraKeys()

        JSONfile = "accessoryplacer/accessories.json"
        #if not JSONfile.isfile():
        # do json function
        #    path = open("accessories.json", "x")
        with open(JSONfile, 'r') as f:
            self.data = json.load(f)

        self.loadGUI()

    def loadHead(self):
        headSize = self.HeadSizes[self.currHeadIndex]
        species, size = headSize
        if species == 'd':
            species = species + size
            self.currHead = loader.loadModel(self.HeadBaseDir + self.HeadDict[species], okMissing=True)
            self.showDogHead(self.currHead)
            self.currHead.reparentTo(render)
            return
        self.currHead = loader.loadModel(self.HeadBaseDir + self.HeadDict[species], okMissing=True)

        if self.currHead is None:
            return

        if size == 'l':
            self.showLongHead(self.currHead)
        elif size == 's':
            self.showShortHead(self.currHead)
        self.currHead.reparentTo(render)

    def unloadHead(self):
        if self.currHead is not None:
            self.currHead.removeNode()

    def changeHead(self, offset):
        self.currHeadIndex += offset

        if self.currHeadIndex >= len(self.HeadSizes):
            self.currHeadIndex = 0
        elif self.currHeadIndex <= -1:
            self.currHeadIndex = len(self.HeadSizes) - 1

        self.unloadHead()
        if self.currTorso is not None:
            self.unloadBackpack()
            self.unloadTorso()
        self.loadHead()
        self.loadHat()
        self.loadGlasses()

    def loadTorso(self):
        size = self.TorsoSizes[self.currTorsoIndex]
        self.currTorso = loader.loadModel(self.TorsoBaseDir + self.TorsoDict[size + 's'], okMissing=True)
        self.showTorso(self.currTorso)
        self.currTorso.setH(self.currTorso.getH() + 180)
        self.currTorso.reparentTo(render)

    def unloadTorso(self):
        if not self.currTorso:
            return
        self.currTorso.removeNode()
        self.currTorso = None

    def changeTorso(self, offset):
        self.currTorsoIndex += offset

        if self.currTorsoIndex >= len(self.TorsoSizes):
            self.currTorsoIndex = 0
        elif self.currTorsoIndex <= -1:
            self.currTorsoIndex = len(self.TorsoSizes) - 1

        self.unloadBackpack()
        self.unloadTorso()
        if self.currHead is not None:
            self.unloadHead()
            self.unloadHat()
            self.unloadGlasses()
        self.loadTorso()
        self.loadBackpack()

    def loadBackpack(self):
        torsoSize = self.TorsoSizes[self.currTorsoIndex]
        print('loadBackpack', self.currBackpackIndex)
        if self.currBackpackIndex == 0:
            self.backpackLabel['text'] = 'Backpack: None'
            return
        modelName = self.BackpackModels[self.currBackpackIndex]
        self.backpackLabel['text'] = 'Backpack: ' + modelName
        self.currBackpack = loader.loadModel(self.AccessoryBaseDir + modelName,okMissing=True)
        if self.currBackpack is not None:
            try:
                pos, hpr, scale = self.data['backpacks']['specific'][str(self.currBackpackIndex)][torsoSize]
                print(pos, hpr, scale)
                self.currBackpack.setPos(*pos)
                self.currBackpack.setHpr(*hpr)
                self.currBackpack.setScale(*scale)
            except KeyError:
                try:
                    pos, hpr, scale = self.data['backpacks']['defaults'][torsoSize]
                    print(pos, hpr, scale)
                    self.currBackpack.setPos(*pos)
                    self.currBackpack.setHpr(*hpr)
                    self.currBackpack.setScale(*scale)
                except KeyError:
                    pass
            self.attachBackpack()

    def attachBackpack(self):
        nodes = self.currTorso.findAllMatches('**/def_joint_attachFlower')
        backpackNode = nodes[0].attachNewNode('backpackNode')
        self.currBackpack.reparentTo(backpackNode)

    def changeBackpack(self, offset):
        self.currBackpackIndex += offset
        if self.currBackpackIndex >= len(self.BackpackModels):
            self.currBackpackIndex = 0
        elif self.currBackpackIndex <= -1:
            self.currBackpackIndex = len(self.BackpackModels) - 1

        self.unloadBackpack()
        if self.currHead and not self.currHead.isEmpty():
            self.unloadHead()
            self.unloadHat()
            self.unloadGlasses()
        if not self.currTorso:
            self.loadTorso()
        self.destroyBackpackPlacer()
        self.loadBackpack()

    def unloadBackpack(self):
        if not self.currBackpack:
            return
        self.currBackpack.removeNode()
        self.currBackpack = None

    def clearBackpack(self):
        if self.currBackpack is not None:
            self.currBackpackIndex = 0
            self.currBackpack.removeNode()
            self.currBackpack = None
            self.backpackLabel['text'] = 'Backpack: None'

    def loadHat(self):
        self.headSize = self.HeadSizes[self.currHeadIndex]
        print('loadHat', self.currHatIndex)
        if self.currHatIndex == 0:
            self.hatLabel['text'] = 'Hat: None'
            return
        modelName = self.HatModels[self.currHatIndex]
        self.hatLabel['text'] = 'Hat: ' + modelName
        self.currHat = loader.loadModel(self.AccessoryBaseDir + modelName, okMissing=True)
        if self.currHat is not None:
            try:
                pos, hpr, scale = self.data['hats']['specific'][str(self.currHatIndex)][self.headSize]
                print(pos, hpr, scale)
                self.currHat.setPos(*pos)
                self.currHat.setHpr(*hpr)
                self.currHat.setScale(*scale)
            except KeyError:
                try:
                    pos, hpr, scale = self.data['hats']['defaults'][self.headSize]
                    print(pos, hpr, scale)
                    self.currHat.setPos(*pos)
                    self.currHat.setHpr(*hpr)
                    self.currHat.setScale(*scale)
                except KeyError:
                    pass
            self.attachHat()

    def attachHat(self):
        if self.currHead is not None:
            hatNode = self.currHead.attachNewNode('hatNode')
            self.currHat.reparentTo(hatNode)

    def changeHat(self, offset):
        self.currHatIndex += offset

        if self.currHatIndex >= len(self.HatModels):
            self.currHatIndex = 0
        elif self.currHatIndex <= -1:
            self.currHatIndex = len(self.HatModels) - 1

        self.unloadHat()
        if self.currTorso is not None:
            self.unloadBackpack()
            self.unloadTorso()
        if not self.currHead:
            self.loadHead()
        self.destroyHatPlacer()
        self.loadHat()

    def unloadHat(self):
        if not self.currHat:
            return
        self.currHat.removeNode()
        self.currHat = None

    def clearHat(self):
        if self.currHat is not None:
            self.currHatIndex = 0
            self.currHat.removeNode()
            self.currHat = None
            self.hatLabel['text'] = 'Hat: None'

    def loadGlasses(self):
        headSize = self.HeadSizes[self.currHeadIndex]
        if self.currGlassesIndex == 0:
            self.glassesLabel['text'] = 'Glasses: None'
            return
        modelName = self.GlassesModels[self.currGlassesIndex]
        self.glassesLabel['text'] = 'Glasses: ' + modelName
        self.currGlasses = loader.loadModel(self.AccessoryBaseDir + modelName, okMissing=True)
        if self.currGlasses is not None:
            try:
                pos, hpr, scale  = self.data['glasses']['specific'][str(self.currGlassesIndex)][self.headSize]
                self.currGlasses.setPos(*pos)
                self.currGlasses.setHpr(*hpr)
                self.currGlasses.setScale(*scale)
            except KeyError:
                print('Couldnt find poshprscale')
                try:
                    pos, hpr, scale = self.data['glasses']['defaults'][self.headSize]
                    self.currGlasses.setPos(*pos)
                    self.currGlasses.setHpr(*hpr)
                    self.currGlasses.setScale(*scale)
                except KeyError:
                    pass
            self.attachGlasses()

    def attachGlasses(self):
        if self.currHead is not None:
            glassesNode = self.currHead.attachNewNode('glassesNode')
            self.currGlasses.reparentTo(glassesNode)

    def changeGlasses(self, offset):
        self.currGlassesIndex += offset

        if self.currGlassesIndex >= len(self.GlassesModels):
            self.currGlassesIndex = 0
        elif self.currGlassesIndex <= -1:
            self.currGlassesIndex = len(self.GlassesModels) - 1

        self.unloadGlasses()
        if self.currTorso is not None:
            self.unloadBackpack()
            self.unloadTorso()
        if not self.currHead:
            self.loadHead()
        self.destroyGlassesPlacer()
        self.loadGlasses()

    def unloadGlasses(self):
        if not self.currGlasses:
            return
        self.currGlasses.removeNode()
        self.currGlasses = None

    def clearGlasses(self):
        if self.currGlasses is not None:
            self.currHatIndex = 0
            self.currGlasses.removeNode()
            self.currHat = None
            self.hatLabel['text'] = 'Glasses: None'

    def showLongHead(self, head):
        head.findAllMatches('**/*-short*').hide()
        head.findAllMatches('**/*_short*').hide()
        head.findAllMatches('**/muzzle-long-*').hide()
        head.ls()
        muzzle = head.find('**/muzzle-long-neutral')
        if muzzle and not muzzle.isEmpty():
            muzzle.show()
        else:
            muzzle = head.find('**/muzzle-short-neutral')
            muzzle.show()

    def showShortHead(self, head):
        head.findAllMatches('**/*-long*').hide()
        head.findAllMatches('**/*_long*').hide()
        head.findAllMatches('**/muzzle-short-*').hide()
        head.ls()
        head.find('**/muzzle-short-neutral').show()

    def showDogHead(self, head):
        head.ls()

    def showTorso(self, torso):
        torso.ls()

    def hashDict(self, d):
        return hash(json.dumps(d, sort_keys=True))

    def save(self):
        headSize = self.HeadSizes[self.currHeadIndex]
        torsoSize = self.TorsoSizes[self.currTorsoIndex]

        if self.currBackpackIndex and self.currBackpack:
            pos, hpr, scale = list(round(i, 4) for i in self.currBackpack.getPos()), list(round(i, 4) for i in self.currBackpack.getHpr()), list(round(i, 4) for i in self.currBackpack.getScale())

            if str(self.currBackpackIndex) not in self.data['backpacks']['specific']:
                self.data['backpacks']['specific'][str(self.currBackpackIndex)] = dict()
            self.data['backpacks']['specific'][str(self.currBackpackIndex)][torsoSize] = [pos, hpr, scale]

        if self.currGlassesIndex and self.currGlasses:
            pos, hpr, scale = list(round(i, 4) for i in self.currGlasses.getPos()), list(round(i, 4) for i in self.currGlasses.getHpr()), list(round(i, 4) for i in self.currGlasses.getScale())

            if str(self.currGlassesIndex) not in self.data['glasses']['specific']:
                self.data['glasses']['specific'][str(self.currGlassesIndex)] = dict()
            self.data['glasses']['specific'][str(self.currGlassesIndex)][self.headSize] = [pos, hpr, scale]

        if self.currHatIndex and self.currHat:
            pos, hpr, scale = list(round(i, 4) for i in self.currHat.getPos()), list(round(i, 4) for i in self.currHat.getHpr()), list(round(i, 4) for i in self.currHat.getScale())
            if str(self.currHatIndex) not in self.data['hats']['specific']:
                self.data['hats']['specific'][str(self.currHatIndex)] = dict()
            self.data['hats']['specific'][str(self.currHatIndex)][self.headSize] = [pos, hpr, scale]

        self.dataHash = self.hashDict(self.data)

        if self.lastdataHash != self.dataHash:
            with open('accessories.json', 'w') as f:
                json.dump(self.data, f, sort_keys=True, indent=2, separators=(',', ': '))

            self.lastdataHash = self.dataHash

    def __autosaveTask(self, task):
        self.save()
        return task.again

    def autosave(self):
        if taskMgr.hasTaskNamed('autosave-task'):
            taskMgr.remove('autosave-task')
            self.autosaveButton['text'] = 'Autosave:\n\x01red\x01off\x02'
        else:
            self.save()
            taskMgr.doMethodLater(10, self.__autosaveTask, 'autosave-task')
            self.autosaveButton['text'] = 'Autosave:\n\x01green\x01on\x02'


    def loadGUI(self):
        from panda3d.core import TextNode, TextProperties, TextPropertiesManager


        DGG.setDefaultFont(loader.loadFont('../resources/phase_3/models/fonts/ImpressBT.ttf'))
        DGG.setDefaultRolloverSound(loader.loadSfx('../resources/phase_3/audio/sfx/GUI_rollover.ogg'))
        DGG.setDefaultClickSound(loader.loadSfx('../resources/phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
        DGG.setDefaultDialogGeom(loader.loadModel('../resources/phase_3/models/gui/dialog_box_gui'))

        red = TextProperties()
        red.setTextColor(1, 0, 0, 1)
        TextPropertiesManager.getGlobalPtr().setProperties('red', red)
        green = TextProperties()
        green.setTextColor(0, 1, 0, 1)
        TextPropertiesManager.getGlobalPtr().setProperties('green', green)
        yellow = TextProperties()
        yellow.setTextColor(1, 1, 0, 1)

        frame = DirectFrame(parent=base.a2dTopRight,relief=DGG.SUNKEN, borderWidth=(0.01, 0.01), frameSize=(-0.3, 0.3, -0.95, 0.3), pos=(-0.3, 0, -0.3))
        nextHead = DirectButton(parent=frame, relief=2, text='Next Head', text_scale=0.04, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(0.15, 0, 0.2), command=self.changeHead, extraArgs=[1])
        previousHead = DirectButton(parent=frame, relief=2, text='Prev Head', text_scale=0.04, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, 0.2), command=self.changeHead, extraArgs=[-1])
        nextTorso = DirectButton(parent=frame, relief=2, text='Next Torso', text_scale=0.04, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(0.15, 0, 0.05), command=self.changeTorso, extraArgs=[1])
        previousTorso = DirectButton(parent=frame, relief=2, text='Prev Torso', text_scale=0.04, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, 0.05), command=self.changeTorso, extraArgs=[-1])
        nextBackpack = DirectButton(parent=frame, relief=2, text='Next Backpack', text_scale=0.030, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(0.15, 0, -0.10), command=self.changeBackpack, extraArgs=[1])
        previousBackpack = DirectButton(parent=frame, relief=2, text='Prev Backpack', text_scale=0.030, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, -0.10), command=self.changeBackpack, extraArgs=[-1])
        nextHat = DirectButton(parent=frame, relief=2, text='Next Hat', text_scale=0.04, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(0.15, 0, -0.25), command=self.changeHat, extraArgs=[1])
        previousHat = DirectButton(parent=frame, relief=2, text='Prev Hat', text_scale=0.04, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, -0.25), command=self.changeHat, extraArgs=[-1])
        nextGlasses = DirectButton(parent=frame, relief=2, text='Next Glasses', text_scale=0.035, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(0.15, 0, -0.40), command=self.changeGlasses, extraArgs=[1]) #delta +- 25
        previousGlasses = DirectButton(parent=frame, relief=2, text='Prev Glasses', text_scale=0.035, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, -0.40), command=self.changeGlasses, extraArgs=[-1])
        clearBackpack = DirectButton(parent=frame, relief=2, text='Clear Backpack', text_scale=0.030, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, -0.55), command=self.clearBackpack)
        clearHat = DirectButton(parent=frame, relief=2, text='Clear Hat', text_scale=0.035, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(0.15, 0, -0.55), command=self.clearHat)
        clearGlasses = DirectButton(parent=frame, relief=2, text='Clear Glasses', text_scale=0.035, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, -0.70), command=self.clearGlasses)
        saveButton = DirectButton(parent=frame, relief=2, text='Save', text_scale=0.035, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), pos=(-0.15, 0, -0.85), command=self.save)
        self.autosaveButton = DirectButton(parent=frame, relief=2, text='Autosave:\n\x01red\x01off\x02', text_scale=0.035, borderWidth=(0.01, 0.01), frameSize=(-0.1, 0.1, -0.05, 0.05), text_pos=(0, 0.01), pos=(0.15, 0, -0.85), command=self.autosave)

        self.backpackLabel = DirectLabel(parent=base.a2dBottomCenter, relief=None, text='Backpack:', text_scale=0.05, pos=(0, 0, 0.1), text_align=TextNode.ACenter)
        self.hatLabel = DirectLabel(parent=base.a2dBottomCenter, relief=None, text='Hat:', text_scale=0.05, pos=(0, 0, 0.2), text_align=TextNode.ACenter)
        self.glassesLabel = DirectLabel(parent=base.a2dBottomCenter, relief=None, text='Glasses:', text_scale=0.05, pos=(0, 0, 0.3), text_align=TextNode.ACenter)


    def togglePlaceBackpack(self):
        if self.currBackpackPlacer:
            self.destroyBackpackPlacer()
        else:
            self.placeBackpack()

    def placeBackpack(self):
        self.destroyBackpackPlacer()
        if self.currBackpack:
            self.currBackpackPlacer = PlacerTool3D(self.currBackpack)
        self.ignoreCameraKeys()

    def destroyBackpackPlacer(self):
        if self.currBackpackPlacer:
            self.currBackpackPlacer.destroy()
            return

    def togglePlaceHat(self):
        if self.currHatPlacer:
            self.destroyHatPlacer()
        else:
            self.placeHat()

    def placeHat(self):
        self.destroyHatPlacer()
        if self.currHat:
            self.currHatPlacer = PlacerTool3D(self.currHat)
        self.ignoreCameraKeys()

    def destroyHatPlacer(self):
        if self.currHatPlacer:
            self.currHatPlacer.destroy()
            return

    def togglePlaceGlasses(self):
        if self.currGlassesPlacer:
            self.destroyGlassesPlacer()
        else:
            self.placeGlasses()

    def placeGlasses(self):
        self.destroyGlassesPlacer()
        if self.currGlasses:
            self.currGlassesPlacer = PlacerTool3D(self.currGlasses)
        self.ignoreCameraKeys()

    def destroyGlassesPlacer(self):
        if self.currGlassesPlacer:
            self.currGlassesPlacer.destroy()
            return


    def cameraLerp(self, i):
        cameraLerps = [
        (Point3(0, 5, 0), Point3(180, 0, 0),),
        (Point3(-5, 0, 0), Point3(270, 0, 0),),
        (Point3(0, -5, 0), Point3(0, 0, 0),),
        (Point3(5, 0, 0), Point3(90, 0, 0),), ]
    
        pos, hpr = cameraLerps[i]
        quat = Quat()
        quat.setHpr(hpr)
        camera.posQuatInterval(1.2, pos, quat).start()



    def acceptCameraKeys(self):
        base.accept('1', lambda: self.cameraLerp(0))
        base.accept('2', lambda: self.cameraLerp(1))
        base.accept('3', lambda: self.cameraLerp(2))
        base.accept('4', lambda: self.cameraLerp(3))

    def ignoreCameraKeys(self):
        base.ignore('1')
        base.ignore('2')
        base.ignore('3')
        base.ignore('4')

    def onPlacerDestroy(self, placer):
        if placer == self.currBackpackPlacer:
            self.currBackpackPlacer = None
        if placer == self.currHatPlacer:
            self.currHatPlacer = None
        if placer == self.currGlassesPlacer:
            self.currGlassesPlacer = None

        if not self.currBackpackPlacer and not self.currGlassesPlacer and not self.currHatPlacer:
            self.acceptCameraKeys()

#
#    try:
#        base.run()
#    except:
#        self.save()



loadPrcFileData('', 'default-model-extension .bam')
loadPrcFileData('', 'model-path .')


base = AccessoryPlacer()
base.run()
