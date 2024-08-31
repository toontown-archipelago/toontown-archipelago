from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from .room import GlobalEntities
from otp.level import LevelUtil

if __debug__:
    loadPrcFile('config/facility-editor.prc')
    loadPrcFile('config/development.prc')

    # The VirtualFileSystem, which has already initialized, doesn't see the mount
    # directives in the config(s) yet. We have to force it to load those manually:
    vfs = VirtualFileSystem.getGlobalPtr()
    mounts = ConfigVariableList('vfs-mount')
    for mount in mounts:
        mountFile, mountPoint = (mount.split(' ', 2) + [None, None, None])[:2]
        vfs.mount(Filename(mountFile), Filename(mountPoint), 0)

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.roomEntId2Model = {}

        self.room = GlobalEntities

        self.roomModelId = 1000
        self.mgrLevel = self.room[self.roomModelId]
        self.oobe()
        self.roomName = self.mgrLevel['modelFilename']
        if '.bam' not in self.mgrLevel['modelFilename']:
            self.roomName = self.mgrLevel['modelFilename'] + '.bam'

        self.roomModel = loader.loadModel(self.roomName)
        self.roomModel.reparentTo(render)
        self.roomModel.place()
        self.roomEntId2Model[self.roomModelId] = self.roomModel
        self.zoneNum2Node = LevelUtil.getZoneNum2Node(self.roomModel)
        self.attribNode2ValueType = {}

        for entity in self.room:
            if self.room[entity]['type'] == 'zone':
                model = self.zoneNum2Node.get(entity)
                self.roomEntId2Model[entity] = model

        for entity in self.room:
            if self.room[entity]['type'] == 'nodepath':
                model = NodePath('nodepath')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
        
        for entity in self.room:
            if self.room[entity]['type'] == 'grid':
                model = NodePath('nodepath')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
        
        for entity in self.room:
            if self.room[entity]['type'] == 'crusherCell':
                model = NodePath('nodepath')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model

        """
        20017: {'type': 'beanBarrel',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 10022,
         'pos': Point3(20.0035, 2.94232, 0),
         'hpr': Vec3(-31.6033, 0, 0),
         'scale': 1,
         'rewardPerGrab': 35,
         'rewardPerGrabMax': 0},
        """

        for entity in self.room: # battleBlocker
            if self.room[entity]['type'] == 'rendering':
                model = loader.loadModel("phase_3/models/props/drop_shadow.bam")
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'entrancePoint':
                model = loader.loadModel("phase_3/models/props/drop_shadow.bam")
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'healBarrel':
                model = loader.loadModel('phase_4/models/cogHQ/gagTank.bam')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(0.5)
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'gagBarrel':
                model = loader.loadModel('phase_4/models/cogHQ/gagTank.bam')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(0.5)
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'apBarrel':
                model = loader.loadModel('phase_4/models/cogHQ/gagTank.bam')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(0.5)
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'beanBarrel':
                model = loader.loadModel('phase_4/models/cogHQ/gagTank.bam')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(0.5)
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'button':
                model = loader.loadModel('phase_9/models/cogHQ/CogDoor_Button.bam')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'stomper':
                model = loader.loadModel('phase_9/models/cogHQ/square_stomper.bam')
                head = model.find('**/head')
                shaft = model.find('**/shaft')
                model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setY(model.getY() + -self.room[entity]['range'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                shaft.setScale(self.room[entity]['shaftScale'])
                head.setScale(self.room[entity]['headScale'])
                if self.room[entity]['style'] == 'vertical':
                    model.setP(model.getP() + -90)
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'model':
                modelName = self.room[entity]['modelPath']
                if '.bam' not in self.room[entity]['modelPath']:
                    modelName = self.room[entity]['modelPath'] + '.bam'

                model = loader.loadModel(modelName)
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'battleBlocker':
                model = loader.loadModel("phase_3/models/props/drop_shadow.bam")
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'door':
                model = loader.loadModel('phase_9/models/cogHQ/CogDoorHandShake.bam')
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'conveyorBelt':
                model = loader.loadModel('phase_9/models/cogHQ/platform1.bam')
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'gear':
                model = loader.loadModel('phase_10/models/cashbotHQ/MintGear.bam')
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['gearScale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'mintShelf':
                model = loader.loadModel('phase_10/models/cashbotHQ/shelf_A1Money.bam')
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'mintProductPallet':
                model = loader.loadModel('phase_10/models/cashbotHQ/DoubleGoldStack.bam')
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'mintProduct':
                model = loader.loadModel('phase_10/models/cashbotHQ/GoldBarStack.bam')
                if self.room[entity]['parentEntId'] != 0:
                    model.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    model.reparentTo(self.roomModel)
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'path':
                model = loader.loadModel("phase_3/models/props/drop_shadow.bam")
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                self.roomEntId2Model[entity] = model
            if self.room[entity]['type'] == 'goon':
                model = loader.loadModel("phase_9/models/char/Cog_Goonie-zero.bam")
                model.setPos(self.room[entity]['pos'])
                model.setHpr(self.room[entity]['hpr'])
                model.setScale(self.room[entity]['scale'])
                strengthNode = NodePath('strength')
                strengthNode.reparentTo(model)
                strengthNode.setScale(self.room[entity]['strength'])
                self.roomEntId2Model[entity] = model
        
        for entity in self.room:
            if self.room[entity]['type'] == 'rendering':
                entityModel = self.roomEntId2Model[entity]    
                entityModel.reparentTo(self.roomModel)

        for entity in self.room:
            if self.room[entity]['type'] == 'nodepath':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'entrancePoint':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'battleBlocker':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'crusherCell':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)

        for entity in self.room:
            if self.room[entity]['type'] == 'stomper':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'conveyorBelt':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'mintProduct':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)

        for entity in self.room:
            if self.room[entity]['type'] == 'mintProductPallet':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'mintShelf':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'door':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
                

        for entity in self.room:
            if self.room[entity]['type'] == 'gagBarrel':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
            if self.room[entity]['type'] == 'healBarrel':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
            if self.room[entity]['type'] == 'apBarrel':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
            if self.room[entity]['type'] == 'beanBarrel':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'button':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if self.room[entity]['type'] == 'path':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)

        for entity in self.room:
            if self.room[entity]['type'] == 'goon':
                entityModel = self.roomEntId2Model[entity]
                if self.room[entity]['parentEntId'] != 0:
                    entityModel.reparentTo(self.roomEntId2Model[self.room[entity]['parentEntId']])
                else:
                    entityModel.reparentTo(self.roomModel)
        
        for entity in self.room:
            if entity in self.roomEntId2Model:
                dict = self.room[entity]

                entityModel = self.roomEntId2Model[entity]
                
                for attrib in dict:
                    self.assignAttributeToModel(entity, entityModel, attrib)

        

        
        self.accept('p', self.printRoom)
    
    def printRoom(self):
        # for each model in the room, change the pos, hpr, and scale of the model in the room
        
        for entity in self.room:
            if entity in self.roomEntId2Model:
                entityModel = self.roomEntId2Model[entity]
                
                dict = self.room[entity]

                for attrib in dict:
                    self.changeAttributeOnModel(entity, entityModel)
        
        for entity in self.room:
            if 'pos' in self.room[entity]:
                self.room[entity]['pos'] = self.roomEntId2Model[entity].getPos()
            if 'hpr' in self.room[entity]:
                if self.room[entity]['type'] == 'stomper':
                    self.room[entity]['hpr'] = Vec3(0, 0, 0)
                else:
                    self.room[entity]['hpr'] = self.roomEntId2Model[entity].getHpr()
            if 'scale' in self.room[entity]:
                if self.room[entity]['type'] in ('gagBarrel', 'healBarrel', 'beanBarrel', 'apBarrel'):
                    self.room[entity]['scale'] = 1
                elif self.room[entity]['type'] == 'goon':
                    self.room[entity]['scale'] = self.roomEntId2Model[entity].getSx()
                else:
                    self.room[entity]['scale'] = self.roomEntId2Model[entity].getScale()
        
        self.room[1000]['type'] = 'levelMgr'
        self.room[0]['visibility'] = []

        # We dont want any objects reparented to 1000(lvlMgr), as it causes a crash.
        for entity in self.room:
            if self.room[entity]['parentEntId'] == 1001:
                self.room[entity]['parentEntId'] = 0

        print(self.room)
    
    def assignAttributeToModel(self, entity, model, attrib):
        attrib_Name = NodePath(str(attrib))
        attrib_Name.reparentTo(model)
        attrib_node = NodePath(str(self.room[entity][attrib]))
        attrib_node.reparentTo(attrib_Name)
        attrib_node.setName(str(self.room[entity][attrib]))
        self.attribNode2ValueType[str(entity) + attrib] = type(self.room[entity][attrib])
    
    def changeAttributeOnModel(self, entity, model):
        dict = self.room[entity]
        for attrib in dict:
            attrib_NameNode = model.find('**/' + str(attrib))
            for child in attrib_NameNode.getChildren():
                type_val = self.attribNode2ValueType[str(entity) + attrib]

                print(type_val)

                if type_val == 'str':
                    type_val = str
                if type_val == 'float':
                    type_val = float
                if type_val == 'int':
                    type_val = int

                #type_val = Point3
                try:
                    self.room[entity][attrib] = type_val(child.getName())
                except:
                    self.room[entity][attrib] = eval(child.getName())
            
            
    

app = MyApp()
app.run()