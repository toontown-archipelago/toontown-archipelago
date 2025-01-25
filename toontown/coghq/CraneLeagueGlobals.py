# A file to put all crane league settings in one place for easy adjustment
from toontown.toonbase import ToontownGlobals

SPECIAL_MODIFIER_CHANCE = 3  # % chance you want to roll a special modifier for a cfo  *** server side only

# Ruleset

NORMAL_CRANE_POSHPR = [
    (97.4, -337.6, 0, - 45, 0, 0),
    (97.4, -292.4, 0, - 135, 0, 0),
    (142.6, -292.4, 0, 135, 0, 0),
    (142.6, -337.6, 0, 45, 0, 0)
]

SIDE_CRANE_POSHPR = [
    (81, -315, 0, -90, 0, 0),
    (160, -315, 0, 90, 0, 0)
]
HEAVY_CRANE_POSHPR = [
    (120, -280, 0, 180, 0, 0),
    (120, -350, 0, 0, 0, 0)
]

SAFE_POSHPR = [
    (120, -315, 30, 0, 0, 0),
    (77.1, -302.7, 0, -90, 0, 0),  # 1R
    (165.7, -326.4, 0, 90, 0, 0),  # 2R
    (134.2, -274.7, 0, 180, 0, 0),  # 4R
    (107.8, -359.1, 0, 0, 0, 0),  # 3R
    (107.0, -274.7, 0, 180, 0, 0),  # 1L
    (133.9, -359.1, 0, 0, 0, 0),  # 2L
    (165.5, -302.4, 0, 90, 0, 0),  # 4L
    (77.2, -329.3, 0, -90, 0, 0),  # 3L
    (102.957,  -301.296,  0, 45, 0, 0),  # C1
    (138.467,  -301.042,  0, -45, 0, 0),  # C2
    (138.457,  -330.047,  0, -135, 0, 0),  # C3
    (102.675,  -328.630,  0, 135, 0, 0),  # C4
]

SAFE_POSHPR_NEW = [
    (120, -315, 30, 0, 0, 0),
    (77.1, -302.7, 0, 180, 0, 0),  # 1R
    (165.7, -326.4, 0, 180, 0, 0),  # 2R
    (134.2, -274.7, 0, 180, 0, 0),  # 4R
    (107.8, -359.1, 0, 180, 0, 0),  # 3R
    (107.0, -274.7, 0, 180, 0, 0),  # 1L
    (133.9, -359.1, 0, 180, 0, 0),  # 2L
    (165.5, -302.4, 0, 180, 0, 0),  # 4L
    (77.2, -329.3, 0, 180, 0, 0),  # 3L
]

SAFE_H = [
    0,
    -270,  # 1R
    270,  # 2R
    0,  # 4R
    -180,  # 3R
    0,  # 1L
    -180,  # 2L
    270,  # 4L
    -270,  # 3L
]

SAFE_R = [
    90,
    180,  # 1R
    0,  # 2R
    -90,  # 4R
    90,  # 3R
    -90,  # 1L
    90,  # 2L
    0,  # 4L
    180,  # 3L
]

TOON_SPAWN_POSITIONS = [
    (105, -285, 0, 208, 0, 0),
    (136, -342, 0, 398, 0, 0),
    (105, -342, 0, 333, 0, 0),
    (135, -292, 0, 146, 0, 0),
    (93, -303, 0, 242, 0, 0),
    (144, -327, 0, 64, 0, 0),
    (145, -302, 0, 117, 0, 0),
    (93, -327, 0, -65, 0, 0)
]

ALL_CRANE_POSHPR = NORMAL_CRANE_POSHPR + SIDE_CRANE_POSHPR + HEAVY_CRANE_POSHPR

LOW_LAFF_BONUS_TEXT = "UBER BONUS"  # Text to display alongside a low laff bonus

# Text to display in popup text for misc point gains
GOON_STOMP_TEXT = 'GOON!'
STUN_TEXT = "STUN!"
IMPACT_TEXT = "PERFECT!"
DESAFE_TEXT = "DESAFE!"
GOON_KILLED_BY_SAFE_TEXT = "DESTRUCTION!"
KILLING_BLOW_TEXT = 'KILLING BLOW!'

PENALTY_SAFEHEAD_TEXT = "SAFED!"
PENALTY_TREASURE_TEXT = 'TREASURE!'
PENALTY_GO_SAD_TEXT = "DIED!"
PENALTY_SANDBAG_TEXT = 'SLOPPY!'
PENALTY_UNSTUN_TEXT = 'UN-STUN!'


