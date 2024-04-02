import random
from dataclasses import dataclass
from typing import Set, List

from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toonbase import TTLocalizer
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
notify = directNotify.newCategory('SuitDNA')
suitHeadTypes = ['f',
 'p',
 'ym',
 'mm',
 'ds',
 'hh',
 'cr',
 'tbc',
 'bf',
 'b',
 'dt',
 'ac',
 'bs',
 'sd',
 'le',
 'bw',
 'sc',
 'pp',
 'tw',
 'bc',
 'nc',
 'mb',
 'ls',
 'rb',
 'cc',
 'tm',
 'nd',
 'gh',
 'ms',
 'tf',
 'm',
 'mh']
suitATypes = ['ym',
 'hh',
 'tbc',
 'dt',
 'bs',
 'le',
 'bw',
 'pp',
 'nc',
 'rb',
 'nd',
 'tf',
 'm',
 'mh']
suitBTypes = ['p',
 'ds',
 'b',
 'ac',
 'sd',
 'bc',
 'ls',
 'tm',
 'ms']
suitCTypes = ['f',
 'mm',
 'cr',
 'bf',
 'sc',
 'tw',
 'mb',
 'cc',
 'gh']
suitDepts = ['c',
 'l',
 'm',
 's']
suitDeptFullnames = {'c': TTLocalizer.Bossbot,
 'l': TTLocalizer.Lawbot,
 'm': TTLocalizer.Cashbot,
 's': TTLocalizer.Sellbot}
suitDeptFullnamesP = {'c': TTLocalizer.BossbotP,
 'l': TTLocalizer.LawbotP,
 'm': TTLocalizer.CashbotP,
 's': TTLocalizer.SellbotP}
corpPolyColor = VBase4(0.95, 0.75, 0.75, 1.0)
legalPolyColor = VBase4(0.75, 0.75, 0.95, 1.0)
moneyPolyColor = VBase4(0.65, 0.95, 0.85, 1.0)
salesPolyColor = VBase4(0.95, 0.75, 0.95, 1.0)
suitsPerLevel = [1,
 1,
 1,
 1,
 1,
 1,
 1,
 1]
suitsPerDept = 8
goonTypes = ['pg', 'sg']


@dataclass
class SuitAnimation:
    key:   str  # The key that the codebase references this animation by.
    suit:  str  # The body type of suit this animation is for. Either A/B/C.
    path:  str  # The path/filename of the animation in resources.
    phase: str  # The phase folder this animation is contained in. Usually an int or 3.5/5.5

    def unique_key(self) -> str:
        return f"{self.key}-{self.suit}"

    def modelPath(self) -> str:
        return f"phase_{self.phase}/models/char/suit{self.suit}-{self.path}"

    def usedForSuitBody(self, bodyType: str):
        return bodyType.upper() == self.suit

    def __hash__(self):
        return self.unique_key().__hash__()


