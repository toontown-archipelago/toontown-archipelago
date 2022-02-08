# A file to put all crane league settings in one place for easy adjustment
from toontown.toonbase import ToontownGlobals

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
    (77.2, -329.3, 0, -90, 0, 0),
    (77.1, -302.7, 0, -90, 0, 0),
    (165.7, -326.4, 0, 90, 0, 0),
    (165.5, -302.4, 0, 90, 0, 0),
    (107.8, -359.1, 0, 0, 0, 0),
    (133.9, -359.1, 0, 0, 0, 0),
    (107.0, -274.7, 0, 180, 0, 0),
    (134.2, -274.7, 0, 180, 0, 0)
]

ALL_CRANE_POSHPR = NORMAL_CRANE_POSHPR + SIDE_CRANE_POSHPR + HEAVY_CRANE_POSHPR

LOW_LAFF_BONUS_TEXT = "UBER BONUS"  # Text to display alongside a low laff bonus


# Text to display in popup text for misc point gains
GOON_STOMP_TEXT = 'GOON!'
STUN_TEXT = "STUN!"
IMPACT_TEXT = "IMPACT!"
DESAFE_TEXT = "DESAFE!"
GOON_KILLED_BY_SAFE_TEXT = "DESTRUCTION!"

PENALTY_SAFEHEAD_TEXT = "SAFED!"
PENALTY_TREASURE_TEXT = 'TREASURE!'
PENALTY_GO_SAD_TEXT = "DIED!"
PENALTY_SANDBAG_TEXT = 'SLOPPY!'
PENALTY_UNSTUN_TEXT = 'UN-STUN!'


