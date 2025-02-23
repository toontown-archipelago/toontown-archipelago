from enum import IntFlag
# Taken from https://github.com/ArchipelagoMW/Archipelago/blob/main/Options.py to assist with keeping
# definition files contained in this repo as 1 to 1 as possible to the files in the AP repo
# If you are modifying the apworld package, visit that link to see what methods and classes you can utilize.

# The purpose of this file is to simply allow us to use the same exact items and locations files in the toontown
# codebase and for the apworld package with no issue, so most of these classes are left empty

class Visibility(IntFlag):
    none = 0b0000
    template = 0b0001
    simple_ui = 0b0010  # show option in simple menus, such as player-options
    complex_ui = 0b0100  # show option in complex menus, such as weighted-options
    spoiler = 0b1000
    all = 0b1111

class Option:
    pass


class PerGameCommonOptions:
    pass


class StartInventoryPool(Option):
    pass


class Range(Option):
    pass


class Choice(Option):
    pass


class Toggle(Option):
    pass

class OptionSet(Option):
    pass
class OptionList(Option):
    pass

#Used by the APWorld for supporting OptionGroups for display on the website. 
class OptionGroup():
    def __init__(*args, **kwargs):
        pass

class ProgressionBalancing(Option):
    pass

class Accessibility(Option):
    pass

