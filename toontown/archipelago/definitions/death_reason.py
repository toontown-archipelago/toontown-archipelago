from enum import Enum
from typing import Union


class DeathReason(Enum):
    UNKNOWN = "%s went sad due to unforeseen circumstances."

    # Cog fighting
    BATTLING = "%s went sad while battling the Cogs."

    # Boss fights
    # VP
    VP = "%s went sad while fighting the VP."
    VP_JUMP = "%s mistimed a jump in the VP and went sad."
    VP_GEAR = "%s got smacked by a gear thrown by the VP and went sad."
    VP_SWAT = "%s got slapped by the VP and went sad."
    VP_RUNOVER = "%s didn't respect the VP's personal space and went sad."
    VP_STRAFE = "%s doesn't know how to stun the VP properly and went sad."
    VP_SHOWER = "%s got gears rained upon them from the VP and went sad."

    # CFO
    CFO = "%s went sad while fighting the CFO."
    CFO_GOON = "%s got caught by a goon in the CFO and went sad."
    CFO_JUMP = "%s mistimed a jump in the CFO and went sad."
    CFO_GEAR = "%s got smacked by a gear thrown by the CFO and went sad."
    CFO_SWAT = "%s got slapped by the CFO and went sad."
    CFO_RUNOVER = "%s didn't respect the CFO's personal space and went sad."

    CJ = "%s went sad while fighting the CJ."
    CJ_LAWYER = "%s got hit by flying evidence from a lawyer in the CJ and went sad."
    CJ_JUMP = "%s mistimed a jump in the CJ and went sad."
    CJ_GAVEL_SMALL = "%s bumped into a gavel in the CJ and went sad."
    CJ_GAVEL_BIG = "%s got obliterated by a gavel in the CJ and went sad."

    CEO = "%s went sad while fighting the CEO."
    CEO_SQUISHED = "%s got greedy and didn't hop off the banquet table. They got squished by the CEO and went sad."
    CEO_RANOVER = "%s didn't respect the CEO's personal space and went sad."
    CEO_GOLFBALL = "%s got hit by a golf ball in the CEO and went sad."
    CEO_GEAR = "%s got smacked by a gear thrown by the CEO and went sad."
    CEO_SHOWER = "%s got gears rained upon them from the CEO and went sad."

    # Entities that deal damage
    GOON = "%s went sad due to getting spotted by a goon."
    SPOTLIGHT = "%s went sad from gettting caught by a spotlight in a Lawbot Office."

    # Environmental damage
    TRAIN = "%s went sad due to getting ran over by a train in Cashbot HQ."
    STOMPER = "%s got crushed by a stomper and went sad."
    PAINT = "%s fell in a pool of paint and went sad."
    LAVA = "%s slipped into a pool of lava and went sad."
    MAZE = "%s got lost in a Bossbot Cog Golf Course maze and went sad."
    MOLES = "%s forgot to step on the red moles in a Bossbot Cog Golf Course and went sad."

    # Commands
    SPELLBOOK = "%s went sad from abusing the spellbook."

    # Deathlink from another player mainly used to check as a case to prevent dupe deaths.
    # AP will never display this message but putting one here just in case this
    # message wants to be displayed anywhere
    DEATHLINK = "%s couldn't stand the thought of friends dying and went sad."

    # Called to insert a toon name into the message
    def format(self, toon) -> str:
        return self.value % toon.getName()

    # What should be sent over astron?
    def to_astron(self) -> str:
        return self.name

    # What should be received and converted via astron?
    # Returns a DeathReason enum or None
    @classmethod
    def from_astron(cls, name) -> Union[Enum, None]:
        try:
            return cls[name]
        except KeyError:
            return None
