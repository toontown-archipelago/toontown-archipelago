# How long should we have a countdown for before the crane round starts?
# Note that this only affects the crane round when more than one player is present.
# Try to keep this an integer/whole number, or else the cutscene may appear funky.
PREPARE_DELAY = 5
PREPARE_LATENCY_FACTOR = .25  # Add a small buffer for latency and showing the "GO!" text

# Colors of the countdown number right before a crane round starts.
RED_COUNTDOWN_COLOR = (.65, .2, .2, 1)
ORANGE_COUNTDOWN_COLOR = (.65, .45, .2, 1)
YELLOW_COUNTDOWN_COLOR = (.65, .65, .2, 1)
GREEN_COUNTDOWN_COLOR = (.2, .65, .2, 1)