# Ruleset
# Instance attached to cfo boss instances, so we can easily modify stuff dynamically
class CFORuleset:

    def __init__(self):
        # Enable for debugging
        self.GENERAL_DEBUG = False
        self.GOON_STATES_DEBUG = False
        self.CRANE_STATES_DEBUG = False
        self.SAFE_STATES_DEBUG = False

        self.TIMER_MODE = False  # When true, the cfo is timed and ends when time is up, when false, acts as a stopwatch
        self.TIMER_MODE_TIME_LIMIT = 15 * 60  # How many seconds do we give the CFO crane round if TIMER_MODE is active?

        self.CFO_MAX_HP = 400  # How much HP should the CFO have?
        self.HP_PER_EXTRA = 150  # How much HP should the CFO increase by per toon?
        self.CFO_STUN_THRESHOLD = 15  # How much damage should a goon do to stun?
        self.SIDECRANE_IMPACT_STUN_THRESHOLD = 0.8  # How much impact should a side crane hit need to register a stun

        self.WANT_BACKWALL = False
        self.WANT_SIDECRANES = True
        self.WANT_HEAVY_CRANES = False

        self.HEAVY_CRANE_DAMAGE_MULTIPLIER = 1.5

        self.MIN_GOON_IMPACT = 0.1  # How much impact should a goon hit need to register?
        self.MIN_SAFE_IMPACT = 0.0  # How much impact should a safe hit need to register?
        self.MIN_DEHELMET_IMPACT = 0.25  # How much impact should a safe hit need to desafe the CFO?

        self.GOON_CFO_DAMAGE_MULTIPLIER = 1.0
        self.SAFE_CFO_DAMAGE_MULTIPLIER = 1.0

        self.WANT_CFO_JUMP_ATTACK = False
        self.CFO_JUMP_ATTACK_CHANCE = 20  # Percent chance for the cfo to perform a AOE jump attack
        self.RANDOM_GEAR_THROW_ORDER = False  # Should the order in which CFO throw gears at toons be random?
        self.CFO_FLINCHES_ON_HIT = True  # Should the CFO flinch when being hit?
        self.DISABLE_SAFE_HELMETS = False  # Should the CFO be allowed to helmet?
        self.SAFES_TO_SPAWN = len(SAFE_POSHPR)  # How many safes should we spawn?

        # A dict that maps attack codes to base damage values from the CFO
        self.CFO_ATTACKS_BASE_DAMAGE = {
            ToontownGlobals.BossCogElectricFence: 1,  # The actual bump
            ToontownGlobals.BossCogSwatLeft: 5,  # Swats from bumping
            ToontownGlobals.BossCogSwatRight: 5,
            ToontownGlobals.BossCogSlowDirectedAttack: 10,  # Gear throw
            ToontownGlobals.BossCogAreaAttack: 20,  # Jump
        }

        # How much should attacks be multiplied by by the time we are towards the end?
        self.CFO_ATTACKS_MULTIPLIER = 3
        # should multiplier gradually scale or go up by integers?  False means 1x then 2x then 3x, True gradually increases
        self.CFO_ATTACKS_MULTIPLIER_INTERPOLATE = True

        # GOON/TREASURE SETTINGS
        self.MIN_GOON_DAMAGE = 3  # What is the lowest amount of damage a goon should do? (beginning of CFO)
        self.MAX_GOON_DAMAGE = 20  # What is the highest amount of damage a goon should do? (end of CFO)
        self.GOON_SPEED_MULTIPLIER = 1.0  # How fast should goons move?

        # How many goons should we allow to spawn? This will scale up towards the end of the fight to the 2nd var
        self.MAX_GOON_AMOUNT_START = 6
        self.MAX_GOON_AMOUNT_END = 12

        # Should goons get stunned instead of die on hit?
        self.SAFES_STUN_GOONS = False
        # Should stomps kill goons instead of stun?
        self.GOONS_DIE_ON_STOMP = False
        # Should ALL cranes wakeup goons when grabbed
        self.GOONS_ALWAYS_WAKE_WHEN_GRABBED = False

        # How many treasures should we allow to spawn?
        self.MAX_TREASURE_AMOUNT = 30

        # Should we have a drop chance?
        self.GOON_TREASURE_DROP_CHANCE = 1.0

        self.REALLY_WEAK_TREASURE_HEAL_AMOUNT = 5  # How much should the treasures from very small goons heal?
        self.WEAK_TREASURE_HEAL_AMOUNT = 7  # How much should the treasures from small goons heal?
        self.AVERAGE_TREASURE_HEAL_AMOUNT = 10  # How much should the treasures from med goons heal?
        self.STRONG_TREASURE_HEAL_AMOUNT = 12  # How much should the treasures from the big goons heal?

        # Applies treasure heal amounts
        self.update_lists()

        # TOON SETTINGS
        self.FORCE_MAX_LAFF = False  # Should we force a laff limit for this crane round?
        self.FORCE_MAX_LAFF_AMOUNT = 100  # The laff that we are going to force all toons participating to have
        self.HEAL_TOONS_ON_START = False  # Should we set all toons to full laff when starting the round?
        self.RANDOM_SPAWN_POSITIONS = False  # Should spawn positions be completely random?

        self.WANT_LOW_LAFF_BONUS = True  # Should we award toons with low laff bonus points?
        self.LOW_LAFF_BONUS = .1  # How much will the bonus be worth? i.e. .1 = 10% bonus for ALL points
        self.LOW_LAFF_BONUS_THRESHOLD = 25  # How much laff or less should a toon have to be considered for a low laff bonus?
        self.LOW_LAFF_BONUS_INCLUDE_PENALTIES = False  # Should penalties also be increased when low on laff?

        # note: When REVIVE_TOONS_UPON_DEATH is True, the only fail condition is if we run out of time
        self.RESTART_CRANE_ROUND_ON_FAIL = False  # Should we restart the crane round if all toons die?
        self.REVIVE_TOONS_UPON_DEATH = False  # Should we revive a toon that dies after a certain amount of time? (essentially a stun)
        self.REVIVE_TOONS_TIME = 10  # Time in seconds to revive a toon after death
        self.REVIVE_TOONS_LAFF_PERCENTAGE = 0.50  # How much laff should we give back to the toon when revived?

        # A for fun mechanic that makes toons have permanent damage buffs based on how much damage they do
        self.WANT_MOMENTUM_MECHANIC = False

        # POINTS SETTINGS
        self.POINTS_GOON_STOMP = 1  # Points per goon stomp
        self.POINTS_STUN = 10  # Points per stun
        self.POINTS_SIDESTUN = 25  # Points per stun on sidecrane
        self.POINTS_IMPACT = 3  # Points given when a max impact hit is achieved
        self.POINTS_DESAFE = 10  # Points for taking a safe helmet off
        self.POINTS_GOON_KILLED_BY_SAFE = 2  # Points for killing a goon with a safe
        self.POINTS_KILLING_BLOW = 0  # Points for dealing the killing blow to the CFO

        self.POINTS_PENALTY_SAFEHEAD = -25  # Deduction for putting a safe on the CFOs head
        self.POINTS_PENALTY_GO_SAD = -50  # Point deduction for dying (can happen multiple times if revive setting is on)
        self.POINTS_PENALTY_SANDBAG = -5  # Point deduction for hitting a very low impact hit
        self.POINTS_PENALTY_UNSTUN = -25

        self.TREASURE_POINT_PENALTY = False  # Should we deduct points for picking up treasures?
        self.TREASURE_POINT_PENALTY_FLAT_RATE = 1  # How much should we deduct? set to 0 or less to make it 1 to 1 with laff gained

        # COMBO SETTINGS
        self.COMBO_DURATION = 2.0  # How long should combos last?
        self.TREASURE_GRAB_RESETS_COMBO = False  # Should picking up a treasure reset a toon's combo?

        self.MODIFIER_TIER_RANGE = (1, 3)  # todo Perhaps refactor this into the modifier class

    def get_max_allowed_hp(self):
        return self.CFO_MAX_HP * 2

    # Called to update various list values constructed from instance attributes
    def update_lists(self):
        # Doesn't need to be modified, just used for math
        self.GOON_HEALS = [
            self.REALLY_WEAK_TREASURE_HEAL_AMOUNT,
            self.WEAK_TREASURE_HEAL_AMOUNT,
            self.AVERAGE_TREASURE_HEAL_AMOUNT,
            self.STRONG_TREASURE_HEAL_AMOUNT,
        ]
        self.TREASURE_STYLES = [
            [ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock],
            [ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens],
            [ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh],
            [ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland],
        ]

    # Call to make sure certain attributes are within certain bounds, for example dont make required impacts > 100%
    def validate(self):
        # Ensure impact required isn't greater than 95%
        self.MIN_SAFE_IMPACT = min(self.MIN_SAFE_IMPACT, .95)
        self.MIN_DEHELMET_IMPACT = min(self.MIN_DEHELMET_IMPACT, .95)
        self.MIN_GOON_IMPACT = min(self.MIN_GOON_IMPACT, .95)
        self.SIDECRANE_IMPACT_STUN_THRESHOLD = min(self.SIDECRANE_IMPACT_STUN_THRESHOLD, .95)

    # Sends an astron friendly array over, ONLY STUFF THE CLIENT NEEDS TO KNOW GOES HERE
    # ANY TIME YOU MAKE A NEW ATTRIBUTE IN THE INIT ABOVE, MAKE SURE TO ADD
    # THE ATTRIBUTE INTO THIS LIST BELOW, AND A PARAMETER FOR IT IN THE DC FILE IN THE CFORuleset STRUCT
    def asStruct(self):
        return [
            self.TIMER_MODE,
            self.TIMER_MODE_TIME_LIMIT,
            self.CFO_MAX_HP,
            self.MIN_GOON_IMPACT,
            self.MIN_SAFE_IMPACT,
            self.MIN_DEHELMET_IMPACT,
            self.WANT_LOW_LAFF_BONUS,
            self.LOW_LAFF_BONUS,
            self.LOW_LAFF_BONUS_THRESHOLD,
            self.LOW_LAFF_BONUS_INCLUDE_PENALTIES,
            self.RESTART_CRANE_ROUND_ON_FAIL,
            self.REVIVE_TOONS_UPON_DEATH,
            self.REVIVE_TOONS_TIME,
            self.POINTS_GOON_STOMP,
            self.POINTS_STUN,
            self.POINTS_SIDESTUN,
            self.POINTS_IMPACT,
            self.POINTS_DESAFE,
            self.POINTS_GOON_KILLED_BY_SAFE,
            self.POINTS_PENALTY_SAFEHEAD,
            self.POINTS_PENALTY_GO_SAD,
            self.POINTS_PENALTY_SANDBAG,
            self.POINTS_PENALTY_UNSTUN,
            self.COMBO_DURATION,
            self.WANT_BACKWALL,
            self.CFO_FLINCHES_ON_HIT,
            self.SAFES_STUN_GOONS,
            self.GOONS_ALWAYS_WAKE_WHEN_GRABBED,
        ]

    @classmethod
    def fromStruct(cls, attrs):
        rulesetInstance = cls()
        rulesetInstance.TIMER_MODE = attrs[0]
        rulesetInstance.TIMER_MODE_TIME_LIMIT = attrs[1]
        rulesetInstance.CFO_MAX_HP = attrs[2]
        rulesetInstance.MIN_GOON_IMPACT = attrs[3]
        rulesetInstance.MIN_SAFE_IMPACT = attrs[4]
        rulesetInstance.MIN_DEHELMET_IMPACT = attrs[5]
        rulesetInstance.WANT_LOW_LAFF_BONUS = attrs[6]
        rulesetInstance.LOW_LAFF_BONUS = attrs[7]
        rulesetInstance.LOW_LAFF_BONUS_THRESHOLD = attrs[8]
        rulesetInstance.LOW_LAFF_BONUS_INCLUDE_PENALTIES = attrs[9]
        rulesetInstance.RESTART_CRANE_ROUND_ON_FAIL = attrs[10]
        rulesetInstance.REVIVE_TOONS_UPON_DEATH = attrs[11]
        rulesetInstance.REVIVE_TOONS_TIME = attrs[12]
        rulesetInstance.POINTS_GOON_STOMP = attrs[13]
        rulesetInstance.POINTS_STUN = attrs[14]
        rulesetInstance.POINTS_SIDESTUN = attrs[15]
        rulesetInstance.POINTS_IMPACT = attrs[16]
        rulesetInstance.POINTS_DESAFE = attrs[17]
        rulesetInstance.POINTS_GOON_KILLED_BY_SAFE = attrs[18]
        rulesetInstance.POINTS_PENALTY_SAFEHEAD = attrs[19]
        rulesetInstance.POINTS_PENALTY_GO_SAD = attrs[20]
        rulesetInstance.POINTS_PENALTY_SANDBAG = attrs[21]
        rulesetInstance.POINTS_PENALTY_UNSTUN = attrs[22]
        rulesetInstance.COMBO_DURATION = attrs[23]
        rulesetInstance.WANT_BACKWALL = attrs[24]
        rulesetInstance.CFO_FLINCHES_ON_HIT = attrs[25]
        rulesetInstance.SAFES_STUN_GOONS = attrs[26]
        rulesetInstance.GOONS_ALWAYS_WAKE_WHEN_GRABBED = attrs[27]
        return rulesetInstance

    def __str__(self):
        return repr(self.__dict__)


