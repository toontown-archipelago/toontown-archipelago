# A file to put all scale settings in one place for easy adjustment
LOW_LAFF_BONUS_TEXT = "UBER BONUS"  # Text to display alongside a low laff bonus

# Text to display in popup text for misc point gains
STUN_TEXT = "STUN!"
PENALTY_GO_SAD_TEXT = "DIED!"


# Ruleset
# Instance attached to cfo boss instances, so we can easily modify stuff dynamically
class CJRuleset:

    def __init__(self):
        # Enable for debugging
        self.GENERAL_DEBUG = False

        self.TIMER_MODE = False  # When true, the cj is timed and ends when time is up, when false, acts as a stopwatch
        self.TIMER_MODE_TIME_LIMIT = 60  # How many seconds do we give the CJ scale round if TIMER_MODE is active?

        self.CJ_MAX_HP = 2700  # How much HP should the CJ have?

        # TOON SETTINGS
        self.FORCE_MAX_LAFF = False  # Should we force a laff limit for this scale round?
        self.FORCE_MAX_LAFF_AMOUNT = 100  # The laff that we are going to force all toons participating to have
        self.HEAL_TOONS_ON_START = False  # Should we set all toons to full laff when starting the round?

        self.WANT_LOW_LAFF_BONUS = True  # Should we award toons with low laff bonus points?
        self.LOW_LAFF_BONUS = .1  # How much will the bonus be worth? i.e. .1 = 10% bonus for ALL points
        self.LOW_LAFF_BONUS_THRESHOLD = 25  # How much laff or less should a toon have to be considered for a low laff bonus?
        self.LOW_LAFF_BONUS_INCLUDE_PENALTIES = True  # Should penalties also be increased when low on laff?

        # note: When REVIVE_TOONS_UPON_DEATH is True, the only fail condition is if we run out of time
        self.RESTART_SCALE_ROUND_ON_FAIL = False  # Should we restart the scale round if all toons die?
        self.REVIVE_TOONS_UPON_DEATH = False  # Should we revive a toon that dies after a certain amount of time? (essentially a stun)
        self.REVIVE_TOONS_TIME = 15  # Time in seconds to revive a toon after death
        self.REVIVE_TOONS_LAFF_PERCENTAGE = 0.50  # How much laff should we give back to the toon when revived?

        # POINTS SETTINGS
        self.POINTS_STUN = 25  # Points per stun
        self.POINTS_PENALTY_GO_SAD = -50  # Point deduction for dying (can happen multiple times if revive setting is on)

        # COMBO SETTINGS
        self.COMBO_DURATION = 2.0  # How long should combos last?

    # Call to make sure certain attributes are within certain bounds, for example dont make required impacts > 100%
    def validate(self):
        pass

    # Sends an astron friendly array over, ONLY STUFF THE CLIENT NEEDS TO KNOW GOES HERE
    # ANY TIME YOU MAKE A NEW ATTRIBUTE IN THE INIT ABOVE, MAKE SURE TO ADD
    # THE ATTRIBUTE INTO THIS LIST BELOW, AND A PARAMETER FOR IT IN THE DC FILE IN THE CFORuleset STRUCT
    def asStruct(self):
        return [
            self.TIMER_MODE,
            self.TIMER_MODE_TIME_LIMIT,
            self.CJ_MAX_HP,
            self.WANT_LOW_LAFF_BONUS,
            self.LOW_LAFF_BONUS,
            self.LOW_LAFF_BONUS_THRESHOLD,
            self.LOW_LAFF_BONUS_INCLUDE_PENALTIES,
            self.REVIVE_TOONS_UPON_DEATH,
            self.REVIVE_TOONS_TIME,
            self.POINTS_STUN,
            self.POINTS_PENALTY_GO_SAD,
            self.COMBO_DURATION
        ]

    @classmethod
    def fromStruct(cls, attrs):
        rulesetInstance = cls()

        rulesetInstance.TIMER_MODE = attrs[0]
        rulesetInstance.TIMER_MODE_TIME_LIMIT = attrs[1]
        rulesetInstance.CJ_MAX_HP = attrs[2]
        rulesetInstance.WANT_LOW_LAFF_BONUS = attrs[3]
        rulesetInstance.LOW_LAFF_BONUS = attrs[4]
        rulesetInstance.LOW_LAFF_BONUS_THRESHOLD = attrs[5]
        rulesetInstance.LOW_LAFF_BONUS_INCLUDE_PENALTIES = attrs[6]
        rulesetInstance.REVIVE_TOONS_UPON_DEATH = attrs[7]
        rulesetInstance.REVIVE_TOONS_TIME = attrs[8]
        rulesetInstance.POINTS_STUN = attrs[9]
        rulesetInstance.POINTS_PENALTY_GO_SAD = attrs[10]
        rulesetInstance.COMBO_DURATION = attrs[11]

        return rulesetInstance

    def __str__(self):
        return repr(self.__dict__)