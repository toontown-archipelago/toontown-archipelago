from panda3d.core import *
from . import TTLocalizer
import random
GlobalEntities = {1000: {'type': 'levelMgr', 'name': 'UberZone', 'comment': '', 'parentEntId': 0, 'cogLevel': 0, 'farPlaneDistance': 1500, 'modelFilename': 'phase_10/models/cashbotHQ/ZONE08a.bam', 'wantDoors': 1}, 1001: {'type': 'editMgr', 'name': 'EditMgr', 'parentEntId': 0, 'insertEntity': None, 'removeEntity': None, 'requestNewEntity': None, 'requestSave': None}, 0: {'type': 'zone', 'name': 'UberZone', 'comment': '', 'parentEntId': 0, 'scale': LVecBase3f(1, 1, 1), 'description': '', 'visibility': []}, 140050051: {'type': 'button', 'name': '<unnamed>', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(5.8654, -39.4956, 9.34462), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(5, 5, 5), 'color': LVector4f(1, 0, 0, 1), 'isOn': 0, 'isOnEvent': 0, 'secondsOn': -1.0}, 140000051: {'type': 'door', 'name': '<unnamed>', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(-1.05295, 49.1, 5.6), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(0.8, 0.8, 0.8), 'color': LVector4f(1, 1, 1, 1), 'isLock0Unlocked': 1, 'isLock1Unlocked': 0, 'isLock2Unlocked': 1, 'isLock3Unlocked': 1, 'isOpen': 0, 'isOpenEvent': 0, 'isVisBlocker': 0, 'secondsOpen': 1, 'unlock0Event': 0, 'unlock1Event': 140050051, 'unlock2Event': 0, 'unlock3Event': 0}, 700556000: {'type': 'goon', 'name': '<unnamed>', 'comment': '', 'parentEntId': 7005596000, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': 1.3, 'attackRadius': 10, 'crushCellId': None, 'goonType': 'pg', 'gridId': None, 'hFov': 70, 'strength': 12.0, 'velocity': 3.2}, 7005596000: {'type': 'path', 'name': 'nearPace', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'pathIndex': 110.0, 'pathScale': 1.0}, 700656000: {'type': 'goon', 'name': '<unnamed>', 'comment': '', 'parentEntId': 7006596000, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': 1.7, 'attackRadius': 10, 'crushCellId': None, 'goonType': 'pg', 'gridId': None, 'hFov': 70, 'strength': 18.0, 'velocity': 3.2}, 7006596000: {'type': 'path', 'name': 'nearPace', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'pathIndex': 111.0, 'pathScale': 1.0}, 70010049: {'type': 'stomper', 'name': 'first', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(58.7457, -31.1033, 0.0247555), 'hpr': LVecBase3f(0, -0, 0), 'scale': LVecBase3f(1.1, 1.1, 1), 'animateShadow': 1, 'crushCellId': None, 'damage': 10.0, 'headScale': LVecBase3f(5, 6, 6.25), 'modelPath': 0, 'motion': 3, 'period': 3.5, 'phaseShift': 0.34, 'range': 7.0, 'removeCamBarrierCollisions': 0, 'removeHeadFloor': 1, 'shaftScale': LVecBase3f(1, 10, 1), 'soundLen': 0, 'soundOn': 1, 'soundPath': 1, 'style': 'vertical', 'switchId': 0, 'wantShadow': 1, 'wantSmoke': 1, 'zOffset': 0}, 70020049: {'type': 'stomper', 'name': 'second', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(25.7869, -32.433, 0.0247555), 'hpr': LVecBase3f(0, -0, 0), 'scale': LVecBase3f(2.7, 1.4, 1), 'animateShadow': 1, 'crushCellId': None, 'damage': 10.0, 'headScale': LVecBase3f(5, 6, 6.25), 'modelPath': 0, 'motion': 3, 'period': 4.0, 'phaseShift': 0.34, 'range': 7.0, 'removeCamBarrierCollisions': 0, 'removeHeadFloor': 1, 'shaftScale': LVecBase3f(1, 10, 1), 'soundLen': 0, 'soundOn': 1, 'soundPath': 1, 'style': 'vertical', 'switchId': 0, 'wantShadow': 1, 'wantSmoke': 1, 'zOffset': 0}, 70030049: {'type': 'stomper', 'name': 'third', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(-23.4182, -37.8725, 0.0247555), 'hpr': LVecBase3f(0, -0, 0), 'scale': LVecBase3f(1.5, 1.5, 1.5), 'animateShadow': 1, 'crushCellId': None, 'damage': 10.0, 'headScale': LVecBase3f(5, 6, 6.25), 'modelPath': 0, 'motion': 3, 'period': 3.0, 'phaseShift': 0.34, 'range': 7.0, 'removeCamBarrierCollisions': 0, 'removeHeadFloor': 1, 'shaftScale': LVecBase3f(1, 10, 1), 'soundLen': 0, 'soundOn': 1, 'soundPath': 1, 'style': 'vertical', 'switchId': 0, 'wantShadow': 1, 'wantSmoke': 1, 'zOffset': 0}, 70040049: {'type': 'stomper', 'name': 'fourth', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(-60.2476, -26.2141, 0.0247555), 'hpr': LVecBase3f(0, -0, 0), 'scale': LVecBase3f(1, 2, 2.8), 'animateShadow': 1, 'crushCellId': None, 'damage': 10.0, 'headScale': LVecBase3f(5, 6, 6.25), 'modelPath': 0, 'motion': 3, 'period': 3.3, 'phaseShift': 0.34, 'range': 7.0, 'removeCamBarrierCollisions': 0, 'removeHeadFloor': 1, 'shaftScale': LVecBase3f(1, 10, 1), 'soundLen': 0, 'soundOn': 1, 'soundPath': 1, 'style': 'vertical', 'switchId': 0, 'wantShadow': 1, 'wantSmoke': 1, 'zOffset': 0}, 70050049: {'type': 'stomper', 'name': 'fifth', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(-29.729, -7.9176, 0.0249996), 'hpr': LVecBase3f(0, -0, 0), 'scale': LVecBase3f(1.6, 1.6, 1.6), 'animateShadow': 1, 'crushCellId': None, 'damage': 10.0, 'headScale': LVecBase3f(5, 6, 6.25), 'modelPath': 0, 'motion': 3, 'period': 1.06, 'phaseShift': 0.34, 'range': 7.0, 'removeCamBarrierCollisions': 0, 'removeHeadFloor': 1, 'shaftScale': LVecBase3f(1, 10, 1), 'soundLen': 0, 'soundOn': 1, 'soundPath': 1, 'style': 'vertical', 'switchId': 0, 'wantShadow': 1, 'wantSmoke': 1, 'zOffset': 0}, 10041: {'type': 'healBarrel', 'name': 'happie', 'comment': '', 'parentEntId': 10033, 'pos': LPoint3f(5.40611, 0, 0), 'hpr': LVecBase3f(199.44, 0, 0), 'scale': 1, 'apRewardIndex': 0, 'rewardPerGrab': 6, 'rewardPerGrabMax': 8}, 10034: {'type': 'healBarrel', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10033, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(163.301, 0, 0), 'scale': 1, 'rewardPerGrab': 7, 'rewardPerGrabMax': 9}, 10015: {'type': 'mintProductPallet', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10014, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12500}, 10016: {'type': 'mintProductPallet', 'name': 'copy of <unnamed>', 'comment': '', 'parentEntId': 10014, 'pos': LPoint3f(0, 13.6865, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10017: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (2)', 'comment': '', 'parentEntId': 10014, 'pos': LPoint3f(0, 27.38, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12600}, 10018: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (3)', 'comment': '', 'parentEntId': 10014, 'pos': LPoint3f(0, 41.07, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10019: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (4)', 'comment': '', 'parentEntId': 10014, 'pos': LPoint3f(0, 54.76, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10020: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (5)', 'comment': '', 'parentEntId': 10014, 'pos': LPoint3f(0, 68.45, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12500}, 10022: {'type': 'mintProductPallet', 'name': 'copy of <unnamed>', 'comment': '', 'parentEntId': 10021, 'pos': LPoint3f(16.8028, 93.3008, 11.5793), 'hpr': LVecBase3f(36.3844, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10025: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (4)', 'comment': '', 'parentEntId': 10045, 'pos': LPoint3f(0, 54.76, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10026: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (5)', 'comment': '', 'parentEntId': 10045, 'pos': LPoint3f(0, 68.45, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12500}, 10036: {'type': 'mintProductPallet', 'name': 'copy of <unnamed>', 'comment': '', 'parentEntId': 10035, 'pos': LPoint3f(0, 13.6865, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10037: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (2)', 'comment': '', 'parentEntId': 10035, 'pos': LPoint3f(0, 27.38, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12600}, 10038: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (3)', 'comment': '', 'parentEntId': 10035, 'pos': LPoint3f(0, 41.07, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12700}, 10043: {'type': 'mintProductPallet', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(-36.6624, -39.0315, 0), 'hpr': LVecBase3f(90, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12500}, 10044: {'type': 'mintProductPallet', 'name': 'copy of <unnamed> (2)', 'comment': '', 'parentEntId': 10021, 'pos': LPoint3f(10.6009, 119.829, 11.7728), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'mintId': 12600}, 10004: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10021, 'pos': LPoint3f(0, -1.09805, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(2, 2, 2), 'collisionsOnly': 0, 'flattenType': 'strong', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 1000009: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(-8.56483, -31.7742, 0.0205088), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1.7, 1.7, 1.7), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10009: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10008, 'pos': LPoint3f(-3.99621, 0.695079, 0.0113303), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1.2, 1.2, 1.2), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cashbotHQ/crates_E.bam'}, 10010: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10008, 'pos': LPoint3f(48.053, -0.531661, -0.327079), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cashbotHQ/crates_C1.bam'}, 10012: {'type': 'model', 'name': 'rightCrates', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(36.0373, 71.3547, 9.99836), 'hpr': LVecBase3f(315, 0, 0), 'scale': LVecBase3f(1.5, 1.5, 1.5), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cashbotHQ/crates_E.bam'}, 10024: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10028, 'pos': LPoint3f(-3.73286, 27.1218, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(2, 2, 2), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10027: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10028, 'pos': LPoint3f(-11.9349, 38.9528, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(2, 2, 2), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10029: {'type': 'model', 'name': 'crate', 'comment': '', 'parentEntId': 10035, 'pos': LPoint3f(0, 0.863602, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(2, 2, 2), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10030: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10023, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10031: {'type': 'model', 'name': 'copy of crate', 'comment': '', 'parentEntId': 10029, 'pos': LPoint3f(0, 0, 5.47), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10032: {'type': 'model', 'name': 'copy of <unnamed>', 'comment': '', 'parentEntId': 10023, 'pos': LPoint3f(0, -5.92218, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10039: {'type': 'model', 'name': '<unnamed>', 'comment': '', 'parentEntId': 10010, 'pos': LPoint3f(-9.23663, 0.821144, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1.5, 1.5, 1.5), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cashbotHQ/crates_F1.bam'}, 10042: {'type': 'model', 'name': 'copy of <unnamed> (2)', 'comment': '', 'parentEntId': 10023, 'pos': LPoint3f(3, -11.84, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam'}, 10048: {'type': 'model', 'name': 'cratesAgainstWall', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(-37.0983, 70.2134, 10), 'hpr': LVecBase3f(225, 0, 0), 'scale': LVecBase3f(1.5, 1.5, 1.5), 'collisionsOnly': 0, 'flattenType': 'light', 'loadType': 'loadModelCopy', 'modelPath': 'phase_10/models/cashbotHQ/crates_E.bam'}, 10000: {'type': 'nodepath', 'name': 'cogs', 'comment': '', 'parentEntId': 10011, 'pos': LPoint3f(0, 66.12, 10.1833), 'hpr': LVecBase3f(270, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10002: {'type': 'nodepath', 'name': 'battle', 'comment': '', 'parentEntId': 10000, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(90, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10003: {'type': 'nodepath', 'name': 'cogs2', 'comment': '', 'parentEntId': 10011, 'pos': LPoint3f(-53.9247, -22.7616, 0), 'hpr': LVecBase3f(45, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10005: {'type': 'nodepath', 'name': 'battle', 'comment': '', 'parentEntId': 10003, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10007: {'type': 'nodepath', 'name': 'props', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10008: {'type': 'nodepath', 'name': 'topWall', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(0, 48.03, 10), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10011: {'type': 'nodepath', 'name': 'cogs', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10013: {'type': 'nodepath', 'name': 'frontCogs', 'comment': '', 'parentEntId': 10011, 'pos': LPoint3f(25.3957, -12.3006, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10014: {'type': 'nodepath', 'name': 'frontPalletWall', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(45.5494, 38.2237, 0), 'hpr': LVecBase3f(180, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10021: {'type': 'nodepath', 'name': 'middlePalletWallLeft', 'comment': '', 'parentEntId': 10046, 'pos': LPoint3f(6, -37.9929, -1.62558), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10023: {'type': 'nodepath', 'name': 'crateIsland', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(-12.9143, 10.4435, 0.01), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(2, 2, 2)}, 10028: {'type': 'nodepath', 'name': 'rewardCulDeSac', 'comment': '', 'parentEntId': 10045, 'pos': LPoint3f(-8.26172, 38.3774, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10033: {'type': 'nodepath', 'name': 'barrels', 'comment': '', 'parentEntId': 10028, 'pos': LPoint3f(-4.75078, 34.1425, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10035: {'type': 'nodepath', 'name': 'backPalletWall', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(-47.6502, 40.0069, 0), 'hpr': LVecBase3f(180, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10040: {'type': 'nodepath', 'name': 'centerCogs', 'comment': '', 'parentEntId': 10011, 'pos': LPoint3f(-23.9376, 28.3533, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10045: {'type': 'nodepath', 'name': 'middlePalletWallRight', 'comment': '', 'parentEntId': 10046, 'pos': LPoint3f(17.42, -38.3, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 10046: {'type': 'nodepath', 'name': 'middlePalletWall', 'comment': '', 'parentEntId': 10007, 'pos': LPoint3f(0, 0, 0), 'hpr': LVecBase3f(0, 0, 0), 'scale': LVecBase3f(1, 1, 1)}, 180000: {'type': 'healBarrel', 'name': 'happie_2', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(24.7684, 72.6028, 9.96114), 'hpr': LVecBase3f(318.013, 0, 0), 'scale': 1, 'rewardPerGrab': 10, 'rewardPerGrabMax': 10}, 180010: {'type': 'healBarrel', 'name': 'happie', 'comment': '', 'parentEntId': 0, 'pos': LPoint3f(26.0562, 68.5209, 9.99362), 'hpr': LVecBase3f(285.005, 0, 0), 'scale': 1, 'rewardPerGrab': 10, 'rewardPerGrabMax': 10}}

"""
GlobalEntities[180000] = {'type': 'healBarrel',
          'name': 'healBuddy',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(0, 0, 0.0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'rewardPerGrab': 16,
          'rewardPerGrabMax': 16}

GlobalEntities[180001] = {'type': 'healBarrel',
          'name': 'healBuddy',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(0, 0, 0.0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'rewardPerGrab': 16,
          'rewardPerGrabMax': 16}

GlobalEntities[180002] = {'type': 'healBarrel',
          'name': 'healBuddy',
          'comment': '',
          'parentEntId': 0,
          'pos': Point3(0, 0, 0.0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'rewardPerGrab': 16,
          'rewardPerGrabMax': 16}


GlobalEntities[16000] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_couchA.bam'}

GlobalEntities[16001] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_couchA.bam'}

GlobalEntities[16002] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_filing_cab.bam'}

GlobalEntities[16003] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_filing_cab.bam'}

GlobalEntities[16004] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_endtableA.bam'}

GlobalEntities[16005] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampA.bam'}

GlobalEntities[16006] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampA.bam'}

GlobalEntities[16007] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA.bam'}

GlobalEntities[16008] = {'type': 'model',
         'name': 'middle',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox.bam'}




GlobalEntities[180010] = {'type': 'healBarrel',
          'name': 'archi',
          'comment': '',
          'parentEntId': 1000,
          'pos': Point3(0, 0, 0.0),
          'hpr': Vec3(0, 0, 0),
          'scale': Vec3(1, 1, 1),
          'rewardPerGrab': 10,
          'rewardPerGrabMax': 10}

"""