# Some other default rulesets to choose from
class SemiFinalsCFORuleset(CFORuleset):

    def __init__(self):
        CFORuleset.__init__(self)
        self.TIMER_MODE_TIME_LIMIT = int(60 * 12.5)
        self.CFO_MAX_HP = 2250


class FinalsCFORuleset(CFORuleset):

    def __init__(self):
        CFORuleset.__init__(self)
        self.TIMER_MODE_TIME_LIMIT = 60 * 15
        self.CFO_MAX_HP = 3000


# This is where we define modifiers, all modifiers alter a ruleset instance in some way to tweak cfo behavior
# dynamically, first the base class that any modifiers should extend from
class CFORulesetModifierBase(object):
    # This should also be overridden, used so that the client knows which class to use when instantiating modifiers
    MODIFIER_ENUM = -1
    # This should also be overridden, use to define what type of modifier this is
    UNDEFINED = -1
    SPECIAL = 0
    HELPFUL = 1
    HURTFUL = 2
    MODIFIER_TYPE = UNDEFINED
    # Special, Helpful, Hurtful

    # Maps the above modifier enums to the classes that extend this one
    MODIFIER_SUBCLASSES = {}

    # Some colors to use for titles and percentages etc
    DARK_RED = (230.0 / 255.0, 20 / 255.0, 20 / 255.0, 1)
    RED = (255.0 / 255.0, 85.0 / 255.0, 85.0 / 255.0, 1)

    DARK_GREEN = (0, 180 / 255.0, 0, 1)
    GREEN = (85.0 / 255.0, 255.0 / 255.0, 85.0 / 255.0, 1)

    DARK_PURPLE = (170.0 / 255.0, 0, 170.0 / 255.0, 1)
    PURPLE = (255.0 / 255.0, 85.0 / 255.0, 255.0 / 255.0, 1)

    DARK_CYAN = (0, 0, 170.0 / 170.0, 1)
    CYAN = (85.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, 1)

    # The color that should be used for the title of this modifier
    TITLE_COLOR = DARK_GREEN
    # The color of the alternate color in the description, eg cfo has '+50%' more hp
    DESCRIPTION_COLOR = GREEN

    # Tier represents modifiers that have multiple tiers to them, like tier 3 modifiers giving cfo +100% hp instead of
    # +50% in tier 1
    def __init__(self, tier=1):
        self.tier = tier

    # Copied from google bc cba
    @staticmethod
    def numToRoman(n):
        NUM = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
        SYM = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]
        i = 12

        romanString = ''

        while n:
            div = n // NUM[i]
            n %= NUM[i]

            while div:
                romanString += SYM[i]
                div -= 1
            i -= 1
        return romanString

    # lazy method to translate ints to percentages since i think percents are cleaner to display
    @staticmethod
    def additivePercent(n):
        return 1.0 + n / 100.0

    # lazy method to translate ints to percentages since i think percents are cleaner to display
    @staticmethod
    def subtractivePercent(n):
        return 1.0 - n / 100.0

    # The name of this modifier to display to the client
    def getName(self):
        raise NotImplementedError('Please override the getName method from the parent class!')

    # The description of this modifier to display to the client
    def getDescription(self):
        raise NotImplementedError('Please override the getName method from the parent class!')

    # Returns an integer to change the total 'heat' of the cfo based on this modifier, heat is an arbitrary measurement
    # of difficulty of a cfo round based on modifiers applied
    def getHeat(self):
        raise NotImplementedError("Please override the getHeat method from the parent class!")

    # This method is called to apply this modifiers effect to a CFORuleset instance on the AI
    def apply(self, cfoRuleset):
        raise NotImplementedError('Please override the apply method from the parent class!')

    # Same as ruleset, used to send to the client in an astron friendly way
    def asStruct(self):
        return [
            self.MODIFIER_ENUM,
            self.tier
        ]

    # Used to construct modifier instances when received from astron using the asStruct method
    @classmethod
    def fromStruct(cls, attrs):
        # Extract the info from the list
        modifierEnum, tier = attrs
        # Check if the enum isn't garbage
        if modifierEnum not in cls.MODIFIER_SUBCLASSES:
            raise Exception('Invalid modifier %s given from astron' % modifierEnum)

        # Extract the registered constructor and instantiate a modifier instance
        cls_constructor = cls.MODIFIER_SUBCLASSES[modifierEnum]
        modifier = cls_constructor(tier)
        return modifier