# Ruleset
# Instance attached to cfo boss instances, so we can easily modify stuff dynamically
class CFORuleset:

    def __init__(self):
        self.TIMER_MODE = True  # When true, the cfo is timed and ends when time is up, when false, acts as a stopwatch
        self.TIMER_MODE_TIME_LIMIT = 60*10  # How many seconds do we give the CFO crane round if TIMER_MODE is active?

        self.CFO_MAX_HP = 1500  # How much HP should the CFO have?
        self.CFO_STUN_THRESHOLD = 30  # How much damage should a goon do to stun?
        self.SIDECRANE_IMPACT_STUN_THRESHOLD = 0.8  # How much impact should a side crane hit need to register a stun

        self.WANT_SIDECRANES = True
        self.WANT_HEAVY_CRANES = True

        self.HEAVY_CRANE_DAMAGE_MULTIPLIER = 1.25

        self.MIN_GOON_IMPACT = 0.1  # How much impact should a goon hit need to register?
        self.MIN_SAFE_IMPACT = 0.0  # How much impact should a safe hit need to register?
        self.MIN_DEHELMET_IMPACT = 0.5  # How much impact should a safe hit need to desafe the CFO?

        self.RANDOM_GEAR_THROW_ORDER = False  # Should the order in which CFO throw gears at toons be random?

        # A dict that maps attack codes to base damage values from the CFO
        self.CFO_ATTACKS_BASE_DAMAGE = {
            ToontownGlobals.BossCogElectricFence: 1,  # The actual bump
            ToontownGlobals.BossCogSwatLeft: 10,  # Swats from bumping
            ToontownGlobals.BossCogSwatRight: 10,
            ToontownGlobals.BossCogSlowDirectedAttack: 20,  # Gear throw
        }

        # How much should attacks be multiplied by by the time we are towards the end?
        self.CFO_ATTACKS_MULTIPLIER = 4
        # should multiplier gradually scale or go up by integers?  False means 1x then 2x then 3x, True gradually increases
        self.CFO_ATTACKS_MULTIPLIER_INTERPOLATE = True

        # GOON/TREASURE SETTINGS
        self.MIN_GOON_DAMAGE = 10  # What is the lowest amount of damage a goon should do? (beginning of CFO)
        self.MAX_GOON_DAMAGE = 50  # What is the highest amount of damage a goon should do? (end of CFO)

        # How many goons should we allow to spawn? This will scale up towards the end of the fight to the 2nd var
        self.MAX_GOON_AMOUNT_START = 8
        self.MAX_GOON_AMOUNT_END = 16

        # How many treasures should we allow to spawn?
        self.MAX_TREASURE_AMOUNT = 15

        self.REALLY_WEAK_TREASURE_HEAL_AMOUNT = 2  # How much should the treasures from very small goons heal?
        self.WEAK_TREASURE_HEAL_AMOUNT = 5  # How much should the treasures from small goons heal?
        self.AVERAGE_TREASURE_HEAL_AMOUNT = 8  # How much should the treasures from med goons heal?
        self.STRONG_TREASURE_HEAL_AMOUNT = 10  # How much should the treasures from the big goons heal?

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

        # TOON SETTINGS
        self.FORCE_MAX_LAFF = True  # Should we force a laff limit for this crane round?
        self.FORCE_MAX_LAFF_AMOUNT = 120  # The laff that we are going to force all toons participating to have
        self.HEAL_TOONS_ON_START = True  # Should we set all toons to full laff when starting the round?

        self.WANT_LOW_LAFF_BONUS = True  # Should we award toons with low laff bonus points?
        self.LOW_LAFF_BONUS = .1  # How much will the bonus be worth? i.e. .1 = 10% bonus for ALL points
        self.LOW_LAFF_BONUS_THRESHOLD = 25  # How much laff or less should a toon have to be considered for a low laff bonus?
        self.LOW_LAFF_BONUS_INCLUDE_PENALTIES = True  # Should penalties also be increased when low on laff?

        # note: When REVIVE_TOONS_UPON_DEATH is True, the only fail condition is if we run out of time
        self.RESTART_CRANE_ROUND_ON_FAIL = True  # Should we restart the crane round if all toons die?
        self.REVIVE_TOONS_UPON_DEATH = True  # Should we revive a toon that dies after a certain amount of time? (essentially a stun)
        self.REVIVE_TOONS_TIME = 15  # Time in seconds to revive a toon after death
        self.REVIVE_TOONS_LAFF_PERCENTAGE = 0.50  # How much laff should we give back to the toon when revived?

        # POINTS SETTINGS
        self.POINTS_GOON_STOMP = 1  # Points per goon stomp
        self.POINTS_STUN = 15  # Points per stun
        self.POINTS_IMPACT = 10  # Points given when a max impact hit is achieved
        self.POINTS_DESAFE = 10  # Points for taking a safe helmet off
        self.POINTS_GOON_KILLED_BY_SAFE = 5  # Points for killing a goon with a safe

        self.POINTS_PENALTY_SAFEHEAD = -20  # Deduction for putting a safe on the CFOs head
        self.POINTS_PENALTY_GO_SAD = -50  # Point deduction for dying (can happen multiple times if revive setting is on)
        self.POINTS_PENALTY_SANDBAG = -5  # Point deduction for hitting a very low impact hit
        self.POINTS_PENALTY_UNSTUN = -20

        self.TREASURE_POINT_PENALTY = True  # Should we deduct points for picking up treasures?
        self.TREASURE_POINT_PENALTY_FLAT_RATE = 0  # How much should we deduct? set to 0 or less to make it 1 to 1 with laff gained

        # COMBO SETTINGS
        self.COMBO_DURATION = 2.0  # How long should combos last?
        self.COMBO_DAMAGE_PERCENTAGE = .2  # Percentage to add to our running combo when doing damage (basically 20% bonus per hits when in a combo)
        self.TREASURE_GRAB_RESETS_COMBO = True  # Should picking up a treasure reset a toon's combo?

        self.VERBOSE_IMPACT = False  # Print impact of cfo objects

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
            self.POINTS_IMPACT,
            self.POINTS_DESAFE,
            self.POINTS_GOON_KILLED_BY_SAFE,
            self.POINTS_PENALTY_SAFEHEAD,
            self.POINTS_PENALTY_GO_SAD,
            self.POINTS_PENALTY_SANDBAG,
            self.POINTS_PENALTY_UNSTUN,
            self.COMBO_DURATION,
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
        rulesetInstance.POINTS_IMPACT = attrs[15]
        rulesetInstance.POINTS_DESAFE = attrs[16]
        rulesetInstance.POINTS_GOON_KILLED_BY_SAFE = attrs[17]
        rulesetInstance.POINTS_PENALTY_SAFEHEAD = attrs[18]
        rulesetInstance.POINTS_PENALTY_GO_SAD = attrs[19]
        rulesetInstance.POINTS_PENALTY_SANDBAG = attrs[20]
        rulesetInstance.POINTS_PENALTY_UNSTUN = attrs[21]
        rulesetInstance.COMBO_DURATION = attrs[22]
        return rulesetInstance

    def __str__(self):
        return repr(self.__dict__)


# Some other default rulesets to choose from
class SemiFinalsCFORuleset(CFORuleset):

    def __init__(self):
        CFORuleset.__init__(self)
        self.TIMER_MODE_TIME_LIMIT = int(60*12.5)
        self.CFO_MAX_HP = 2250


class FinalsCFORuleset(CFORuleset):

    def __init__(self):
        CFORuleset.__init__(self)
        self.TIMER_MODE_TIME_LIMIT = 60*15
        self.CFO_MAX_HP = 3000