# Define a list of suit animations that every suit has.
__GENERAL_SUIT_ANIMATIONS: Set[SuitAnimation] = {

    # Global animations every suit has.
    SuitAnimation(key='walk', suit='A', path='walk', phase='4'),
    SuitAnimation(key='walk', suit='B', path='walk', phase='4'),
    SuitAnimation(key='walk', suit='C', path='walk', phase='3.5'),
    SuitAnimation(key='run', suit='A', path='walk', phase='4'),
    SuitAnimation(key='run', suit='B', path='walk', phase='4'),
    SuitAnimation(key='run', suit='C', path='walk', phase='3.5'),
    SuitAnimation(key='neutral', suit='A', path='neutral', phase='4'),
    SuitAnimation(key='neutral', suit='B', path='neutral', phase='4'),
    SuitAnimation(key='neutral', suit='C', path='neutral', phase='3.5'),
    SuitAnimation(key='lured', suit='A', path='lured', phase='5'),
    SuitAnimation(key='lured', suit='B', path='lured', phase='5'),
    SuitAnimation(key='lured', suit='C', path='lured', phase='5'),

    # "Minigame" animations that every suit has.
    SuitAnimation(key='victory', suit='A', path='victory', phase='4'),
    SuitAnimation(key='victory', suit='B', path='victory', phase='4'),
    SuitAnimation(key='victory', suit='C', path='victory', phase='4'),
    SuitAnimation(key='flail', suit='A', path='flailing', phase='4'),
    SuitAnimation(key='flail', suit='B', path='flailing', phase='4'),
    SuitAnimation(key='flail', suit='C', path='flailing', phase='4'),
    SuitAnimation(key='tug-o-war', suit='A', path='tug-o-war', phase='4'),
    SuitAnimation(key='tug-o-war', suit='B', path='tug-o-war', phase='4'),
    SuitAnimation(key='tug-o-war', suit='C', path='tug-o-war', phase='4'),
    SuitAnimation(key='slip-backward', suit='A', path='slip-backward', phase='4'),
    SuitAnimation(key='slip-backward', suit='B', path='slip-backward', phase='4'),
    SuitAnimation(key='slip-backward', suit='C', path='slip-backward', phase='4'),
    SuitAnimation(key='slip-forward', suit='A', path='slip-forward', phase='4'),
    SuitAnimation(key='slip-forward', suit='B', path='slip-forward', phase='4'),
    SuitAnimation(key='slip-forward', suit='C', path='slip-forward', phase='4'),

    # General battle animations.
    SuitAnimation(key='lose', suit='A', path='lose', phase='4'),
    SuitAnimation(key='lose', suit='B', path='lose', phase='4'),
    SuitAnimation(key='lose', suit='C', path='lose', phase='3.5'),
    SuitAnimation(key='pie-small-react', suit='A', path='pie-small', phase='4'),
    SuitAnimation(key='pie-small-react', suit='B', path='pie-small', phase='4'),
    SuitAnimation(key='pie-small-react', suit='C', path='pie-small', phase='3.5'),
    SuitAnimation(key='squirt-small-react', suit='A', path='squirt-small', phase='4'),
    SuitAnimation(key='squirt-small-react', suit='B', path='squirt-small', phase='4'),
    SuitAnimation(key='squirt-small-react', suit='C', path='squirt-small', phase='3.5'),
    SuitAnimation(key='drop-react', suit='A', path='anvil-drop', phase='5'),
    SuitAnimation(key='drop-react', suit='B', path='anvil-drop', phase='5'),
    SuitAnimation(key='drop-react', suit='C', path='anvil-drop', phase='5'),
    SuitAnimation(key='flatten', suit='A', path='drop', phase='5'),
    SuitAnimation(key='flatten', suit='B', path='drop', phase='5'),
    SuitAnimation(key='flatten', suit='C', path='drop', phase='5'),
    SuitAnimation(key='sidestep-left', suit='A', path='sidestep-left', phase='5'),
    SuitAnimation(key='sidestep-left', suit='B', path='sidestep-left', phase='5'),
    SuitAnimation(key='sidestep-left', suit='C', path='sidestep-left', phase='5'),
    SuitAnimation(key='sidestep-right', suit='A', path='sidestep-right', phase='5'),
    SuitAnimation(key='sidestep-right', suit='B', path='sidestep-right', phase='5'),
    SuitAnimation(key='sidestep-right', suit='C', path='sidestep-right', phase='5'),
    SuitAnimation(key='squirt-large-react', suit='A', path='squirt-large', phase='5'),
    SuitAnimation(key='squirt-large-react', suit='B', path='squirt-large', phase='5'),
    SuitAnimation(key='squirt-large-react', suit='C', path='squirt-large', phase='5'),
    SuitAnimation(key='landing', suit='A', path='landing', phase='5'),
    SuitAnimation(key='landing', suit='B', path='landing', phase='5'),
    SuitAnimation(key='landing', suit='C', path='landing', phase='5'),
    SuitAnimation(key='reach', suit='A', path='walknreach', phase='5'),
    SuitAnimation(key='reach', suit='B', path='walknreach', phase='5'),
    SuitAnimation(key='reach', suit='C', path='walknreach', phase='5'),
    SuitAnimation(key='rake-react', suit='A', path='rake', phase='5'),
    SuitAnimation(key='rake-react', suit='B', path='rake', phase='5'),
    SuitAnimation(key='rake-react', suit='C', path='rake', phase='5'),
    SuitAnimation(key='hypnotized', suit='A', path='hypnotize', phase='5'),
    SuitAnimation(key='hypnotized', suit='B', path='hypnotize', phase='5'),
    SuitAnimation(key='hypnotized', suit='C', path='hypnotize', phase='5'),
    SuitAnimation(key='soak', suit='A', path='soak', phase='5'),
    SuitAnimation(key='soak', suit='B', path='soak', phase='5'),
    SuitAnimation(key='soak', suit='C', path='soak', phase='5'),

    # CEO Diner animations.
    SuitAnimation(key='sit', suit='A', path='sit', phase='12'),
    SuitAnimation(key='sit', suit='B', path='sit', phase='12'),
    SuitAnimation(key='sit', suit='C', path='sit', phase='12'),
    SuitAnimation(key='sit-eat-in', suit='A', path='sit-eat-in', phase='12'),
    SuitAnimation(key='sit-eat-in', suit='B', path='sit-eat-in', phase='12'),
    SuitAnimation(key='sit-eat-in', suit='C', path='sit-eat-in', phase='12'),
    SuitAnimation(key='sit-eat-loop', suit='A', path='sit-eat-loop', phase='12'),
    SuitAnimation(key='sit-eat-loop', suit='B', path='sit-eat-loop', phase='12'),
    SuitAnimation(key='sit-eat-loop', suit='C', path='sit-eat-loop', phase='12'),
    SuitAnimation(key='sit-eat-out', suit='A', path='sit-eat-out', phase='12'),
    SuitAnimation(key='sit-eat-out', suit='B', path='sit-eat-out', phase='12'),
    SuitAnimation(key='sit-eat-out', suit='C', path='sit-eat-out', phase='12'),
    SuitAnimation(key='sit-angry', suit='A', path='sit-angry', phase='12'),
    SuitAnimation(key='sit-angry', suit='B', path='sit-angry', phase='12'),
    SuitAnimation(key='sit-angry', suit='C', path='sit-angry', phase='12'),
    SuitAnimation(key='sit-hungry-left', suit='A', path='leftsit-hungry', phase='12'),
    SuitAnimation(key='sit-hungry-left', suit='B', path='leftsit-hungry', phase='12'),
    SuitAnimation(key='sit-hungry-left', suit='C', path='leftsit-hungry', phase='12'),
    SuitAnimation(key='sit-hungry-right', suit='A', path='rightsit-hungry', phase='12'),
    SuitAnimation(key='sit-hungry-right', suit='B', path='rightsit-hungry', phase='12'),
    SuitAnimation(key='sit-hungry-right', suit='C', path='rightsit-hungry', phase='12'),
    SuitAnimation(key='sit-lose', suit='A', path='sit-lose', phase='12'),
    SuitAnimation(key='sit-lose', suit='B', path='sit-lose', phase='12'),
    SuitAnimation(key='sit-lose', suit='C', path='sit-lose', phase='12'),
    SuitAnimation(key='tray-walk', suit='A', path='tray-walk', phase='12'),
    SuitAnimation(key='tray-walk', suit='B', path='tray-walk', phase='12'),
    SuitAnimation(key='tray-walk', suit='C', path='tray-walk', phase='12'),
    SuitAnimation(key='tray-neutral', suit='A', path='tray-neutral', phase='12'),
    SuitAnimation(key='tray-neutral', suit='B', path='tray-neutral', phase='12'),
    SuitAnimation(key='tray-neutral', suit='C', path='tray-neutral', phase='12'),
    SuitAnimation(key='sit-lose', suit='A', path='sit-lose', phase='12'),
    SuitAnimation(key='sit-lose', suit='B', path='sit-lose', phase='12'),
    SuitAnimation(key='sit-lose', suit='C', path='sit-lose', phase='12'),
}