# An example implementation of a modifier, can be copied and modified
# class ModifierExample(CFORulesetModifierBase):
#
#     # The enum used by astron to know the type
#     MODIFIER_ENUM = 69
#
#     TITLE_COLOR = CFORulesetModifierBase.DARK_PURPLE
#     DESCRIPTION_COLOR = CFORulesetModifierBase.PURPLE
#
#     def getName(self):
#         return 'Funny Number'
#
#     def getDescription(self):
#         return "This modifier sets the CFO's hp to %(color_start)s69%(color_end)s"
#
#     def getHeat(self):
#         return 69
#
#     def apply(self, cfoRuleset):
#         cfoRuleset.CFO_MAX_HP = 69  # Give the cfo 69 hp


# Now here is where we can actually define our modifiers
class ModifierComboExtender(CFORulesetModifierBase):
    MODIFIER_ENUM = 0
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    # The combo percentage increase per tier
    COMBO_DURATION_PER_TIER = [0, 50, 100, 200]

    def _duration(self):
        if self.tier <= len(self.COMBO_DURATION_PER_TIER):
            return self.COMBO_DURATION_PER_TIER[self.tier]

        # tier 4 = 300, 5=400 ...
        return (self.tier - 1) * 100

    def getName(self):
        return 'Chains of Finesse ' + self.numToRoman(self.tier)

    def getDescription(self):
        perc = self._duration()
        return 'Increases combo length by %(color_start)s+' + str(perc) + '%%%(color_end)s'

    def getHeat(self):
        return -10 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.COMBO_DURATION *= self.additivePercent(self._duration())


