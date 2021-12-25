from toontown.toonbase import ToontownGlobals

# A file to put all crane league settings in one place for easy adjustment

# Ruleset

# CFO SETTINGS
CFO_MAX_HP = 3000  # How much HP should the CFO have?
CFO_STUN_THRESHOLD = 30  # How much damage should a goon do to stun?
SIDECRANE_IMPACT_STUN_THRESHOLD = 0.8  # How much impact should a side crane hit need to register a stun

MIN_GOON_IMPACT = 0.1  # How much impact should a goon hit need to register?
MIN_SAFE_IMPACT = 0.0  # How much impact should a safe hit need to register?
MIN_DEHELMET_IMPACT = 0.5  # How much impact should a safe hit need to desafe the CFO?

RANDOM_GEAR_THROW_ORDER = False  # Should the order in which CFO throw gears at toons be random?

# A dict that maps attack codes to base damage values from the CFO
CFO_ATTACKS_BASE_DAMAGE = {
    ToontownGlobals.BossCogElectricFence: 1,  # The actual bump
    ToontownGlobals.BossCogSwatLeft: 7,  # Swats from bumping
    ToontownGlobals.BossCogSwatRight: 7,
    ToontownGlobals.BossCogSlowDirectedAttack: 25,  # Gear throw
}

# How much should attacks be multiplied by by the time we are towards the end?
CFO_ATTACKS_MULTIPLIER = 3
# should multiplier gradually scale or go up by integers?  False means 1x then 2x then 3x, True gradually increases
CFO_ATTACKS_MULTIPLIER_INTERPOLATE = False

# GOON/TREASURE SETTINGS
MIN_GOON_DAMAGE = 10  # What is the lowest amount of damage a goon should do? (beginning of CFO)
MAX_GOON_DAMAGE = 50  # What is the highest amount of damage a goon should do? (end of CFO)

# How many goons should we allow to spawn? This will scale up towards the end of the fight to the 2nd var
MAX_GOON_AMOUNT_START = 8
MAX_GOON_AMOUNT_END = 16

# How many treasures should we allow to spawn?
MAX_TREASURE_AMOUNT = 15

REALLY_WEAK_TREASURE_HEAL_AMOUNT = 2  # How much should the treasures from very small goons heal?
WEAK_TREASURE_HEAL_AMOUNT = 5  # How much should the treasures from small goons heal?
AVERAGE_TREASURE_HEAL_AMOUNT = 8  # How much should the treasures from med goons heal?
STRONG_TREASURE_HEAL_AMOUNT = 10  # How much should the treasures from the big goons heal?

# Doesn't need to be modified, just used for math
GOON_HEALS = [
    REALLY_WEAK_TREASURE_HEAL_AMOUNT,
    WEAK_TREASURE_HEAL_AMOUNT,
    AVERAGE_TREASURE_HEAL_AMOUNT,
    STRONG_TREASURE_HEAL_AMOUNT,
]
TREASURE_STYLES = [
    [ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock],
    [ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens],
    [ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh],
    [ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland],
]

# TOON SETTINGS
FORCE_MAX_LAFF = False  # Should we force a laff limit for this crane round?
FORCE_MAX_LAFF_AMOUNT = 100  # The laff that we are going to force all toons participating to have
HEAL_TOONS_ON_START = True  # Should we set all toons to full laff when starting the round?

# note: restarting on fail and reviving on death enabled at the same time will NOT work correctly
RESTART_CRANE_ROUND_ON_FAIL = False  # Should we restart the crane round if all toons die?
REVIVE_TOONS_UPON_DEATH = True  # Should we revive a toon that dies after a certain amount of time? (essentially a stun)
REVIVE_TOONS_TIME = 10  # Time in seconds to revive a toon after death
REVIVE_TOONS_LAFF_PERCENTAGE = 0.50  # How much laff should we give back to the toon when revived?

# POINTS SETTINGS
POINTS_GOON_STOMP = 1  # Points per goon stomp
POINTS_STUN = 15  # Points per stun
POINTS_IMPACT = 10  # Points given when a max impact hit is achieved
POINTS_DESAFE = 10  # Points for taking a safe helmet off
POINTS_GOON_KILLED_BY_SAFE = 5  # Points for killing a goon with a safe

POINTS_PENALTY_SAFEHEAD = -20  # Deduction for putting a safe on the CFOs head
POINTS_PENALTY_GO_SAD = -50  # Point deduction for dying (can happen multiple times if revive setting is on)
POINTS_PENALTY_SANDBAG = -5  # Point deduction for hitting a very low impact hit
POINTS_PENALTY_UNSTUN = -20

TREASURE_POINT_PENALTY = True  # Should we deduct points for picking up treasures?
TREASURE_POINT_PENALTY_FLAT_RATE = 0  # How much should we deduct? set to 0 or less to make it 1 to 1 with laff gained

# COMBO SETTINGS
COMBO_DURATION = 2.0  # How long should combos last?
COMBO_DAMAGE_PERCENTAGE = .2  # Percentage to add to our running combo when doing damage (basically 20% bonus per hits when in a combo)
TREASURE_GRAB_RESETS_COMBO = True  # Should picking up a treasure reset a toon's combo?

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

# Debug
VERBOSE_IMPACT = False  # Print impact of cfo objects