__SUIT_BATTLE_ANIMATIONS: Set[SuitAnimation] = {

    # Animations shared between all body types.
    SuitAnimation(key='pickpocket', suit='A', path='pickpocket', phase='5'),
    SuitAnimation(key='pickpocket', suit='B', path='pickpocket', phase='5'),
    SuitAnimation(key='pickpocket', suit='C', path='pickpocket', phase='5'),

    SuitAnimation(key='magic1', suit='A', path='magic1', phase='5'),
    SuitAnimation(key='magic1', suit='B', path='magic1', phase='5'),
    SuitAnimation(key='magic1', suit='C', path='magic1', phase='5'),

    SuitAnimation(key='magic2', suit='A', path='magic2', phase='5'),
    SuitAnimation(key='magic2', suit='B', path='magic2', phase='5'),
    SuitAnimation(key='magic2', suit='C', path='magic2', phase='5'),

    SuitAnimation(key='pen-squirt', suit='A', path='fountain-pen', phase='7'),
    SuitAnimation(key='pen-squirt', suit='B', path='pen-squirt', phase='5'),
    SuitAnimation(key='pen-squirt', suit='C', path='fountain-pen', phase='5'),

    SuitAnimation(key='throw-paper', suit='A', path='throw-paper', phase='5'),
    SuitAnimation(key='throw-paper', suit='B', path='throw-paper', phase='5'),
    SuitAnimation(key='throw-paper', suit='C', path='throw-paper', phase='3.5'),

    SuitAnimation(key='finger-wag', suit='A', path='fingerwag', phase='5'),
    SuitAnimation(key='finger-wag', suit='B', path='finger-wag', phase='5'),
    SuitAnimation(key='finger-wag', suit='C', path='finger-wag', phase='5'),

    SuitAnimation(key='phone', suit='A', path='phone', phase='5'),
    SuitAnimation(key='phone', suit='B', path='phone', phase='5'),
    SuitAnimation(key='phone', suit='C', path='phone', phase='3.5'),

    SuitAnimation(key='speak', suit='A', path='speak', phase='5'),
    SuitAnimation(key='speak', suit='B', path='speak', phase='5'),
    SuitAnimation(key='speak', suit='C', path='speak', phase='5'),

    # AB Animations (C cannot use).
    SuitAnimation(key='roll-o-dex', suit='A', path='roll-o-dex', phase='5'),
    SuitAnimation(key='roll-o-dex', suit='B', path='roll-o-dex', phase='5'),

    SuitAnimation(key='throw-object', suit='A', path='throw-object', phase='5'),
    SuitAnimation(key='throw-object', suit='B', path='throw-object', phase='5'),

    SuitAnimation(key='magic3', suit='A', path='magic3', phase='5'),
    SuitAnimation(key='magic3', suit='B', path='magic3', phase='5'),

    # AC Animations (B cannot use).
    SuitAnimation(key='rubber-stamp', suit='A', path='rubber-stamp', phase='5'),
    SuitAnimation(key='rubber-stamp', suit='C', path='rubber-stamp', phase='5'),

    SuitAnimation(key='glower', suit='A', path='glower', phase='5'),
    SuitAnimation(key='glower', suit='C', path='glower', phase='5'),

    # CB Animations (A Cannot use).
    SuitAnimation(key='effort', suit='C', path='effort', phase='5'),
    SuitAnimation(key='effort', suit='B', path='effort', phase='5'),

    # Animations exclusive to Suit A (Muscular).
    SuitAnimation(key='smile', suit='A', path='smile', phase='5'),
    SuitAnimation(key='cigar-smoke', suit='A', path='cigar-smoke', phase='8'),
    SuitAnimation(key='song-and-dance', suit='A', path='song-and-dance', phase='8'),
    SuitAnimation(key='golf-club-swing', suit='A', path='golf-club-swing', phase='5'),
    SuitAnimation(key='gavel', suit='A', path='gavel', phase='8'),

    # Animations exlcusive to Suit B (Skinny).
    SuitAnimation(key='hold-pencil', suit='B', path='hold-pencil', phase='5'),
    SuitAnimation(key='pencil-sharpener', suit='B', path='pencil-sharpener', phase='5'),
    SuitAnimation(key='hold-eraser', suit='B', path='hold-eraser', phase='5'),
    SuitAnimation(key='quick-jump', suit='B', path='jump', phase='6'),
    SuitAnimation(key='stomp', suit='B', path='stomp', phase='5'),

    # Animations exclusive to Suit C (Fat).
    SuitAnimation(key='shredder', suit='C', path='shredder', phase='3.5'),
    SuitAnimation(key='watercooler', suit='C', path='watercooler', phase='5'),
}