class ModifierComboShortener(CFORulesetModifierBase):
    MODIFIER_ENUM = 1
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    # The combo percentage increase per tier
    COMBO_DURATION_PER_TIER = [0, 25, 50, 75]

    def _duration(self):
        if self.tier <= len(self.COMBO_DURATION_PER_TIER):
            return self.COMBO_DURATION_PER_TIER[self.tier]

        # tier 4 = 80, 5=85 ...
        perc = 75 + ((self.tier - 3) * 5)
        # Don't let this go higher than 99
        return min(perc, 99)

    def getName(self):
        return 'Chain Locker ' + self.numToRoman(self.tier)

    def getDescription(self):
        perc = self._duration()
        return 'Decreases combo length by %(color_start)s-' + str(perc) + '%%%(color_end)s'

    def getHeat(self):
        return 10 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.COMBO_DURATION *= self.subtractivePercent(self._duration())


# Now here is where we can actually define our modifiers
class ModifierCFOHPIncreaser(CFORulesetModifierBase):
    MODIFIER_ENUM = 2
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    # The combo percentage increase per tier
    CFO_INCREASE_PER_TIER = [0, 25, 50, 100]

    def _perc_increase(self):
        if self.tier <= len(self.CFO_INCREASE_PER_TIER):
            return self.CFO_INCREASE_PER_TIER[self.tier]

        # tier 4 = 200, 5=300 ...
        return (self.tier - 2) * 100

    def getName(self):
        return 'Financial Aid ' + self.numToRoman(self.tier)

    def getDescription(self):
        perc = self._perc_increase()
        return 'The CFO has %(color_start)s+' + str(perc) + '%%%(color_end)s more HP'

    def getHeat(self):
        return 125 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_MAX_HP *= self.additivePercent(self._perc_increase())


# Now here is where we can actually define our modifiers
class ModifierCFOHPDecreaser(CFORulesetModifierBase):
    MODIFIER_ENUM = 3
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    # The combo percentage increase per tier
    CFO_DECREASE_PER_TIER = [0, 20, 35, 50]

    def _perc_decrease(self):
        if self.tier <= len(self.CFO_DECREASE_PER_TIER):
            return self.CFO_DECREASE_PER_TIER[self.tier]

        # tier 4 = 65, 5=75 6=80...
        # todo: grow some brain cells and find formula that does this
        if self.tier == 4:
            return 65
        if self.tier == 5:
            return 75

        # Don't let it go higher than 99%
        return min(99, self.tier * 5 + 50)

    def getName(self):
        return 'Financial Drain ' + self.numToRoman(self.tier)

    def getDescription(self):
        perc = self._perc_decrease()
        return 'The CFO has %(color_start)s-' + str(perc) + '%%%(color_end)s less HP'

    def getHeat(self):
        return -30 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_MAX_HP *= self.subtractivePercent(self._perc_decrease())


# (-) Strong/Tough/Reinforced Bindings
# --------------------------------
# - required impact to desafe increased by 20/40/75%
class ModifierDesafeImpactIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 4
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    TIER_NAMES = ['', 'Strong', 'Tough', 'Reinforced']
    CFO_DECREASE_PER_TIER = [0, 25, 50, 75]

    def _perc_increase(self):
        if self.tier <= len(self.CFO_DECREASE_PER_TIER):
            return self.CFO_DECREASE_PER_TIER[self.tier]

        # tier 4 = 80, 5=85 6=90...
        return 5 * self.tier + 60

    def getName(self):

        if self.tier <= len(self.TIER_NAMES):
            return self.TIER_NAMES[self.tier] + ' Bindings'

        return 'Reinforced Bindings ' + self.numToRoman(self.tier)

    def getDescription(self):
        perc = self._perc_increase()
        return "Increases the impact required to remove the CFO's helmet by %(color_start)s+" + str(
            perc) + "%%%(color_end)s"

    def getHeat(self):
        return 50 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.MIN_DEHELMET_IMPACT *= self.additivePercent(self._perc_increase())


# (+) Copper Plating
# --------------------------------
# - required general impact decreased by 25%
class ModifierGeneralImpactDecreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 5
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    PERC_REDUCTION = 25

    def getName(self):
        return 'Copper Plating'

    def getDescription(self):
        return "Decreases general impact required by %(color_start)s-" + str(
            self.PERC_REDUCTION) + "%%%(color_end)s for goons and safes"

    def getHeat(self):
        return -30

    def apply(self, cfoRuleset):
        cfoRuleset.MIN_DEHELMET_IMPACT *= self.subtractivePercent(
            self.PERC_REDUCTION)  # reduce min safe impact for helms
        cfoRuleset.SIDECRANE_IMPACT_STUN_THRESHOLD *= self.subtractivePercent(
            self.PERC_REDUCTION)  # Reduce sidestun impact
        cfoRuleset.MIN_GOON_IMPACT *= self.subtractivePercent(self.PERC_REDUCTION)  # Reduce goon impact
        cfoRuleset.MIN_SAFE_IMPACT *= self.subtractivePercent(self.PERC_REDUCTION)  # Reduce safe impact


