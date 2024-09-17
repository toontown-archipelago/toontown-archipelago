from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from apworld.toontown.consts import ToontownWinCondition

from toontown.quest import Quests
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals, TTLocalizer

if typing.TYPE_CHECKING:
    from toontown.toon.DistributedToon import DistributedToon
    from toontown.toon.DistributedToonAI import DistributedToonAI


# Base class for defining an AP win condition and contains functionality to extract information to display
# progress/test win conditions based on a toon's state.
class WinCondition(ABC):
    def __init__(self, toon: DistributedToon | DistributedToonAI):
        self.toon: DistributedToon | DistributedToonAI = toon

    # Returns True if this toon completed their assigned win condition based on their current state
    @abstractmethod
    def satisfied(self) -> bool: ...

    # Generate some text for an NPC to say depending on the state of the win condition
    @abstractmethod
    def generate_npc_dialogue(self, delimiter='\x07') -> str: ...

    # Generate some text for an NPC to say when all win conditions are complete.
    def generate_npc_victory_dialogue(self, delimiter='\x07') -> str:
        return delimiter.join(["You have completed your goal!",
                "You may now use !release to give the other players in your multi-world the items that you haven't found yet.",
                "Thank you for playing!"])


# Represents a toon that hasn't connected to an AP server, basically a blank win condition when in an invalid state
class NoWinCondition(WinCondition):
    def satisfied(self) -> bool:
        return False

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        return "Connect to an Archipelago server to have a goal to work towards!"


# Similar to NoWinCondition, but when connected. gives the user a message to help.
class InvalidWinCondition(WinCondition):
    def satisfied(self) -> bool:
        return True

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        return "This message should never appear."

    def generate_npc_victory_dialogue(self, delimiter='\x07') -> str:
        self.toon.ConfirmedWinConditionError = True
        return delimiter.join(["It seems you have no valid win condition!",
                f"Your win condition ID is set to: {self.toon.slotData.get('win_condition', -1)}.",
                "This means either your YAML was configured incorrectly, or all win conditions were disabled",
                "Congratulations, you saved toontown by doing nothing!"])


