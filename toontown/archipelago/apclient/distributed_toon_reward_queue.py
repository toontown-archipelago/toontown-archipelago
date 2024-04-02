from typing import List

from toontown.archipelago.definitions.rewards import EarnedAPReward

# How many times a second should we process the queue of rewards for the toon?
DEFAULT_QUEUE_PROCESS_FREQUENCY = 5
TASK_DELAY_TIME = 1 / DEFAULT_QUEUE_PROCESS_FREQUENCY
# How many rewards per run should we process if we have a lot of rewards to handle?
DEFAULT_REWARD_BATCH = 1


# A container for rewards stored on DistributedToonAI that runs at a certain defined interval and handles a defined
# amount of APRewards to apply to a toon
class DistributedToonRewardQueue:

    def __init__(self, toon):
        self.toon = toon
        self._queue: List[EarnedAPReward] = []

    def __getTaskName(self):
        return self.toon.uniqueName('apreward-queue')

    def queue(self, reward: EarnedAPReward):
        self._queue.append(reward)

    # Call to forcibly apply all rewards in the queue
    def finish(self):
        for reward in self._queue:
            reward.apply()
        self._queue.clear()

    def start(self):
        self.stop()
        taskMgr.add(self.__process, name=self.__getTaskName())

    def stop(self):
        self.finish()
        taskMgr.remove(self.__getTaskName())

    # Called via a task. Process rewards in the queue if we have any.
    def __process(self, task):
        task.delayTime = TASK_DELAY_TIME

        operations = min(len(self._queue), DEFAULT_REWARD_BATCH)
        if operations <= 0:
            return task.again

        for index in range(operations):
            reward = self._queue.pop(0)
            reward.apply()

        return task.again
