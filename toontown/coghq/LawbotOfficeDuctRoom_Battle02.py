from toontown.coghq.SpecImports import *
GlobalEntities = {1000: {'type': 'levelMgr',
        'name': 'LevelMgr',
        'comment': '',
        'parentEntId': 0,
        'cogLevel': 0,
        'farPlaneDistance': 1500,
        'modelFilename': 'phase_11/models/lawbotHQ/LB_Zone30',
        'wantDoors': 1},
 1001: {'type': 'editMgr',
        'name': 'EditMgr',
        'parentEntId': 0,
        'insertEntity': None,
        'removeEntity': None,
        'requestNewEntity': None,
        'requestSave': None},
 0: {'type': 'zone',
     'name': 'UberZone',
     'comment': '',
     'parentEntId': 0,
     'scale': 1,
     'description': '',
     'visibility': []},
 10001: {'type': 'battleBlocker',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(44.257774353, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'cellId': 0,
         'radius': 10.0},
 11001: {'type': 'battleBlocker',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(6.70862, 157.068, 0.0239553),
         'hpr': Vec3(180.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'cellId': 1,
         'radius': 10.0},
 100001: {'type': 'model',
          'name': '<unnamed>',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(178.642, -0.313949, 0),
          'hpr': Point3(-90, 0, 0),
          'scale': Point3(3.0, 3.0, 3.0),
          'collisionsOnly': 0,
          'flattenType': 'light',
          'loadType': 'loadModelCopy',
          'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfB'},
 14001: {'type': 'door',
          'name': '<unnamed>',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(2.42782, 18.5, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': 1,
          'color': Vec4(1, 1, 1, 1),
          'isLock0Unlocked': 1,
          'isLock1Unlocked': 0,
          'isLock2Unlocked': 1,
          'isLock3Unlocked': 1,
          'isOpen': 0,
          'isOpenEvent': 0,
          'isVisBlocker': 0,
          'secondsOpen': 1,
          'unlock0Event': 0,
          'unlock1Event': 14020,
          'unlock2Event': 0,
          'unlock3Event': 0},
 14020: {'type': 'button',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(54.1377, -36.0275, 0.0249996),
         'hpr': Vec3(0, 0, 0),
         'scale': Point3(3, 3, 3),
         'color': Vec4(1, 0, 0, 1),
         'isOn': 0,
         'isOnEvent': 0,
         'secondsOn': -1.0},
 20111: {'type': 'healBarrel',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(20.9015, 78.8094, 0.0239558),
         'hpr': Vec3(0, 0, 0),
         'scale': 1,
         'rewardPerGrab': 10,
         'rewardPerGrabMax': 0},
 20211: {'type': 'healBarrel',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(-29.4342, 45.2614, 0.0239525),
         'hpr': Vec3(180, 0, 0),
         'scale': 1,
         'rewardPerGrab': 10,
         'rewardPerGrabMax': 0},
 20311: {'type': 'healBarrel',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(16.7276, 200.07, 0.0239558),
         'hpr': Vec3(180, 0, 0),
         'scale': 1,
         'rewardPerGrab': 10,
         'rewardPerGrabMax': 0},
 145010: {'type': 'path',
          'name': 'GoonPath1',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(0, 0, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'pathIndex': 80,
          'pathScale': 1.0},
 145000: {'type': 'goon',
          'name': '<unnamed>',
          'comment': '',
          'parentEntId': 145010,
          'pos': Point3(0, 0, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': 1.75,
          'attackRadius': 6.0,
          'crushCellId': None,
          'goonType': 'sg',
          'gridId': None,
          'hFov': 90.0,
          'strength': 24,
          'velocity': 4},
 145110: {'type': 'path',
          'name': 'GoonPath2',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(0, 0, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'pathIndex': 81,
          'pathScale': 1.0},
 145100: {'type': 'goon',
          'name': '<unnamed>',
          'comment': '',
          'parentEntId': 145110,
          'pos': Point3(0, 0, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': 1.75,
          'attackRadius': 6.0,
          'crushCellId': None,
          'goonType': 'sg',
          'gridId': None,
          'hFov': 90.0,
          'strength': 24,
          'velocity': 4},
 145210: {'type': 'path',
          'name': 'GoonPath2',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(0, 0, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'pathIndex': 82,
          'pathScale': 1.0},
 145200: {'type': 'goon',
          'name': '<unnamed>',
          'comment': '',
          'parentEntId': 145210,
          'pos': Point3(0, 0, 0),
          'hpr': Vec3(0, 0, 0),
          'scale': 1.75,
          'attackRadius': 6.0,
          'crushCellId': None,
          'goonType': 'sg',
          'gridId': None,
          'hFov': 90.0,
          'strength': 24,
          'velocity': 4},
 10000: {'type': 'nodepath',
         'name': 'cogs',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Point3(270.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0)},
 11000: {'type': 'nodepath',
         'name': 'cogs',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(1.3663, 234.45, 0.0239544),
         'hpr': Vec3(-180.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0)},
 10002: {'type': 'nodepath',
         'name': 'props',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1},
 10004: {'type': 'nodepath',
         'name': 'collisions',
         'comment': '',
         'parentEntId': 10002,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1}}
Scenario0 = {}
levelSpec = {'globalEntities': GlobalEntities,
 'scenarios': [Scenario0]}