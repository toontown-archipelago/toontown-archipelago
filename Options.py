# Taken from https://github.com/ArchipelagoMW/Archipelago/blob/main/Options.py to assist with keeping
# definition files contained in this repo as 1 to 1 as possible to the files in the AP repo
# If you are modifying the apworld package, visit that link to see what methods and classes you can utilize.

# The purpose of this file is to simply allow us to use the same exact items and locations files in the toontown
# codebase and for the apworld package with no issue, so most of these classes are left empty

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


#Used by the APWorld for supporting OptionGroups for display on the website. 
class OptionGroup():
    def __init__(*args, **kwargs):
        pass

class ProgressionBalancing(Option):
    pass

class Accessibility(Option):
    pass