# This is where we define modifiers, all modifiers alter a ruleset instance in some way to tweak cfo behavior
# dynamically, first the base class that any modifiers should extend from
class CFORulesetModifierBase(object):

    # This should also be overridden, used so that the client knows which class to use when instantiating modifiers
    MODIFIER_ENUM = -1

    # Maps the above modifier enums to the classes that extend this one
    MODIFIER_SUBCLASSES = {}

    # Some colors to use for titles and percentages etc
    DARK_RED = (230.0/255.0, 20/255.0, 20/255.0, 1)
    RED = (255.0/255.0, 85.0/255.0, 85.0/255.0, 1)

    DARK_GREEN = (0, 180/255.0, 0, 1)
    GREEN = (85.0/255.0, 255.0/255.0, 85.0/255.0, 1)

    DARK_PURPLE = (170.0/255.0, 0, 170.0/255.0, 1)
    PURPLE = (255.0/255.0, 85.0/255.0, 255.0/255.0, 1)

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

    # This method is called to apply this modifiers effect to a CFORuleset instance
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
class ModifierExample(CFORulesetModifierBase):

    # The enum used by astron to know the type
    MODIFIER_ENUM = 69

    TITLE_COLOR = CFORulesetModifierBase.DARK_PURPLE
    DESCRIPTION_COLOR = CFORulesetModifierBase.PURPLE

    def getName(self):
        return 'Funny Number'

    def getDescription(self):
        return "This modifier sets the CFO's hp to %(color_start)s69%(color_end)s"

    def getHeat(self):
        return 69

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_MAX_HP = 69  # Give the cfo 69 hp


# Now here is where we can actually define our modifiers
class ModifierComboExtender(CFORulesetModifierBase):

    MODIFIER_ENUM = 0

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    # The combo percentage increase per tier
    COMBO_DURATION_PER_TIER = [0, 50, 100, 200]

    def getName(self):
        return 'Chains of Finesse %s' % self.numToRoman(self.tier)

    def getDescription(self):
        perc = self.COMBO_DURATION_PER_TIER[self.tier]
        return 'Increases combo length by %(color_start)s+' + str(perc) + '%%%(color_end)s'

    def getHeat(self):
        return -10 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.COMBO_DURATION *= self.additivePercent(self.COMBO_DURATION_PER_TIER[self.tier])


class ModifierComboShortener(CFORulesetModifierBase):

    MODIFIER_ENUM = 1

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.RED

    # The combo percentage increase per tier
    COMBO_DURATION_PER_TIER = [0, 30, 50, 75]

    def getName(self):
        return 'Chain Locker %s' % self.numToRoman(self.tier)

    def getDescription(self):
        perc = self.COMBO_DURATION_PER_TIER[self.tier]
        return 'Decreases combo length by %(color_start)s-' + str(perc) + '%%%(color_end)s'

    def getHeat(self):
        return 10 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.COMBO_DURATION *= self.subtractivePercent(self.COMBO_DURATION_PER_TIER[self.tier])


# Now here is where we can actually define our modifiers
class ModifierCFOHPIncreaser(CFORulesetModifierBase):

    MODIFIER_ENUM = 2

    TITLE_COLOR = CFORulesetModifierBase.DARK_RED
    DESCRIPTION_COLOR = CFORulesetModifierBase.DARK_GREEN

    # The combo percentage increase per tier
    CFO_INCREASE_PER_TIER = [0, 25, 50, 100]

    def getName(self):
        return 'Financial Aid %s' % self.numToRoman(self.tier)

    def getDescription(self):
        perc = self.CFO_INCREASE_PER_TIER[self.tier]
        return 'The CFO has %(color_start)s+' + str(perc) + '%%%(color_end)s more HP'

    def getHeat(self):
        return 200 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_MAX_HP *= self.additivePercent(self.CFO_INCREASE_PER_TIER[self.tier])


# Now here is where we can actually define our modifiers
class ModifierCFOHPDecreaser(CFORulesetModifierBase):

    MODIFIER_ENUM = 3

    TITLE_COLOR = CFORulesetModifierBase.DARK_GREEN
    DESCRIPTION_COLOR = CFORulesetModifierBase.GREEN

    # The combo percentage increase per tier
    CFO_DECREASE_PER_TIER = [0, 20, 35, 50]

    def getName(self):
        return 'Financial Drain %s' % self.numToRoman(self.tier)

    def getDescription(self):
        perc = self.CFO_DECREASE_PER_TIER[self.tier]
        return 'The CFO has %(color_start)s-' + str(perc) + '%%%(color_end)s less HP'

    def getHeat(self):
        return -50 * self.tier

    def apply(self, cfoRuleset):
        cfoRuleset.CFO_MAX_HP *= self.subtractivePercent(self.CFO_DECREASE_PER_TIER[self.tier])


# Any implemented subclasses of CFORulesetModifierBase cannot go past this point
# Loop through all the classes that extend the base modifier class and map an enum to the class for easier construction
for subclass in CFORulesetModifierBase.__subclasses__():
    CFORulesetModifierBase.MODIFIER_SUBCLASSES[subclass.MODIFIER_ENUM] = subclass