# (-) Refined Plating
# --------------------------------
# - required general impact increased by 25%
class ModifierGeneralImpactIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 6
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    PERC_REDUCTION = 25

    def getName(self):
        return 'Refined Plating'

    def getDescription(self):
        return "Increases general impact required by %(color_start)s+" + str(
            self.PERC_REDUCTION) + "%%%(color_end)s for goons and safes"

    def getHeat(self):
        return 50

    def apply(self, cfoRuleset):
        cfoRuleset.MIN_DEHELMET_IMPACT *= self.additivePercent(self.PERC_REDUCTION)  # reduce min safe impact for helms
        cfoRuleset.SIDECRANE_IMPACT_STUN_THRESHOLD *= self.additivePercent(
            self.PERC_REDUCTION)  # Reduce sidestun impact
        cfoRuleset.MIN_GOON_IMPACT *= self.additivePercent(self.PERC_REDUCTION)  # Reduce goon impact
        cfoRuleset.MIN_SAFE_IMPACT *= self.additivePercent(self.PERC_REDUCTION)  # Reduce safe impact


# (-) Devolution (Omega/Beta/Alpha)
# --------------------------------
# - heavy cranes disabled (Omega)
# - sidecranes disabled (Beta)
# - classic collisions and back wall (Alpha)
class ModifierDevolution(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 7
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    TIER_NAMES = ['', 'Omega', 'Beta', 'Alpha']
    TIER_HEATS = [0, 25, 200, 225]

    # Returns the part of the string that's colored, basically what is disabled
    def _getDynamicString(self):
        if self.tier >= 2:
            return "Heavy cranes and Sidecranes"
        elif self.tier >= 1:
            return "Heavy cranes"

        else:
            return "no cranes?"

    def getName(self):
        tier = min(self.tier, len(self.TIER_NAMES) - 1)
        return 'Devolution ' + self.TIER_NAMES[tier]

    def getDescription(self):

        ret = 'A trip down memory lane. %(color_start)s' + self._getDynamicString() + '%(color_end)s are disabled'
        if self.tier >= 3:
            ret += '. %(color_start)sBack walls%(color_end)s are enabled'

        return ret

    def getHeat(self):
        if self.tier <= len(self.TIER_HEATS):
            return self.TIER_HEATS[self.tier]

        return self.TIER_HEATS[-1]

    def apply(self, cfoRuleset):
        cfoRuleset.WANT_HEAVY_CRANES = False

        if self.tier >= 2:
            cfoRuleset.WANT_SIDECRANES = False

        if self.tier >= 3:
            cfoRuleset.WANT_BACKWALL = True


# (-) Armor of Alloys
# --------------------------------
# - cfo does not flinch when getting hit
class ModifierCFONoFlinch(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 8
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def getName(self):
        return 'Armor of Alloys'

    def getDescription(self):
        return 'The CFO %(color_start)sno longer flinches%(color_end)s upon being damaged'

    def getHeat(self):
        return 150

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_FLINCHES_ON_HIT = False


# (+) Hard(er/est) Hats
# --------------------------------
# + goons inflict 10/20/30% more damage to the cfo
class ModifierGoonDamageInflictIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 9
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN
    TIER_SUFFIXES = ['', '', 'er', 'est']
    TIER_PERCENT_AMOUNTS = [0, 20, 50, 75]

    def _perc_increase(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return self.TIER_PERCENT_AMOUNTS[self.tier]

        return self.tier * 25

    def getName(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return 'Hard' + self.TIER_SUFFIXES[self.tier] + ' Hats'

        return 'Harder Hats ' + self.numToRoman(self.tier)

    def getDescription(self):
        _start = ''
        _end = ''

        return 'Increases damages inflicted to the CFO from goons by %(color_start)s+' + str(
            self._perc_increase()) + '%%%(color_end)s'

    def getHeat(self):
        return -20 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.GOON_CFO_DAMAGE_MULTIPLIER *= self.additivePercent(self._perc_increase())


# (+) Safer Containers
# --------------------------------
# + safes inflict 10/20/30% more damage to the cfo
class ModifierSafeDamageInflictIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 10
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN
    TIER_SUFFIXES = ['e', 'e', 'er', 'est']
    TIER_PERCENT_AMOUNTS = [0, 25, 50, 100]

    def _perc_increase(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return self.TIER_PERCENT_AMOUNTS[self.tier]

        return self.tier * 50 - 50

    def getName(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return 'Saf' + self.TIER_SUFFIXES[self.tier] + ' Containers'

        return "Safer Containers " + self.numToRoman(self.tier)

    def getDescription(self):
        return 'Increases damages inflicted to the CFO from safes by %(color_start)s+' + str(
            self._perc_increase()) + '%%%(color_end)s'

    def getHeat(self):
        return -20 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.SAFE_CFO_DAMAGE_MULTIPLIER *= self.additivePercent(self._perc_increase())


# (-) Fast(er/est) Security
# --------------------------------
# - goons move 25/50/75% faster
class ModifierGoonSpeedIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 11
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN
    TIER_SUFFIXES = ['', '', 'er', 'est']
    TIER_PERCENT_AMOUNTS = [0, 10, 25, 50]

    def _perc_increase(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return self.TIER_PERCENT_AMOUNTS[self.tier]

        return self.tier * 25 - 25

    def getName(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return 'Fast' + self.TIER_SUFFIXES[self.tier] + ' Security'

        return "Faster Security " + self.numToRoman(self.tier)

    def getDescription(self):
        return 'Goons move %(color_start)s+' + str(self._perc_increase()) + '%%%(color_end)s faster'

    def getHeat(self):
        return 50 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.GOON_SPEED_MULTIPLIER *= self.additivePercent(self._perc_increase())


# (-) Overwhelming Security (I-III)
# --------------------------------
# - goon cap raised by 20/50/75%
class ModifierGoonCapIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 12
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN
    TIER_PERCENT_AMOUNTS = [0, 25, 50, 75]

    def _perc_increase(self):
        if self.tier <= len(self.TIER_PERCENT_AMOUNTS):
            return self.TIER_PERCENT_AMOUNTS[self.tier]

        return self.tier * 25

    def getName(self):
        n = "Overwhelming Security"
        if self.tier > 1:
            n += ' ' + self.numToRoman(self.tier)
        return n

    def getDescription(self):
        return 'The CFO spawns %(color_start)s+' + str(self._perc_increase()) + '%%%(color_end)s more goons'

    def getHeat(self):
        return 40 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.MAX_GOON_AMOUNT_START *= self.additivePercent(self._perc_increase())
        cfoRuleset.MAX_GOON_AMOUNT_END *= self.additivePercent(self._perc_increase())


# (-) Undying Security
# --------------------------------
# - safes can only stun goons
class ModifierSafesStunGoons(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 13
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def getName(self):
        return 'Undying Security'

    def getDescription(self):
        return 'Safes now %(color_start)sstun goons instead of destroy%(color_end)s them on impact'

    def getHeat(self):
        return 50

    def apply(self, cfoRuleset):
        cfoRuleset.SAFES_STUN_GOONS = True


# (-) Slippery Security
# --------------------------------
# - all cranes wake goons up when grabbed
class ModifierGoonsGrabbedWakeup(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 14
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def getName(self):
        return 'Slippery Security'

    def getDescription(self):
        return 'Goons %(color_start)salways wakeup%(color_end)s when grabbed by all cranes'

    def getHeat(self):
        return 90

    def apply(self, cfoRuleset):
        cfoRuleset.GOONS_ALWAYS_WAKE_WHEN_GRABBED = True


# (+) Sweet Treat
# --------------------------------
# + treasures heal an additional 50%
class ModifierTreasureHealIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 15
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN
    INCREASE_PERC = 50

    def getName(self):
        return 'Sweet Treat'

    def getDescription(self):
        return 'Treasures heal %(color_start)s+' + str(self.INCREASE_PERC) + '%%%(color_end)s when grabbed'

    def getHeat(self):
        return -50

    def apply(self, cfoRuleset):
        cfoRuleset.WEAK_TREASURE_HEAL_AMOUNT *= self.additivePercent(self.INCREASE_PERC)
        cfoRuleset.AVERAGE_TREASURE_HEAL_AMOUNT *= self.additivePercent(self.INCREASE_PERC)
        cfoRuleset.STRONG_TREASURE_HEAL_AMOUNT *= self.additivePercent(self.INCREASE_PERC)
        cfoRuleset.REALLY_WEAK_TREASURE_HEAL_AMOUNT *= self.additivePercent(self.INCREASE_PERC)


# (-) Tastebud Dullers (I-III)
# --------------------------------
# - treasures heal 25/50/80% less
class ModifierTreasureHealDecreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 16
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED
    TIER_DECREASE_PERC = [0, 20, 50, 75]

    def _perc_decrease(self):
        if self.tier <= len(self.TIER_DECREASE_PERC):
            return self.TIER_DECREASE_PERC[self.tier]

        return min(99, self.tier * 5 + 55)

    def getName(self):
        n = "Tastebud Dullers"
        if self.tier > 1:
            n += ' ' + self.numToRoman(self.tier)
        return n

    def getDescription(self):
        return 'Treasures heal %(color_start)s-' + str(self._perc_decrease()) + '%%%(color_end)s when grabbed'

    def getHeat(self):
        return 40 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.WEAK_TREASURE_HEAL_AMOUNT *= self.subtractivePercent(self._perc_decrease())
        cfoRuleset.AVERAGE_TREASURE_HEAL_AMOUNT *= self.subtractivePercent(self._perc_decrease())
        cfoRuleset.STRONG_TREASURE_HEAL_AMOUNT *= self.subtractivePercent(self._perc_decrease())
        cfoRuleset.REALLY_WEAK_TREASURE_HEAL_AMOUNT *= self.subtractivePercent(self._perc_decrease())
        cfoRuleset.update_lists()


# (-) Tasteless Goons (I-III)
# --------------------------------
# - treasures have a 50/25/10% chance to drop from a stunned goon
class ModifierTreasureRNG(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 17
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED
    TIER_DROP_PERCENT = [0, 30, 50, 90]

    def _get_decrease(self):
        if self.tier <= len(self.TIER_DROP_PERCENT):
            return self.TIER_DROP_PERCENT[self.tier]

        return min(99, self.tier * 2 + 84)

    def getName(self):
        n = "Tasteless Goons"
        if self.tier > 1:
            n += ' ' + self.numToRoman(self.tier)
        return n

    def getDescription(self):
        return 'Treasures have a %(color_start)s-' + str(
            self._get_decrease()) + '%%%(color_end)s chance to drop from stunned goons'

    def getHeat(self):
        return 30 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.GOON_TREASURE_DROP_CHANCE *= self.subtractivePercent(self._get_decrease())


# (-) Wealth Filter (I-III)
# --------------------------------
# - treasure cap reduced by 25/50/80%
class ModifierTreasureCapDecreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 18
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED
    TIER_DROP_PERCENT = [0, 25, 50, 80]

    def _get_decrease(self):
        if self.tier <= len(self.TIER_DROP_PERCENT):
            return self.TIER_DROP_PERCENT[self.tier]

        return min(99, self.tier * 5 + 55)

    def getName(self):
        n = "Wealth Filter"
        if self.tier > 1:
            n += ' ' + self.numToRoman(self.tier)
        return n

    def getDescription(self):
        return 'Amount of treasures decreased by %(color_start)s-' + str(self._get_decrease()) + '%%%(color_end)s'

    def getHeat(self):
        return 40 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.MAX_TREASURE_AMOUNT *= self.subtractivePercent(self._get_decrease())


# (+) The Melancholic Bonus/Gift/Offering
# --------------------------------
# + UBER bonuses yield 100/200/300% more points
class ModifierUberBonusIncreaser(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 19
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN
    TIER_BONUS_PERC = [0, 100, 200, 300]
    NAME_SUFFIXES = ['', 'Bonus', 'Gift', 'Offering']

    def _perc_increase(self):
        if self.tier <= len(self.TIER_BONUS_PERC):
            return self.TIER_BONUS_PERC[self.tier]

        return self.tier * 100

    def getName(self):
        if self.tier <= len(self.NAME_SUFFIXES):
            return 'The Melancholic ' + self.NAME_SUFFIXES[self.tier]

        return 'Melancholic Fever ' + self.numToRoman(self.tier)

    def getDescription(self):
        return 'Points gained from UBER BONUS increased by %(color_start)s+' + str(
            self._perc_increase()) + '%%%(color_end)s'

    def getHeat(self):
        return -10 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.LOW_LAFF_BONUS *= self.additivePercent(self._perc_increase())


# (-) Jumping for Joy
# --------------------------------
# - The CFO can now use the AOE jump attack
class ModifierCFOJumpAttackEnabler(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 20
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def getName(self):
        return 'Jumping for Joy'

    def getDescription(self):
        return 'The CFO can now perform an %(color_start)sAoE jump attack%(color_end)s!'

    def getHeat(self):
        return 250

    def apply(self, cfoRuleset):
        cfoRuleset.WANT_CFO_JUMP_ATTACK = True


# (-) SPECIAL: Maximum Momentum
# --------------------------------
# - CFO has 1M HP, damage output increases upon every hit
class ModifierMillionMomentum(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 21
    MODIFIER_TYPE = CFORulesetModifierBase.SPECIAL

    TITLE_COLOR = CFORulesetModifierBase.PURPLE
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    def getName(self):
        return 'Maximum Momentum'

    def getDescription(self):
        return 'The CFO has a %(color_start)smillion HP%(color_end)s, but toons gain %(color_start)spermanent damage buffs %(color_end)swhen inflicting damage!'

    def getHeat(self):
        return 1000

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_MAX_HP = 1000000
        cfoRuleset.WANT_MOMENTUM_MECHANIC = True


# (-) Hats Off (come up with better name later)
# --------------------------------
# - CFO cannot safe helmet
class ModifierNoSafeHelmet(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 22
    MODIFIER_TYPE = CFORulesetModifierBase.HELPFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    def getName(self):
        return 'Hats Off'

    def getDescription(self):
        return 'The CFO can %(color_start)sno longer equip safe helmets%(color_end)s!'

    def getHeat(self):
        return -50

    def apply(self, cfoRuleset):
        cfoRuleset.DISABLE_SAFE_HELMETS = True


# (-) Safe Shortage
# --------------------------------
# - Less safes spawn
class ModifierReducedSafes(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 23
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def _getSafesDecrement(self):
        return min(max(0, self.tier * 2), len(SAFE_POSHPR))

    def getName(self):
        return 'Safe Shortage ' + self.numToRoman(self.tier)

    def getDescription(self):
        return 'Amount of safes %(color_start)sdecreased by ' + str(self._getSafesDecrement()) + '%(color_end)s!'

    def getHeat(self):
        return 20 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.SAFES_TO_SPAWN -= self._getSafesDecrement()

        if cfoRuleset.SAFES_TO_SPAWN <= 1:
            cfoRuleset.SAFES_TO_SPAWN = 1
            cfoRuleset.DISABLE_SAFE_HELMETS = True


# (-) Monkey Mode
# --------------------------------
# - Random spawns
class ModifierRandomSpawns(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 24
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def getName(self):
        return 'Monkey Mode'

    def getDescription(self):
        return 'Spawn positions are %(color_start)srandomized%(color_end)s!'

    def getHeat(self):
        return 10

    def apply(self, cfoRuleset):
        cfoRuleset.RANDOM_SPAWN_POSITIONS = True


# (-) Goodbye Goons!
# --------------------------------
# - goons explode when stomped
class ModifierInstakillGoons(CFORulesetModifierBase):
    # The enum used by astron to know the type
    MODIFIER_ENUM = 25
    MODIFIER_TYPE = CFORulesetModifierBase.HURTFUL

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    def getName(self):
        return 'Goodbye Goons!'

    def getDescription(self):
        return 'Goons are %(color_start)sdestroyed%(color_end)s when stomped!'

    def getHeat(self):
        return 50

    def apply(self, cfoRuleset):
        cfoRuleset.GOONS_DIE_ON_STOMP = True


# Any implemented subclasses of CFORulesetModifierBase cannot go past this point
# Loop through all the classes that extend the base modifier class and map an enum to the class for easier construction
for subclass in CFORulesetModifierBase.__subclasses__():
    CFORulesetModifierBase.MODIFIER_SUBCLASSES[subclass.MODIFIER_ENUM] = subclass


# Given a modifier type enum, return a list of classes of this type
def getModifiersOfType(mod_type_enum):
    cls_list = []
    # Loop through all the subclasses
    for mod_subclass in CFORulesetModifierBase.MODIFIER_SUBCLASSES.values():
        # If the type of this class matches the param we passed in
        if mod_subclass.MODIFIER_TYPE == mod_type_enum:
            cls_list.append(mod_subclass)

    return tuple(cls_list)


HURTFUL_MODIFIER_CLASSES = getModifiersOfType(CFORulesetModifierBase.HURTFUL)
HELPFUL_MODIFIER_CLASSES = getModifiersOfType(CFORulesetModifierBase.HELPFUL)
SPECIAL_MODIFIER_CLASSES = getModifiersOfType(CFORulesetModifierBase.SPECIAL)

NON_SPECIAL_MODIFIER_CLASSES = HURTFUL_MODIFIER_CLASSES + HELPFUL_MODIFIER_CLASSES

# Used for when i want to spit out a cheat sheet
# for e, c in CFORulesetModifierBase.MODIFIER_SUBCLASSES.items():
#     i = c()
#     d = i.getDescription() % {'color_start': '', 'color_end': ''}
#     print('(ID:%s) %s\n%s\n' % (e, i.getName(), d))
