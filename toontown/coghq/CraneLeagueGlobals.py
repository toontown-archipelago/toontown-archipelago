# A file to put all crane league settings in one place for easy adjustment

# Ruleset
HEAL_TOONS_ON_START = True  # Should we set all toons to full laff when starting the round?
RESTART_CRANE_ROUND_ON_FAIL = True  # Should we restart the crane round if all toons die?

RANDOM_GEAR_THROW_ORDER = False  # Should the order in which CFO throw gears at toons be random?

TREASURE_POINT_PENALTY = True  # Should we deduct points for picking up treasures?
TREASURE_POINT_PENALTY_FLAT_RATE = 0  # How much should we deduct? set to 0 or less to make it 1 to 1 with laff gained

# Point values
POINTS_GOON_STOMP = 1
POINTS_STUN = 15
POINTS_IMPACT = 10
POINTS_DESAFE = 10

POINTS_PENALTY_SAFEHEAD = -20
POINTS_PENALTY_GO_SAD = -50

# Text to display in popup text for misc point gains
GOON_STOMP_TEXT = 'GOON!'
STUN_TEXT = "STUN!"
IMPACT_TEXT = "IMPACT!"
DESAFE_TEXT = "DESAFE!"

PENALTY_SAFEHEAD_TEXT = "SAFED!"
PENALTY_GO_SAD_TEXT = "DIED!"

# Combo values
COMBO_DURATION = 2.0  # How long should combos last?
COMBO_DAMAGE_PERCENTAGE = .2  # Percentage to add to our running combo when doing damage (basically 20% bonus per hits when in a combo)
