from dataclasses import dataclass
from typing import Set, List

from direct.actor import Actor
from otp.avatar import Avatar
from .SuitDNA import *
from toontown.toonbase import ToontownGlobals
from panda3d.core import *
from toontown.battle import SuitBattleGlobals
from direct.task.Task import Task
from toontown.battle import BattleProps
from toontown.toonbase import TTLocalizer
from libotp import *
from direct.showbase import AppRunnerGlobal
import string
import json
import os

TutorialModelDict = ModelDict

HeadModelDict = ModelDict

def loadTutorialSuit():
    loader.loadModel('phase_3.5/models/char/suitC-mod').node()
    loadDialog(1)


def loadSuits(level):
    __loadUnloadSuitModelsAndAnims(unload=False)
    loadDialog(level)


def unloadSuits(level):
    __loadUnloadSuitModelsAndAnims(unload=True)
    unloadDialog(level)


def __loadUnloadSuitModelsAndAnims(unload=False):

    for key in list(ModelDict.keys()):
        model, phase = ModelDict[key]
        headModel, headPhase = ModelDict[key]

        if unload:
            loader.unloadModel('phase_3.5' + model + 'mod')
            loader.unloadModel('phase_' + str(headPhase) + headModel + 'heads')
        else:
            loader.loadModel('phase_3.5' + model + 'mod').node()
            loader.loadModel('phase_' + str(headPhase) + headModel + 'heads').node()


def cogExists(filePrefix):
    searchPath = DSearchPath()
    if AppRunnerGlobal.appRunner:
        searchPath.appendDirectory(Filename.expandFrom('$TT_3_5_ROOT/phase_3.5'))
    else:
        basePath = os.path.expandvars('$TTMODELS') or './ttmodels'
        searchPath.appendDirectory(Filename.fromOsSpecific(basePath + '/built/phase_3.5'))
    filePrefix = filePrefix.strip('/')
    pfile = Filename(filePrefix)
    found = vfs.resolveFilename(pfile, searchPath)
    if not found:
        return False
    return True



def loadDialog(level):
    global SuitDialogArray
    if len(SuitDialogArray) > 0:
        return
    else:
        loadPath = 'phase_3.5/audio/dial/'
        SuitDialogFiles = ['COG_VO_grunt',
         'COG_VO_murmur',
         'COG_VO_statement',
         'COG_VO_question']
        for file in SuitDialogFiles:
            SuitDialogArray.append(base.loader.loadSfx(loadPath + file + '.ogg'))

        SuitDialogArray.append(SuitDialogArray[2])
        SuitDialogArray.append(SuitDialogArray[2])


def loadSkelDialog():
    global SkelSuitDialogArray
    if len(SkelSuitDialogArray) > 0:
        return
    else:
        grunt = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_grunt.ogg')
        murmur = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_murmur.ogg')
        statement = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_statement.ogg')
        question = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_question.ogg')
        SkelSuitDialogArray = [grunt,
         murmur,
         statement,
         question,
         statement,
         statement]


def unloadDialog(level):
    global SuitDialogArray
    SuitDialogArray = []


def unloadSkelDialog():
    global SkelSuitDialogArray
    SkelSuitDialogArray = []


def attachSuitHead(node, suitName):
    suitIndex = suitHeadTypes.index(suitName)
    suitDNA = SuitDNA()
    suitDNA.newSuit(suitName)
    suit = Suit()
    suit.setDNA(suitDNA)
    headParts = suit.getHeadParts()
    head = node.attachNewNode('head')
    for part in headParts:
        copyPart = part.copyTo(head)
        copyPart.setDepthTest(1)
        copyPart.setDepthWrite(1)

    suit.delete()
    suit = None
    p1 = Point3()
    p2 = Point3()
    head.calcTightBounds(p1, p2)
    d = p2 - p1
    biggest = max(d[0], d[2])
    column = suitIndex % suitsPerDept
    s = (0.2 + column / 100.0) / biggest
    pos = -0.14 + (suitsPerDept - column - 1) / 135.0
    head.setPosHprScale(0, 0, pos, 180, 0, 0, s, s, s)
    return head

