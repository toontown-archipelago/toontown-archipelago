# Status codes for ready status in groups.
STATUS_EMPTY = 0
STATUS_LEADER = 1
STATUS_READY = 2
STATUS_UNREADY = 3

# Special codes for team related values.
TEAM_SPECTATOR = -1  # This player is watching the game.
TEAM_FFA = 0         # This player is participating in a "free for all" mode.
# later on, we can define more teams if needed or just use raw ints in the code and track them internally.