def getSuitBodyType(name):
    if name in suitATypes:
        return 'a'
    elif name in suitBTypes:
        return 'b'
    elif name in suitCTypes:
        return 'c'
    else:
        print('Unknown body type for suit name: ', name)


def getGeneralAnimationsForSuitBody(bodyType: str) -> List[SuitAnimation]:
    animations: List[SuitAnimation] = []

    for animation in __GENERAL_SUIT_ANIMATIONS:

        # Skip animations not used for this body.
        if not animation.usedForSuitBody(bodyType):
            continue

        animations.append(animation)

    return animations


def getBattleAnimationsForSuit(suitName: str, attackKeys: Set[str]) -> List[SuitAnimation]:
    animations: List[SuitAnimation] = []
    bodyType = getSuitBodyType(suitName)

    for animation in __SUIT_BATTLE_ANIMATIONS:

        # Skip attack animations this suit doesn't possess.
        # This probably isn't needed, but it seems like it is a memory optimization.
        if animation.key not in attackKeys:
            continue

        # Skip animations this suit can't use because of their body.
        if not animation.usedForSuitBody(bodyType):
            continue

        animations.append(animation)

    return animations


def getSuitDept(name):
    index = suitHeadTypes.index(name)
    if index < suitsPerDept:
        return suitDepts[0]
    elif index < suitsPerDept * 2:
        return suitDepts[1]
    elif index < suitsPerDept * 3:
        return suitDepts[2]
    elif index < suitsPerDept * 4:
        return suitDepts[3]
    else:
        print('Unknown dept for suit name: ', name)
        return None
    return None


