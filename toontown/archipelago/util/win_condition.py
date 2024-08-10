from __future__ import annotations

import typing

from toontown.quest import Quests
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals

if typing.TYPE_CHECKING:
    from toontown.toon.DistributedToon import DistributedToon
    from toontown.toon.DistributedToonAI import DistributedToonAI


# Base class for defining an AP win condition and contains functionality to extract information to display
# progress/test win conditions based on a toon's state.
class WinCondition:

    def __init__(self, toon: DistributedToon | DistributedToonAI):

        # Since this is an abstract class, this should never be constructed as an instance
        if type(self) is WinCondition:
            raise Exception("WinCondition is abstract and cannot be instantiated")

        self.toon: DistributedToon | DistributedToonAI = toon

    # Returns True if this toon completed their assigned win condition based on their current state
    def satisfied(self) -> bool:
        raise NotImplementedError(f"Missing method override for {self.__class__.__name__}.satisfied()")

    # Generate some text for an NPC to say depending on the state of the win condition
    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        raise NotImplementedError(f"Missing method override for {self.__class__.__name__}.generate_npc_dialogue()")


# Represents a toon that hasn't connected to an AP server, basically a blank win condition when in an invalid state
class NoWinCondition(WinCondition):

    def satisfied(self) -> bool:
        return False

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        return f"Connect to an Archipelago server to have a goal to work towards!"


# Same as a NoWinCondition, but gives the user a message to help them fix their issue
class InvalidWinCondition(NoWinCondition):
    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        return (f"It seems you have an invalid win condition!{delimiter}"
                f"Your win condition ID is set to: {self.toon.slotData.get('win_condition', -1)}.{delimiter}"
                f"This means either your YAML was configured incorrectly or something else went wrong.")


# Represents the win condition on defeating a certain number of bosses
class BossDefeatWinCondition(WinCondition):

    def __init__(self, toon: DistributedToon | DistributedToonAI, bosses: int):
        super().__init__(toon)
        self.bosses_required: int = bosses

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
        return (f'You still have not completed your goal!{delimiter}'
                f'You still must defeat {self.__get_bosses_needed()} unique bosses.{delimiter}'
                f'When you finish, come back and see me!{delimiter}'
                f'Good luck!')


class GlobalTaskWinCondition(WinCondition):

    def __init__(self, toon: DistributedToon | DistributedToonAI, tasks: int):
        super().__init__(toon)
        self.tasks_required: int = tasks

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
        return (f'You still have not completed your goal!{delimiter}'
                f'You still must complete {self.__get_tasks_needed()} more ToonTasks.{delimiter}'
                f'When you finish, come back and see me!{delimiter}'
                f'Good luck!')


class HoodTaskWinCondition(WinCondition):

    # Hoods to consider for win condition
    TASKING_HOODS = (ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens,
                     ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland)

    def __init__(self, toon: DistributedToon | DistributedToonAI, tasks_per_hood: int):
        super().__init__(toon)
        self.tasks_per_hood_needed: int = tasks_per_hood

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

        from toontown.toonbase import TTLocalizer
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
        instructions = ''
        for hood_id in self.TASKING_HOODS:
            tasks_needed = self.tasks_per_hood_needed - task_completion.get(hood_id, 0)
            if tasks_needed <= 0:
                continue

            plural = 's' if tasks_needed > 1 else ''
            instructions += f'{tasks_needed} more ToonTask{plural} completed in {hood_id_to_name.get(hood_id, hood_id)}.{delimiter}'

        return (f'You still have not completed your goal!{delimiter}'
                f'You need to fulfil the following requirements still:{delimiter}'
                f'{instructions}'
                f'When you finish, come back and see me!{delimiter}'
                f'Good luck!')


class GagTrackWinCondition(WinCondition):
    # gag tracks to consider for win condition
    GAG_TRACKS = (ToontownBattleGlobals.HEAL_TRACK, ToontownBattleGlobals.TRAP_TRACK,
                  ToontownBattleGlobals.LURE_TRACK, ToontownBattleGlobals.SOUND_TRACK,
                  ToontownBattleGlobals.THROW_TRACK, ToontownBattleGlobals.SQUIRT_TRACK,
                  ToontownBattleGlobals.DROP_TRACK)
    
    def __init__(self, toon: DistributedToon | DistributedToonAI, gag_tracks: int):
        super().__init__(toon)
        self.gag_tracks = gag_tracks # gag tracks needed to meet win condition
    
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
        gags_needed = self.gag_tracks - sum(self._get_gags_maxxed().values())
        plural = 's' if gags_needed > 1 else ''
        return (f'You still have not completed your goal!{delimiter}'
                f'You still need to max out {gags_needed} gag track{plural}.{delimiter}'
                f'When you finish, come back and see me!{delimiter}'
                f'Good luck!')


class FishSpeciesWinCondition(WinCondition):
    def __init__(self, toon: DistributedToon | DistributedToonAI, fish_species: int):
        super().__init__(toon)
        self.fish_species = fish_species # fish species needed to meet win condition
    
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
        fish_needed = self.fish_species - self._get_fish_species_caught()
        plural = 's' if fish_needed > 1 else ''
        return (f'You still have not completed your goal!{delimiter}'
                f'You still need to catch {fish_needed} more fish species.{delimiter}'
                f'When you finish, come back and see me!{delimiter}'
                f'Good luck!')


class LaffOLympicsWinCondition(WinCondition):
    def __init__(self, toon: DistributedToon | DistributedToonAI, laff_points: int):
        super().__init__(toon)
        self.laff_points = laff_points  # laff points needed to meet win condition

    def satisfied(self) -> bool:
        return self.toon.getMaxHp() >= self.laff_points

    def generate_npc_dialogue(self, delimiter='\x07') -> str:
        laff_needed = self.laff_points - self.toon.getMaxHp()
        plural = 's' if laff_needed > 1 else ''
        return (f'You still have not completed your goal!{delimiter}'
                f'You still need to gain {laff_needed} more Laff Point{plural}.{delimiter}'
                f'When you finish, come back and see me!{delimiter}'
                f'Good luck!')

# Given a win condition ID (given to us via slot data from archipelago) generate and return the corresponding condition
# When new win conditions are added, be sure to add them here
def generate_win_condition(condition_id: int, toon: DistributedToon | DistributedToonAI) -> WinCondition:

    # Special ID used in the "not connected" state
    if condition_id == -2:
        return NoWinCondition(toon)

    # Check for boss defeat condition
    if condition_id == 0:
        return BossDefeatWinCondition(toon, toon.slotData.get('cog_bosses_required', 4))

    # Check for global task condition
    if condition_id == 1:
        return GlobalTaskWinCondition(toon, toon.slotData.get('total_tasks_required', 72))

    # Check for per playground task condition
    if condition_id == 2:
        return HoodTaskWinCondition(toon, toon.slotData.get('hood_tasks_required', 12))
    
    # Check for gag tracks condition
    if condition_id == 3:
        return GagTrackWinCondition(toon, toon.slotData.get('gag_tracks_required', 5))
    
    # check for fish species condition
    if condition_id == 4:
        return FishSpeciesWinCondition(toon, toon.slotData.get('fish_species_required', 70))

    # check for laff-o-lympics condition
    if condition_id == 5:
        return LaffOLympicsWinCondition(toon, toon.slotData.get('laff_points_required', 120))

    # We don't have a valid win condition
    return InvalidWinCondition(toon)
