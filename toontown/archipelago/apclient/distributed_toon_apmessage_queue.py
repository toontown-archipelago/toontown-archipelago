from typing import List

# How many times a second should we process the queue of messages for the toon?
DEFAULT_QUEUE_PROCESS_FREQUENCY = 5
# How many messages per run should we process if we have a lot of messages to handle?
DEFAULT_QUEUE_MESSAGE_BATCH = 10


# A container for messages stored on DistributedToonAI that runs at a certain defined interval and handles a defined
# amount of APRewards to apply to a toon
class DistributedToonAPMessageQueue:

    def __init__(self, toon):
        self.toon = toon
        self._queue: List[str] = []

    def __getTaskName(self):
        return self.toon.uniqueName('apmessage-queue')

    def queue(self, message: str) -> None:
        self._queue.append(message)

    # Call to forcibly apply all rewards in the queue
    def finish(self):
        self.toon.d_sendArchipelagoMessages(self._queue)
        self._queue.clear()

    def start(self):
        taskMgr.add(self.__process, name=self.__getTaskName())

    def stop(self):
        self.finish()
        taskMgr.remove(self.__getTaskName())

    # Called via a task. Process rewards in the queue if we have any.
    def __process(self, task):
        operations = min(len(self._queue), DEFAULT_QUEUE_MESSAGE_BATCH)
        toSend: List[str] = []
        for index in range(operations):
            toSend.append(self._queue.pop(0))

        self.toon.d_sendArchipelagoMessages(toSend)
        task.delayTime = 1 / DEFAULT_QUEUE_PROCESS_FREQUENCY
        return task.again