def getDeptFullname(dept):
    return suitDeptFullnames[dept]


def getDeptFullnameP(dept):
    return suitDeptFullnamesP[dept]


def getSuitDeptFullname(name):
    return suitDeptFullnames[getSuitDept(name)]


def getSuitType(name):
    index = suitHeadTypes.index(name)
    return index % suitsPerDept + 1


def getRandomSuitType(level, rng = random):
    if level >= 11:
        return random.choice([6, 7, 8])
    else:
        return random.randint(max(level - 4, 1), min(level, 8))


def getRandomSuitByDept(dept):
    deptNumber = suitDepts.index(dept)
    return suitHeadTypes[suitsPerDept * deptNumber + random.randint(0, 7)]


class SuitDNA(AvatarDNA.AvatarDNA):

    def __init__(self, str = None, type = None, dna = None, r = None, b = None, g = None):
        if str != None:
            self.makeFromNetString(str)
        elif type != None:
            if type == 's':
                self.newSuit()
        else:
            self.type = 'u'
        return

    def __str__(self):
        if self.type == 's':
            return 'type = %s\nbody = %s, dept = %s, name = %s' % ('suit',
             self.body,
             self.dept,
             self.name)
        elif self.type == 'b':
            return 'type = boss cog\ndept = %s' % self.dept
        else:
            return 'type undefined'

    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if self.type == 's':
            dg.addFixedString(self.name, 3)
            dg.addFixedString(self.dept, 1)
        elif self.type == 'b':
            dg.addFixedString(self.dept, 1)
        elif self.type == 'u':
            notify.error('undefined avatar')
        else:
            notify.error('unknown avatar type: ', self.type)
        return dg.getMessage()

    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 's':
            self.name = dgi.getFixedString(3)
            self.dept = dgi.getFixedString(1)
            self.body = getSuitBodyType(self.name)
        elif self.type == 'b':
            self.dept = dgi.getFixedString(1)
        else:
            notify.error('unknown avatar type: ', self.type)
        return None

    def __defaultGoon(self):
        self.type = 'g'
        self.name = goonTypes[0]

    def __defaultSuit(self):
        self.type = 's'
        self.name = 'ds'
        self.dept = getSuitDept(self.name)
        self.body = getSuitBodyType(self.name)

    def newSuit(self, name = None):
        if name == None:
            self.__defaultSuit()
        else:
            self.type = 's'
            self.name = name
            self.dept = getSuitDept(self.name)
            self.body = getSuitBodyType(self.name)
        return

    def newBossCog(self, dept):
        self.type = 'b'
        self.dept = dept

    def newSuitRandom(self, level = None, dept = None):
        self.type = 's'
        if level == None:
            level = random.choice(list(range(1, len(suitsPerLevel))))
        elif level < 0 or level > len(suitsPerLevel):
            notify.error('Invalid suit level: %d' % level)
        if dept == None:
            dept = random.choice(suitDepts)
        self.dept = dept
        index = suitDepts.index(dept)
        base = index * suitsPerDept
        offset = 0
        if level > 1:
            for i in range(1, level):
                offset = offset + suitsPerLevel[i - 1]

        bottom = base + offset
        top = bottom + suitsPerLevel[level - 1]
        self.name = suitHeadTypes[random.choice(list(range(bottom, top)))]
        self.body = getSuitBodyType(self.name)
        return

    def newGoon(self, name = None):
        if type == None:
            self.__defaultGoon()
        else:
            self.type = 'g'
            if name in goonTypes:
                self.name = name
            else:
                notify.error('unknown goon type: ', name)
        return

    def getType(self):
        if self.type == 's':
            type = 'suit'
        elif self.type == 'b':
            type = 'boss'
        else:
            notify.error('Invalid DNA type: ', self.type)
        return type
