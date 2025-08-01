from toontown.toon import AccessoryGlobals
import json

# This is the animal that will be added to the accessory globals
mergeAnimal = 'e'

default_hats = AccessoryGlobals.HatTransTable
default_glasses = AccessoryGlobals.GlassesTransTable
default_backpacks = AccessoryGlobals.BackpackTransTable
hats = AccessoryGlobals.ExtendedHatTransTable
glasses = AccessoryGlobals.ExtendedGlassesTransTable
backpacks = AccessoryGlobals.ExtendedBackpackTransTable

exists_json = True

try:
    with open('accessoryplacer/accessories.json', 'r') as f:
        extra = json.load(f)
except:
    # template
    exists_json = False
    extra = {
    'hats': {'defaults': {}, 'specific': {}},
    'glasses': {'defaults': {}, 'specific': {}},
    'backpacks': {'defaults': {}, 'specific': {}}
    }
    


def get_key(key):
    try:
        return int(key)
    except ValueError:
        return key

def remove_dups(dic):
    return {k:v for k,v in dic.items() if list(dic.values()).count(v)==1}

def merge(defaultAccessories, specificAccessories, fromDict, type):
    for animal, transform in fromDict['defaults'].items():
        #if animal[0] == mergeAnimal:
        defaultAccessories[animal] = tuple([tuple(x) for x in transform])

    for number, specific in fromDict['specific'].items():
        for animal, transform in specific.items():
            transform = tuple([tuple(x) for x in transform])
            #if animal[0] == mergeAnimal:
            if int(number) not in specificAccessories:
                specificAccessories[int(number)] = {}
            if animal in specificAccessories[int(number)] and specificAccessories[int(number)][animal] == transform:
                continue
            specificAccessories[int(number)][animal] = tuple([tuple(x) for x in transform])

def merge_in_head(defaultAccessories, specificAccessories, toDict, type):
    for animal, transform in defaultAccessories.items():
        if animal in toDict['defaults']:
            continue
        toDict['defaults'][animal] = tuple([tuple(x) for x in transform])

    for number, specific in specificAccessories.items():
        for animal, transform in specific.items():
            if str(number) not in toDict['specific']:
                toDict['specific'][str(number)] = {}
            if animal in toDict['specific'][str(number)]:
                continue
            toDict['specific'][str(number)][animal] = tuple([tuple(x) for x in transform])

def merge_in_torso(defaultAccessories, specificAccessories, toDict, type):
    for animal, transform in defaultAccessories.items():
        if animal in toDict['defaults']:
            continue
        toDict['defaults'][animal] = tuple([tuple(x) for x in transform])

    for numberStr, specific in specificAccessories.items():
        numberStr = int(numberStr)
        for size, transform in specific.items():
            if numberStr not in toDict['specific']:
                toDict['specific'][numberStr] = {}
            if size in toDict['specific'][numberStr].keys():
                continue
            toDict['specific'][numberStr][size] = tuple([tuple(x) for x in transform])

if 'backpacks' not in extra:
    extra['backpacks'] = {'defaults': {}, 'specific': {}}
    merge_in_torso(default_backpacks, backpacks, extra['backpacks'], 'backpacks')

#merge_in(default_hats, hats, extra['hats'], 'hats')
#merge_in(default_glasses, glasses, extra['glasses'], 'glasses')


if exists_json:
    merge(default_backpacks, backpacks, extra['backpacks'], 'backpacks')
    merge(default_hats, hats, extra['hats'], 'hats')
    merge(default_glasses, glasses, extra['glasses'], 'glasses')
    print('Extra exists, writing to JSON')
else:
    # If we don't have a *.JSON file, add new entries
    merge_in_torso(default_backpacks, backpacks, extra['backpacks'], 'backpacks')
    merge_in_head(default_hats, hats, extra['hats'], 'hats')
    merge_in_head(default_glasses, glasses, extra['glasses'], 'glasses')
    print('Extra does NOT exist, creating new entries')

remove_dups(backpacks)

def exportSpecificHead(accessories):
    ids = []

    for number in sorted(accessories.keys()):
        animals = []
        accessory = accessories[number]

        for animal in sorted(accessory.keys()):
            animals.append("        '{0}': {1}".format(animal, accessory[animal]))

        id = '    ' + str(number) + ': {\n' + ',\n'.join(animals) + '\n    }'
        ids.append(id)

    return ',\n'.join(ids)

def exportSpecificTorso(accessories):
    ids = []

    for number in sorted(accessories.keys(), key=lambda t: get_key(t)):
        sizes = []

        for size in sorted(accessories[number].keys()):
            string = "        '{0}': {1}".format(size, accessories[number][size])
            sizes.append(string)

        id = '    ' + str(number) + ': {\n' + ',\n'.join(sizes) + '\n    }'
        if id in ids:
            continue
        ids.append(id)

    return ',\n'.join(ids)

def exportDefault(accessories):
    ids = []

    for animal in sorted(accessories.keys()):
        ids.append("    '{0}': {1}".format(animal, accessories[animal]))

    return ',\n'.join(ids)

DefaultBackpackString = exportDefault(default_backpacks)
DefaultHatString = exportDefault(default_hats)
DefaultGlassesString = exportDefault(default_glasses)
BackpackString = exportSpecificTorso(backpacks)
HatString = exportSpecificHead(hats)
GlassesString = exportSpecificHead(glasses)

result = "BackpackTransTable  = {\n" + DefaultBackpackString + "\n}\nHatTransTable = {\n" + DefaultHatString + "\n}\nGlassesTransTable = {\n" + DefaultGlassesString + "\n}\nExtendedBackpackTransTable = {\n" + BackpackString + "\n}\nExtendedHatTransTable = {\n" + HatString + "\n}\nExtendedGlassesTransTable = {\n" + GlassesString + "\n}"

with open('toontown/toon/AccessoryGlobals.py', 'w') as f:
    f.write(result)

# Re-dump the .json to make sure everything from .py is present.
with open('accessoryplacer/accessories.json', 'w') as f:
    json.dump(extra, f, sort_keys=True, indent=2, separators=(',', ': '))