from enum import Enum


class GroupOperationResult(Enum):
    """
    Used for checking results of various group operations.
    Mostly for checking the state of two toons and what their relationship is to each other
    in the context of what groups they are in or aren't in.
    """
    SUCCESS = "success"
    SUCCESS_BOTH_GROUPLESS = "both toons are not in a group"
    GROUP_FULL = "the group is full"
    GROUP_STARTING = "the group is leaving"
    ALREADY_IN_GROUP = "they are already in a group"
    ALREADY_PRESENT = "they are already in the group"
    IS_SAME_PERSON = "are the same person"
    NONEXISTENT_TOON = "toon does not exist"