# Represents the win condition on defeating a certain number of bosses
class BossDefeatWinCondition(WinCondition):

    def __init__(self, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.bosses_required: int = toon.slotData.get('cog_bosses_required', 4)

    def __get_bosses_defeated(self) -> int:
        bosses = 0
        for level in self.toon.getCogLevels():
            if level > 0:
                bosses += 1

        return bosses

    def __get_bosses_needed(self) -> int:
        return max(0, self.bosses_required - self.__get_bosses_defeated())

    def satisfied(self) -> bool:
        return self.__get_bosses_needed() <= 0

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        if self.satisfied():
            return 'It seems your bosses goal is completed!'
        return delimiter.join(['You still have not completed your bosses goal!',
                f'You still must defeat {self.__get_bosses_needed()} unique bosses.'])


class GlobalTaskWinCondition(WinCondition):

    def __init__(self, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.tasks_required: int = toon.slotData.get('total_tasks_required', 72)

    # Calculate the intersection of all AP rewards and earned AP rewards and see how many were earned
    def __get_tasks_completed(self) -> int:
        _, reward_history = self.toon.getRewardHistory()
        earned_ap_rewards: set[int] = set(reward_history) & Quests.getAllAPRewardIds()
        # remove the "earned rewards" that are currently in our held quests
        for quest in self.toon.quests:
            questId, fromNpcId, toNpcId, rewardId, toonProgress = quest
            if rewardId in earned_ap_rewards:
                earned_ap_rewards.remove(rewardId)
        return len(earned_ap_rewards)

    # Calculate how many tasks are needed to satisfy the win condition
    def __get_tasks_needed(self) -> int:
        return max(0, self.tasks_required - self.__get_tasks_completed())

    def satisfied(self) -> bool:
        return self.__get_tasks_needed() <= 0

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        if self.satisfied():
            return 'It seems your total ToonTasks goal is completed!'
        return delimiter.join(['You still have not completed your total ToonTasks goal!',
                f'You still must complete {self.__get_tasks_needed()} more ToonTasks.'])


class HoodTaskWinCondition(WinCondition):

    # Hoods to consider for win condition
    TASKING_HOODS = (ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens,
                     ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland)

    def __init__(self, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.tasks_per_hood_needed: int = toon.slotData.get('hood_tasks_required', 12)

    # Calculate a dictionary that represents tasks completed per hood
    # It will always be populated with every hood where tasks may be completed even if no tasks have been completed
    def __get_tasks_completed(self) -> dict[int, int]:

        # First, filter out AP reward IDs specifically
        _, reward_history = self.toon.getRewardHistory()
        earned_ap_rewards: set[int] = set(reward_history) & Quests.getAllAPRewardIds()

        # remove the "earned rewards" that are currently in our held quests
        for quest in self.toon.quests:
            questId, fromNpcId, toNpcId, rewardId, toonProgress = quest
            if rewardId in earned_ap_rewards:
                earned_ap_rewards.remove(rewardId)

        # Then construct a mapping of how many quests were completed per hood
        completion_per_hood: dict[int, int] = {hood_id: 0 for hood_id in self.TASKING_HOODS}
        for ap_reward_id in earned_ap_rewards:
            hood_id = Quests.getHoodFromRewardId(ap_reward_id)
            if hood_id in completion_per_hood:
                completion_per_hood[hood_id] += 1

        return completion_per_hood

    # Returns the # of tasks completed based on hood with least amount of task progress based on quests completed
    # If all playgrounds have 5 tasks completed except for one which only has 3, we return 3.
    def __get_lowest_completion_amount(self) -> int:
        return min(self.__get_tasks_completed().values())

    def satisfied(self) -> bool:
        return self.__get_lowest_completion_amount() >= self.tasks_per_hood_needed

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        if self.satisfied():
            return 'It seems your hood ToonTasks goal is completed!'

        hood_id_to_name = {
            ToontownGlobals.TheBrrrgh: TTLocalizer.lTheBrrrgh,
            ToontownGlobals.DaisyGardens: TTLocalizer.lDaisyGardens,
            ToontownGlobals.DonaldsDock: TTLocalizer.lDonaldsDock,
            ToontownGlobals.DonaldsDreamland: TTLocalizer.lDonaldsDreamland,
            ToontownGlobals.MinniesMelodyland: TTLocalizer.lMinniesMelodyland,
            ToontownGlobals.ToontownCentral: TTLocalizer.lToontownCentral,
        }

        # Generate instructions per playground that still needs task completions
        task_completion = self.__get_tasks_completed()
        instructions = []
        for hood_id in self.TASKING_HOODS:
            tasks_needed = self.tasks_per_hood_needed - task_completion.get(hood_id, 0)
            if tasks_needed <= 0:
                continue
            plural = 's' if tasks_needed > 1 else ''
            instructions.append(f'{tasks_needed} more ToonTask{plural} completed in {hood_id_to_name.get(hood_id, hood_id)}.')

        return delimiter.join(['You still have not completed your hood ToonTasks goal!',
                'You need to fulfil the following requirements still:'] + instructions)


class GagTrackWinCondition(WinCondition):
    # gag tracks to consider for win condition
    GAG_TRACKS = (ToontownBattleGlobals.HEAL_TRACK, ToontownBattleGlobals.TRAP_TRACK,
                  ToontownBattleGlobals.LURE_TRACK, ToontownBattleGlobals.SOUND_TRACK,
                  ToontownBattleGlobals.THROW_TRACK, ToontownBattleGlobals.SQUIRT_TRACK,
                  ToontownBattleGlobals.DROP_TRACK)

    def __init__(self, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.gag_tracks = toon.slotData.get('gag_tracks_required', 5) # gag tracks needed to meet win condition

    # Calculate a dictionary that represents gags maxxed (have 20k exp at least)
    def _get_gags_maxxed(self) -> dict[int, int]:
        gags_maxxed = {track: 0 for track in self.GAG_TRACKS}
        experience = self.toon.experience.getCurrentExperience()
        for track in self.GAG_TRACKS:
            if experience[track] >= 19999:
                gags_maxxed[track] = 1
        return gags_maxxed

    def satisfied(self) -> bool:
        return sum(self._get_gags_maxxed().values()) >= self.gag_tracks

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        if self.satisfied():
            return 'It seems your max gags goal is completed!'
        gags_needed = self.gag_tracks - sum(self._get_gags_maxxed().values())
        plural = 's' if gags_needed > 1 else ''
        return delimiter.join(['You still have not completed your max gags goal!',
                f'You still need to max out {gags_needed} gag track{plural}.'])


class FishSpeciesWinCondition(WinCondition):
    def __init__(self, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.fish_species = toon.slotData.get('fish_species_required', 70)  # fish species needed to meet win condition

    # Calculate how many fish species the toon has caught
    def _get_fish_species_caught(self) -> int:
        if hasattr(self.toon, 'fishCollection'):
            toonsFishCollection = self.toon.fishCollection
        else:
            toonsFishCollection = None
            print(f'win_condition warning: fish collection not found in toon {self.toon.getDoId()}')
            return 0
        if toonsFishCollection is None:
            return 0
        toonsFishCollection = toonsFishCollection.getNetLists()
        toonsFishSpecies = toonsFishCollection[1] # 1 is fish species
        return len(toonsFishSpecies)

    def satisfied(self) -> bool:
        return self._get_fish_species_caught() >= self.fish_species

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        if self.satisfied():
            return 'It seems your fish species is completed!'
        fish_needed = self.fish_species - self._get_fish_species_caught()
        return delimiter.join(['You still have not completed your fish species goal!',
                f'You still need to catch {fish_needed} more fish species.'])


class LaffOLympicsWinCondition(WinCondition):
    def __init__(self, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.laff_points = toon.slotData.get('laff_points_required', 120)  # laff points needed to meet win condition

    def satisfied(self) -> bool:
        return self.toon.getMaxHp() >= self.laff_points

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        if self.satisfied():
            return 'It seems your Laff-O-Lympics goal is completed!'
        laff_needed = self.laff_points - self.toon.getMaxHp()
        plural = 's' if laff_needed > 1 else ''
        return delimiter.join(['You still have not completed your Laff-O-Lympics goal!',
                f'You still need to gain {laff_needed} more Laff Point{plural}.'])

class MultiWinCondition(WinCondition):
    def __init__(self, condition: ToontownWinCondition, toon: DistributedToon | DistributedToonAI):
        super().__init__(toon)
        self.win_conditions: list[WinCondition] = []
        for flag in condition:
            self.win_conditions.append(generate_win_condition(flag, toon))

    def satisfied(self) -> bool:
        return all(condition.satisfied() for condition in self.win_conditions)

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        return delimiter.join(condition.generate_npc_dialogue(delimiter=delimiter) for condition in self.win_conditions)

    def generate_npc_victory_dialogue(self, delimiter='\x07') -> str:
        return delimiter.join(["You have completed your goals!",
                "You may now use !release to give the other players in your multi-world the items that you haven't found yet.",
                "Thank you for playing!"])



# Given a win condition ID (given to us via slot data from archipelago) generate and return the corresponding condition
# When new win conditions are added, be sure to add them here
def generate_win_condition(condition_id: int, toon: DistributedToon | DistributedToonAI) -> WinCondition:

    # Special ID used in the "not connected" state
    if condition_id == -2:
        return NoWinCondition(toon)
    # Any other special ID, that wouldn't be valid for flags, or Archipelago generated with no win conditions enabled.
    if condition_id <= 0:
        return InvalidWinCondition(toon)

    condition = ToontownWinCondition(condition_id)
    win_conditions = {
        ToontownWinCondition.cog_bosses: BossDefeatWinCondition,
        ToontownWinCondition.total_tasks: GlobalTaskWinCondition,
        ToontownWinCondition.hood_tasks: HoodTaskWinCondition,
        ToontownWinCondition.gag_tracks: GagTrackWinCondition,
        ToontownWinCondition.fish_species: FishSpeciesWinCondition,
        ToontownWinCondition.laff_o_lympics: LaffOLympicsWinCondition,
    }

    # Return either a simple win condition matching the settings if only one is enabled,
    # defaulting to a MultiWinCondition container, if it doesn't match exactly.
    return win_conditions.get(condition, lambda toon: MultiWinCondition(condition, toon))(toon)