class Suit(Avatar.Avatar):

    healthColors = (
        Vec4(0, 1, 0, 1),        # Green/full(ish) hp
        Vec4(1, 1, 0, 1),        # Yellow (Halfish)
        Vec4(1, 0.5, 0, 1),      # Orange (Low)
        Vec4(1, 0, 0, 1),        # Red (Very low)
        Vec4(0.3, 0.3, 0.3, 1),  # Blink slow, task will refer to red as well
        Vec4(0.3, 0.3, 0.3, 1),  # Blink fast, task will refer to red as well
        ToontownGlobals.CogImmuneColor  # Immune
    )

    healthGlowColors = (
        Vec4(0.25, 1, 0.25, 0.5),  # Green/full(ish) hp
        Vec4(1, 1, 0.25, 0.5),     # Yellow (Halfish)
        Vec4(1, 0.5, 0.25, 0.5),   # Orange (Low)
        Vec4(1, 0.25, 0.25, 0.5),  # Red (Very low)
        Vec4(0.3, 0.3, 0.3, 0),    # Blink slow, task will refer to red as well
        Vec4(0.3, 0.3, 0.3, 0),    # Blink fast, task will refer to red as well
        ToontownGlobals.CogImmuneGlowColor  # Immune
    )

    healthColorsAccess = (
        Vec4(0.42, 0.8, 0, 1),        # Green/full(ish) hp
        Vec4(0.8, 0.8, 0.42, 1),        # Yellow (Halfish)
        Vec4(0.8, 0.3, 0.23, 1),      # Orange (Low)
        Vec4(0.8, 0.3, 0.3, 1),        # Red (Very low)
        Vec4(0.3, 0.3, 0.3, 1),  # Blink slow, task will refer to red as well
        Vec4(0.3, 0.3, 0.3, 1),  # Blink fast, task will refer to red as well
        ToontownGlobals.CogImmuneColor  # Immune
    )

    healthGlowColorsAccess = (
        Vec4(0.25, 0.6, 0.25, 0.5),  # Green/full(ish) hp
        Vec4(0.8, 0.6, 0.25, 0.5),     # Yellow (Halfish)
        Vec4(0.6, 0.5, 0.25, 0.5),   # Orange (Low)
        Vec4(0.6, 0.25, 0.25, 0.5),  # Red (Very low)
        Vec4(0.3, 0.3, 0.3, 0),    # Blink slow, task will refer to red as well
        Vec4(0.3, 0.3, 0.3, 0),    # Blink fast, task will refer to red as well
        ToontownGlobals.CogImmuneGlowColor  # Immune
    )

    medallionColors = {
        'c': Vec4(0.863, 0.776, 0.769, 1.0),
        's': Vec4(0.843, 0.745, 0.745, 1.0),
        'l': Vec4(0.749, 0.776, 0.824, 1.0),
        'm': Vec4(0.749, 0.769, 0.749, 1.0)
    }

    def __init__(self):
        try:
            self.Suit_initialized
            return
        except:
            self.Suit_initialized = 1

        Avatar.Avatar.__init__(self)
        self.setFont(ToontownGlobals.getSuitFont())
        self.setPlayerType(NametagGroup.CCSuit)
        self.setPickable(1)
        self.leftHand = None
        self.rightHand = None
        self.shadowJoint = None
        self.nametagJoint = None
        self.headParts = []
        self.healthBar = None
        self.healthCondition = 0
        self.isDisguised = 0
        self.isWaiter = 0
        self.isRental = 0
        self.isImmune = 0
        if not base.colorBlindMode:
            self.healthBarColors = self.healthColors
            self.healthBarGlowColors = self.healthGlowColors
        else:
            self.healthBarColors = self.healthColorsAccess
            self.healthBarGlowColors = self.healthGlowColorsAccess
        self.setBlend(frameBlend=True)
        return

    def delete(self):
        try:
            self.Suit_deleted
        except:
            self.Suit_deleted = 1
            if self.leftHand:
                self.leftHand.removeNode()
                self.leftHand = None
            if self.rightHand:
                self.rightHand.removeNode()
                self.rightHand = None
            if self.shadowJoint:
                self.shadowJoint.removeNode()
                self.shadowJoint = None
            if self.nametagJoint:
                self.nametagJoint.removeNode()
                self.nametagJoint = None
            for part in self.headParts:
                part.removeNode()

            self.headParts = []
            self.removeHealthBar()
            Avatar.Avatar.delete(self)

        return

    def setHeight(self, height):
        Avatar.Avatar.setHeight(self, height)
        self.nametag3d.setPos(0, 0, height + 1.0)

    def getRadius(self):
        return 2

    def setDNAString(self, dnaString):
        self.dna = SuitDNA()
        self.dna.makeFromNetString(dnaString)
        self.setDNA(self.dna)

    def setDNA(self, dna):
        if self.style:
            pass
        else:
            self.style = dna
            self.generateSuit()
            self.initializeDropShadow()
            self.initializeNametag3d()

    def generateSuit(self):
        dna = self.style
        self.headParts = []
        self.headColor = None
        self.headTexture = None
        self.loseActor = None
        self.isSkeleton = 0
        self.isImmune = 0

        visuals = GENERAL_SUIT_VISUALS
        for s_visual in visuals:
            if s_visual.key == dna.name:
                visual = s_visual
                
        if visual is None:
            self.notify.warning(f"Suit DNA name {dna.name} is not in the visuals table!")
            return
        
        self.scale = visual.scale
        self.handColor = visual.hand_color
        self.headColor = visual.head_color_override
        self.headTexture = visual.head_texture_override
        self.generateBody()
        visual.addHeadModel(self)
        self.generateVisual()
        self.setHeight(visual.height)

        self.setName(SuitBattleGlobals.getSuitAttributes(dna.name).name)
        self.getGeomNode().setScale(self.scale)
        self.generateHealthBar()
        self.generateCorporateMedallion()
        self.setBlend(frameBlend=True)
        return

    def generateBody(self):
        animDict = self.generateAnimDict()
        filePrefix, bodyPhase = ModelDict[self.style.body]

        self.loadModel('phase_3.5' + filePrefix + 'mod')
        self.loadAnims(animDict)
        self.setSuitClothes()

    def generateAnimDict(self):
        animDict = {}

        # Find animations that are shared between all suits for our specific body type.
        for animation in getGeneralAnimationsForSuitBody(self.style.body):
            animDict[animation.key] = animation.modelPath()

        # Analyze what attacks this suit can do.
        # We can then load the animations that are attached.
        attacks: Set[str] = SuitBattleGlobals.getAttackAnimationNamesForSuit(self.style.name)
        for animation in getBattleAnimationsForSuit(self.style.name, attacks):

            # Now add the animation!
            animDict[animation.key] = animation.modelPath()

        return animDict

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def setSuitClothes(self, modelRoot = None):
        if not modelRoot:
            modelRoot = self
        
        # Suit's Department : returns --> c, s, l, m : --> letter2dept (bossbot, sellbot, lawbot, cashbot)
        
        customClothesNeeeded = False
        customClothes = CUSTOM_SUIT_CLOTHES
        for s_clothes in customClothes:
            if s_clothes.key == self.style.name:
                customClothesVisual = s_clothes
                customClothesNeeeded = True
                break

        fileSystem = VirtualFileSystem.getGlobalPtr()
        clothesJson = json.loads(fileSystem.readFile(ToontownGlobals.suitClothesJsonFilePath, True))
        
        if self.style.name in clothesJson['suit_clothes']:
            if clothesJson['suit_clothes'][self.style.name] == True:
                torsoTex, legTex, armTex = getSuitNameContentPackClotheTexture(self.style.name)
        elif customClothesNeeeded:
            torsoTex, legTex, armTex = customClothesVisual.getClotheTexture(self)
        else:
            torsoTex, legTex, armTex = getNormalClotheTexture(self.style.dept)
        
        torsoTex.setMinfilter(Texture.FTLinearMipmapLinear)
        torsoTex.setMagfilter(Texture.FTLinear)
        
        legTex.setMinfilter(Texture.FTLinearMipmapLinear)
        legTex.setMagfilter(Texture.FTLinear)
        
        armTex.setMinfilter(Texture.FTLinearMipmapLinear)
        armTex.setMagfilter(Texture.FTLinear)


        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagJoint = self.find('**/joint_nameTag')

    def makeWaiter(self, modelRoot = None):
        if not modelRoot:
            modelRoot = self
        self.isWaiter = 1
        
        torsoTex, legTex, armTex = getWaiterClotheTexture()
        
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        handTexture = loader.loadTexture('phase_' + str(suitDeptToPhase[self.style.dept]) + '/maps/tt_t_ene_suitHand_' + self.style.name + '.png')
        modelRoot.find('**/hands').setTexture(handTexture, 1)

    def makeRentalSuit(self, suitType, modelRoot = None):
        if not modelRoot:
            modelRoot = self.getGeomNode()
        if suitType == 's':
            torsoTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_blazer.jpg')
            legTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_leg.jpg')
            armTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_sleeve.jpg')
            handTex = loader.loadTexture('phase_3.5/maps/tt_t_ene_sellbotRental_hand.jpg')
        else:
            self.notify.warning('No rental suit for cog type %s' % suitType)
            return
        self.isRental = 1
        modelRoot.find('**/torso').setTexture(torsoTex, 1)
        modelRoot.find('**/arms').setTexture(armTex, 1)
        modelRoot.find('**/legs').setTexture(legTex, 1)
        modelRoot.find('**/hands').setTexture(handTex, 1)

    def generateVisual(self):
        # Head Portion
        for headPart in self.headParts:
            if self.headTexture:
                path = suit2headTexturePaths[self.style.body]
                headTex = loader.loadTexture(path + self.headTexture)
                headTex.setMinfilter(Texture.FTLinearMipmapLinear)
                headTex.setMagfilter(Texture.FTLinear)
                headPart.setTexture(headTex, 1)
            if self.headColor:
                headPart.setColor(self.headColor)
        
        # Hands
        handTexture = loader.loadTexture('phase_' + str(suitDeptToPhase[self.style.dept]) + '/maps/tt_t_ene_suitHand_' + self.style.name + '.png')
        self.find('**/hands').setTexture(handTexture, 1)

    def generateCorporateTie(self, modelPath = None):
        if not modelPath:
            modelPath = self
        dept = self.style.dept
        tie = modelPath.find('**/tie')
        if tie.isEmpty():
            self.notify.warning('skelecog has no tie model!!!')
            return
        if dept == 'c':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_boss.jpg')
        elif dept == 's':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_sales.jpg')
        elif dept == 'l':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_legal.jpg')
        elif dept == 'm':
            tieTex = loader.loadTexture('phase_5/maps/cog_robot_tie_money.jpg')
        tieTex.setMinfilter(Texture.FTLinearMipmapLinear)
        tieTex.setMagfilter(Texture.FTLinear)
        tie.setTexture(tieTex, 1)

    def generateCorporateMedallion(self):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        dept = self.style.dept
        chestNull = self.find('**/joint_attachMeter')
        if dept == 'c':
            self.corpMedallion = icons.find('**/CorpIcon').copyTo(chestNull)
        elif dept == 's':
            self.corpMedallion = icons.find('**/SalesIcon').copyTo(chestNull)
        elif dept == 'l':
            self.corpMedallion = icons.find('**/LegalIcon').copyTo(chestNull)
        elif dept == 'm':
            self.corpMedallion = icons.find('**/MoneyIcon').copyTo(chestNull)
        self.corpMedallion.setPosHprScale(0.02, 0.05, 0.04, 180.0, 0.0, 0.0, 0.51, 0.51, 0.51)
        self.corpMedallion.setColor(self.medallionColors[dept])
        icons.removeNode()

    def generateHealthBar(self):
        self.removeHealthBar()
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        button.setScale(3.0)
        button.setH(180.0)
        button.setColor(self.healthBarColors[0])
        chestNull = self.find('**/joint_attachMeter')
        button.reparentTo(chestNull)
        self.healthBar = button
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(self.healthBar)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(self.healthBarGlowColors[0])
        button.flattenLight()
        self.healthBarGlow = glow
        self.healthBar.hide()
        self.healthCondition = 0 if not self.isImmune else 6
        self.updateHealthBar(0, forceUpdate=True)

    def resetHealthBarForSkele(self):
        self.healthBar.setPos(0.0, 0.1, 0.0)

    def virtualize(self, condition):
        self.healthBar.stash()
        actorNode = self.find('**/__Actor_modelRoot')
        actorCollection = actorNode.findAllMatches('*')
        parts = ()
        for thingIndex in range(0, actorCollection.getNumPaths()):
            thing = actorCollection[thingIndex]
            if thing.getName() not in ('joint_attachMeter', 'joint_nameTag', 'def_nameTag'):
                thing.setColor(self.healthBarColors[condition])
                thing.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                thing.setDepthWrite(False)
                thing.setBin('fixed', 1)

    def updateHealthBar(self, hp, forceUpdate = 0):

        if not hasattr(self, 'currHP'):
            return

        if hp > self.currHP:
            hp = self.currHP
        self.currHP -= hp
        messenger.send(self.uniqueName('suitHpUpdate'), [self.currHP, self.maxHP, hp])
        health = float(self.currHP) / float(self.maxHP)

        if self.isImmune:
            newCondition = 6
        elif health > 0.95:
            newCondition = 0  # green
        elif health > 0.7:
            newCondition = 1  # yellow
        elif health > 0.3:
            newCondition = 2  # orange
        elif health > .05:
            newCondition = 3  # red
        elif health > 0:
            newCondition = 4  # blink red
        else:
            newCondition = 5  # blink red fast

        oldCondition = self.healthCondition
        self.healthCondition = newCondition

        if oldCondition != newCondition or forceUpdate:

            # Handle blinking condition
            if newCondition == 4:
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, self.uniqueName('blink-task'))
                return

            # Handle fast blink condition
            if newCondition == 5:
                if self.getVirtual():
                    self.virtualize(4)
                taskMgr.remove(self.uniqueName('blink-task'))
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, self.uniqueName('blink-task'))
                return

            # Simply setting color
            self.healthBar.setColor(self.healthBarColors[newCondition], 1)
            self.healthBarGlow.setColor(self.healthBarGlowColors[newCondition], 1)
            if self.getVirtual():
                self.virtualize(newCondition)

    def __blinkRed(self, task):
        self.healthBar.setColor(self.healthBarColors[3], 1)
        self.healthBarGlow.setColor(self.healthBarGlowColors[3], 1)
        if self.healthCondition == 5:
            self.healthBar.setScale(1.17)
        return Task.done

    def __blinkGray(self, task):
        if not self.healthBar:
            return
        self.healthBar.setColor(self.healthBarColors[4], 1)
        self.healthBarGlow.setColor(self.healthBarGlowColors[4], 1)
        if self.healthCondition == 5:
            self.healthBar.setScale(1.0)
        return Task.done

    def removeHealthBar(self):
        if self.healthBar:
            self.healthBar.removeNode()
            self.healthBar = None
        if self.healthCondition == 4 or self.healthCondition == 5:
            taskMgr.remove(self.uniqueName('blink-task'))
        self.healthCondition = 0
        return

    def getLoseActor(self):
        if base.config.GetBool('want-new-cogs', 0):
            if self.find('**/body'):
                return self
        if self.loseActor == None:
            if not self.isSkeleton:
                filePrefix, phase = TutorialModelDict[self.style.body]
                loseModel = 'phase_' + str(phase) + filePrefix + 'lose-mod'
                loseAnim = 'phase_' + str(phase) + filePrefix + 'lose'
                self.loseActor = Actor.Actor(loseModel, {'lose': loseAnim})
                loseNeck = self.loseActor.find('**/joint_head')
                for part in self.headParts:
                    part.instanceTo(loseNeck)

                if self.isWaiter:
                    self.makeWaiter(self.loseActor)
                else:
                    self.setSuitClothes(self.loseActor)
            else:
                loseModel = 'phase_5/models/char/cog' + self.style.body.upper() + '_robot-lose-mod'
                filePrefix, phase = TutorialModelDict[self.style.body]
                loseAnim = 'phase_' + str(phase) + filePrefix + 'lose'
                self.loseActor = Actor.Actor(loseModel, {'lose': loseAnim})
                self.generateCorporateTie(self.loseActor)
        self.loseActor.setScale(self.scale)
        self.loseActor.setPos(self.getPos())
        self.loseActor.setHpr(self.getHpr())
        shadowJoint = self.loseActor.find('**/joint_shadow')
        dropShadow = loader.loadModel('phase_3/models/props/drop_shadow')
        dropShadow.setScale(0.45)
        dropShadow.setColor(0.0, 0.0, 0.0, 0.5)
        dropShadow.reparentTo(shadowJoint)
        self.loseActor.setBlend(frameBlend=True)
        
        # Set the hand color
        if not self.isSkeleton:
            handTexture = loader.loadTexture('phase_' + str(suitDeptToPhase[self.style.dept]) + '/maps/tt_t_ene_suitHand_' + self.style.name + '.png')
            self.loseActor.find('**/hands').setTexture(handTexture, 1)
        return self.loseActor

    def cleanupLoseActor(self):
        self.notify.debug('cleanupLoseActor()')
        if self.loseActor != None:
            self.notify.debug('cleanupLoseActor() - got one')
            self.loseActor.cleanup()
        self.loseActor = None
        return

    def makeIntoImmune(self):
        self.isImmune = 1
        self.healthBar.setColor(self.healthBarColors[6])
        self.healthBarGlow.setColor(self.healthBarGlowColors[6])
        self.updateHealthBar(0)

    def removeImmune(self):
        self.isImmune = 0
        self.updateHealthBar(0)

    def makeSkeleton(self):
        model = 'phase_5/models/char/cog' + self.style.body.upper() + '_robot-zero'
        anims = self.generateAnimDict()
        anim = self.getCurrentAnim()
        dropShadow = self.dropShadow
        if not dropShadow.isEmpty():
            dropShadow.reparentTo(hidden)
        self.removePart('modelRoot')
        self.loadModel(model)
        self.loadAnims(anims)
        self.getGeomNode().setScale(self.scale * 1.0173)
        self.generateHealthBar()
        self.generateCorporateMedallion()
        self.generateCorporateTie()
        self.setHeight(self.height)
        parts = self.findAllMatches('**/pPlane*')
        for partNum in range(0, parts.getNumPaths()):
            bb = parts.getPath(partNum)
            bb.setTwoSided(1)

        self.setName(TTLocalizer.Skeleton)
        nameInfo = TTLocalizer.SuitBaseNameWithLevel % {'name': self._name,
         'dept': self.getStyleDept(),
         'level': self.getActualLevel()}
        self.setDisplayName(nameInfo)
        self.leftHand = self.find('**/joint_Lhold')
        self.rightHand = self.find('**/joint_Rhold')
        self.shadowJoint = self.find('**/joint_shadow')
        self.nametagNull = self.find('**/joint_nameTag')
        if not dropShadow.isEmpty():
            dropShadow.setScale(0.75)
            if not self.shadowJoint.isEmpty():
                dropShadow.reparentTo(self.shadowJoint)
        self.loop(anim)
        self.isSkeleton = 1
        self.setBlend(frameBlend=True)

    def getHeadParts(self):
        return self.headParts

    def getRightHand(self):
        return self.rightHand

    def getLeftHand(self):
        return self.leftHand

    def getShadowJoint(self):
        return self.shadowJoint

    def getNametagJoints(self):
        return []

    def getDialogueArray(self):
        if self.isSkeleton:
            loadSkelDialog()
            return SkelSuitDialogArray
        else:
            return SuitDialogArray
