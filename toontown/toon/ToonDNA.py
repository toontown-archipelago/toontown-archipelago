import random
from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from toontown.util.BytestringParser import BytestringParser, Packers, migration, ValueType
from toontown.toonbase import TTLocalizer
from io import BytesIO

notify = directNotify.newCategory('ToonDNA')
toonSpeciesTypes = ['d',    # Dog
                    'c',    # Cat
                    'h',    # Horse
                    'm',    # Mouse
                    'r',    # Rabbit
                    'f',    # Duck
                    'p',    # Monkey
                    'b',    # Bear
                    's',    # Pig (swine)
                    'x',    # Deer
                    'z',    # Beaver
                    'a',    # Alligator
                    'v',    # Fox
                    'n',    # Bat
                    't',    # Raccoon
                    'g',    # Turkey
                    'e',    # Koala
                    'j',    # Kangaroo
                    'k',    # Kiwi
                    'l',    # Armadillo
                    ]
toonNameToSpecies = {
    'dog': 'd',       # Dog
    'cat': 'c',       # Cat
    'horse': 'h',     # Horse
    'mouse': 'm',     # Mouse
    'rabbit': 'r',    # Rabbit
    'duck': 'f',      # Duck
    'monkey': 'p',    # Monkey
    'bear': 'b',      # Bear
    'pig': 's',       # Pig (swine)
    'deer': 'x',      # Deer
    'beaver': 'z',    # Beaver
    'alligator': 'a', # Alligator
    'fox': 'v',       # Fox
    'bat': 'n',       # Bat
    'raccoon': 't',   # Raccoon
    'turkey': 'g',    # Turkey
    'koala': 'e',     # Koala
    'kangaroo': 'j',  # Kangaroo
    'kiwi': 'k',      # Kiwi
    'armadillo': 'l', # Armadillo
}
toonHeadTypes = [ "dls", "dss", "dsl", "dll",  # Dog
                  "cls", "css", "csl", "cll",  # Cat
                  "hls", "hss", "hsl", "hll",  # Horse
                  "mls", "mss", "msl", "mll",  # Mouse
                  "rls", "rss", "rsl", "rll",  # Rabbit
                  "fls", "fss", "fsl", "fll",  # Duck (Fowl)
                  "pls", "pss", "psl", "pll",  # Monkey (Primate)
                  "bls", "bss", "bsl", "bll",  # Bear
                  "sls", "sss", "ssl", "sll",  # Pig (swine)
                  "xls", "xss", "xsl", "xll",  # Deer
                  "zls", "zss", "zsl", "zll",  # Beaver
                  "als", "ass", "asl", "all",  # Alligator
                  "vls", "vss", "vsl", "vll",  # Fox
                  "nls", "nss", "nsl", "nll",  # Bat
                  "tls", "tss", "tsl", "tll",  # Raccoon
                  "gls", "gss", "gsl", "gll",  # Turkey
                  "els", "ess", "esl", "ell",  # Koala
                  "jls", "jss", "jsl", "jll",  # Kangaroo
                  "kls", "kss", "ksl", "kll",  # Kiwi
                  "lls", "lss", "lsl", "lll",  # Armadillo
]

def getHeadList(species):
    headList = []
    for head in toonHeadTypes:
        if head[0] == species:
            headList.append(head)

    return headList


def getHeadStartIndex(species):
    for head in toonHeadTypes:
        if head[0] == species:
            return toonHeadTypes.index(head)


def getSpecies(head):
    for species in toonSpeciesTypes:
        if species == head[0]:
            return species


def getSpeciesName(head):
    species = getSpecies(head)
    speciesToSpeciesName = {
        'd': 'dog',
        'c': 'cat',
        'h': 'horse',
        'm': 'mouse',
        'r': 'rabbit',
        'f': 'duck',
        'p': 'monkey',
        'b': 'bear',
        's': 'pig',
        'x': 'deer',
        'z': 'beaver',
        'a': 'alligator',
        'v': 'fox',
        'n': 'bat',
        't': 'raccoon'
    }
    return speciesToSpeciesName[species]

toonHeadAnimalIndices = [ 0, # start of dog heads
                          4, # start of cat heads
                          8, # start of horse heads
                          12, # start of mouse heads
                          16, # start of rabbit heads
                          20, # start of duck heads
                          24, # start of monkey heads
                          28, # start of bear heads
                          32, # start of pig heads
                          36, # start of deer heads
                          40, # start of beaver heads
                          44, # start of alligator heads
                          48, # start of fox heads
                          52, # start of bat heads
                          56, # start of raccoon heads
                          60, # start of turkey heads
                          64, # start of koala heads
                          68, # start of kangaroo heads
                          72, # start of kiwi heads
                          76, # start of armadillo heads
                          ]
toonHeadAnimalIndicesTrial = [0,
 4,
 12,
 14,
 18,
 30]
allToonHeadAnimalIndices = [ 0, 1, 2, 3,      # Dog
                             4, 5, 6, 7,      # Cat
                             8, 9, 10, 11,    # Horse
                             12, 13, 14, 15,  # Mouse
                             16, 17, 18, 19,  # Rabbit
                             20, 21, 22, 23,  # Duck
                             24, 25, 26, 27,  # Monkey
                             28, 29, 30, 31,  # Bear
                             32, 33, 34, 35,  # Pig
                             36, 37, 38, 39,  # Deer
                             40, 41, 42, 43,  # Beaver
                             44, 45, 46, 47,  # Alligator
                             48, 49, 50, 51,  # Fox
                             52, 53, 54, 55,  # Bat
                             56, 57, 58, 59,  # Raccoon
                             60, 61, 62, 63,  # Turkey
                             64, 65, 66, 67,  # Koala
                             68, 69, 70, 71,  # Kangaroo
                             72, 73, 74, 75,  # Kiwi
                             76, 77, 78, 79   # Armadillo
                             ]
toonTorsoTypes = ['ss',
 'ms',
 'ls',
 'sd',
 'md',
 'ld',
 's',
 'm',
 'l']
toonLegTypes = ['s', 'm', 'l']
Shirts = [
    "phase_3/maps/desat_shirt_1.jpg", # 0 solid
    "phase_3/maps/desat_shirt_2.jpg", # 1 single stripe
    "phase_3/maps/desat_shirt_3.jpg", # 2 collar
    "phase_3/maps/desat_shirt_4.jpg", # 3 double stripe
    "phase_3/maps/desat_shirt_5.jpg", # 4 multiple stripes (boy)
    "phase_3/maps/desat_shirt_6.jpg", # 5 collar w/ pocket
    "phase_3/maps/desat_shirt_7.jpg", # 6 flower print (girl)
    "phase_3/maps/desat_shirt_8.jpg", # 7 special, flower trim (girl)
    "phase_3/maps/desat_shirt_9.jpg", # 8 hawaiian (boy)
    "phase_3/maps/desat_shirt_10.jpg", # 9 collar w/ 2 pockets
    "phase_3/maps/desat_shirt_11.jpg", # 10 bowling shirt 
    "phase_3/maps/desat_shirt_12.jpg", # 11 special, vest (boy)
    "phase_3/maps/desat_shirt_13.jpg", # 12 special (no color), denim vest (girl)
    "phase_3/maps/desat_shirt_14.jpg", # 13 peasant (girl)
    "phase_3/maps/desat_shirt_15.jpg", # 14 collar w/ ruffles
    "phase_3/maps/desat_shirt_16.jpg", # 15 peasant w/ mid stripe (girl)
    "phase_3/maps/desat_shirt_17.jpg", # 16 special (no color), soccer jersey
    "phase_3/maps/desat_shirt_18.jpg", # 17 special, lightning bolt
    "phase_3/maps/desat_shirt_19.jpg", # 18 special, jersey 19 (boy)
    "phase_3/maps/desat_shirt_20.jpg", # 19 guayavera (boy)
    "phase_3/maps/desat_shirt_21.jpg", # 20 hearts (girl)
    "phase_3/maps/desat_shirt_22.jpg", # 21 special, stars (girl)
    "phase_3/maps/desat_shirt_23.jpg", # 22 flower (girl)

    # Catalog exclusive shirts
    "phase_4/maps/female_shirt1b.jpg", # 23 blue with 3 yellow stripes
    "phase_4/maps/female_shirt2.jpg", # 24 pink and beige with flower
    "phase_4/maps/female_shirt3.jpg", # 25 yellow hooded sweatshirt (also for boys)
    "phase_4/maps/male_shirt1.jpg", # 26 blue stripes
    "phase_4/maps/male_shirt2_palm.jpg", # 27 yellow with palm tree
    "phase_4/maps/male_shirt3c.jpg", # 28 orange

    # Halloween
    "phase_4/maps/shirt_ghost.jpg", # 29 ghost (Halloween)
    "phase_4/maps/shirt_pumkin.jpg", # 30 pumpkin (Halloween)

    # Winter holiday
    "phase_4/maps/holiday_shirt1.jpg", # 31 (Winter Holiday)
    "phase_4/maps/holiday_shirt2b.jpg", # 32 (Winter Holiday)
    "phase_4/maps/holidayShirt3b.jpg", # 33 (Winter Holiday)
    "phase_4/maps/holidayShirt4.jpg", # 34 (Winter Holiday)

    # Catalog 2 exclusive shirts
    "phase_4/maps/female_shirt1b.jpg",    # 35 Blue and gold wavy stripes
    "phase_4/maps/female_shirt5New.jpg",  # 36 Blue and pink with bow
    "phase_4/maps/shirtMale4B.jpg",       # 37 Lime green with stripe
    "phase_4/maps/shirt6New.jpg",         # 38 Purple with stars
    "phase_4/maps/shirtMaleNew7.jpg",     # 39 Red kimono with checkerboard

    # Unused
    "phase_4/maps/femaleShirtNew6.jpg",   # 40 Aqua kimono white stripe

    # Valentines
    "phase_4/maps/Vday1Shirt5.jpg",       # 41 (Valentines)
    "phase_4/maps/Vday1Shirt6SHD.jpg",    # 42 (Valentines)
    "phase_4/maps/Vday1Shirt4.jpg",       # 43 (Valentines)
    "phase_4/maps/Vday_shirt2c.jpg",      # 44 (Valentines)

    # Catalog 3 exclusive shirts
    "phase_4/maps/shirtTieDyeNew.jpg",    # 45 Tie dye
    "phase_4/maps/male_shirt1.jpg",       # 46 Light blue with blue and white stripe

    # St Patrick's Day shirts
    "phase_4/maps/StPats_shirt1.jpg",     # 47 (St. Pats) Four leaf clover shirt
    "phase_4/maps/StPats_shirt2.jpg",     # 48 (St. Pats) Pot o gold

    # T-Shirt Contest shirts
    "phase_4/maps/ContestfishingVestShirt2.jpg",    # 49 (T-shirt Contest) Fishing Vest
    "phase_4/maps/ContestFishtankShirt1.jpg",       # 50 (T-shirt Contest) Fish Tank
    "phase_4/maps/ContestPawShirt1.jpg",            # 51 (T-shirt Contest) Paw Print

    # Catlog 4 exclusive shirts
    "phase_4/maps/CowboyShirt1.jpg",    # 52 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt2.jpg",    # 53 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt3.jpg",    # 54 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt4.jpg",    # 55 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt5.jpg",    # 56 (Western) Cowboy Shirt
    "phase_4/maps/CowboyShirt6.jpg",    # 57 (Western) Cowboy Shirt

    # July 4 shirts
    "phase_4/maps/4thJulyShirt1.jpg",   # 58 (July 4th) Flag Shirt
    "phase_4/maps/4thJulyShirt2.jpg",   # 59 (July 4th) Fireworks Shirt

    # Catalog 7 exclusive shirts
    "phase_4/maps/shirt_Cat7_01.jpg",   # 60 Green w/ yellow buttons
    "phase_4/maps/shirt_Cat7_02.jpg",   # 61 Purple w/ big flower

    # T-Shirt Contest 2 shirts
    "phase_4/maps/contest_backpack3.jpg",    # 62 Multicolor shirt w/ backpack
    "phase_4/maps/contest_leder.jpg",     # 63 Lederhosen
    "phase_4/maps/contest_mellon2.jpg",   # 64 Watermelon
    "phase_4/maps/contest_race2.jpg",     # 65 Race Shirt (UK winner)
    
    # Pajama shirts
    "phase_4/maps/PJBlueBanana2.jpg", # 66 Blue Banana PJ Shirt
    "phase_4/maps/PJRedHorn2.jpg", # 67 Red Horn PJ Shirt
    "phase_4/maps/PJGlasses2.jpg", # 68 Purple Glasses PJ Shirt
    
    # 2009 Valentines Day Shirts
    "phase_4/maps/tt_t_chr_avt_shirt_valentine1.jpg", # 69 Valentines Shirt 1
    "phase_4/maps/tt_t_chr_avt_shirt_valentine2.jpg", # 70 Valentines Shirt 2    
    
    # Award Clothes
    "phase_4/maps/tt_t_chr_avt_shirt_desat4.jpg",    # 71
    "phase_4/maps/tt_t_chr_avt_shirt_fishing1.jpg",   # 72
    "phase_4/maps/tt_t_chr_avt_shirt_fishing2.jpg",  # 73
    "phase_4/maps/tt_t_chr_avt_shirt_gardening1.jpg",   # 74
    "phase_4/maps/tt_t_chr_avt_shirt_gardening2.jpg",   # 75
    "phase_4/maps/tt_t_chr_avt_shirt_party1.jpg",   # 76
    "phase_4/maps/tt_t_chr_avt_shirt_party2.jpg",   # 77
    "phase_4/maps/tt_t_chr_avt_shirt_racing1.jpg",  # 78
    "phase_4/maps/tt_t_chr_avt_shirt_racing2.jpg",  # 79 
    "phase_4/maps/tt_t_chr_avt_shirt_summer1.jpg",   # 80
    "phase_4/maps/tt_t_chr_avt_shirt_summer2.jpg",   # 81
    
    "phase_4/maps/tt_t_chr_avt_shirt_golf1.jpg",    # 82
    "phase_4/maps/tt_t_chr_avt_shirt_golf2.jpg",    # 83
    "phase_4/maps/tt_t_chr_avt_shirt_halloween1.jpg",   # 84
    "phase_4/maps/tt_t_chr_avt_shirt_halloween2.jpg",   # 85
    "phase_4/maps/tt_t_chr_avt_shirt_marathon1.jpg",    # 86
    "phase_4/maps/tt_t_chr_avt_shirt_saveBuilding1.jpg",    # 87
    "phase_4/maps/tt_t_chr_avt_shirt_saveBuilding2.jpg",    # 88 
    "phase_4/maps/tt_t_chr_avt_shirt_toonTask1.jpg",    # 89
    "phase_4/maps/tt_t_chr_avt_shirt_toonTask2.jpg",    # 90
    "phase_4/maps/tt_t_chr_avt_shirt_trolley1.jpg",     # 91
    "phase_4/maps/tt_t_chr_avt_shirt_trolley2.jpg",     # 92
    "phase_4/maps/tt_t_chr_avt_shirt_winter1.jpg",      # 93
    "phase_4/maps/tt_t_chr_avt_shirt_halloween3.jpg",   # 94
    "phase_4/maps/tt_t_chr_avt_shirt_halloween4.jpg",   # 95
    # 2010 Valentines Day Shirts
    "phase_4/maps/tt_t_chr_avt_shirt_valentine3.jpg", # 96 Valentines Shirt 3
    
    # Scientist Shirts
    "phase_4/maps/tt_t_chr_shirt_scientistC.jpg",   # 97
    "phase_4/maps/tt_t_chr_shirt_scientistA.jpg",   # 98
    "phase_4/maps/tt_t_chr_shirt_scientistB.jpg",   # 99
    
    # Silly Story Shirts
    "phase_4/maps/tt_t_chr_avt_shirt_mailbox.jpg",  # 100 Mailbox Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_trashcan.jpg", # 101 Trash Can Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_loonyLabs.jpg",# 102 Loony Labs Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_hydrant.jpg",  # 103 Hydrant Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_whistle.jpg",  # 104 Sillymeter Whistle Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_cogbuster.jpg",  # 105 Silly Cogbuster Shirt
    
    "phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated01.jpg",  # 106 Most Cogs Defeated Shirt
    "phase_4/maps/tt_t_chr_avt_shirt_victoryParty01.jpg",  # 107 Victory Party Shirt 1
    "phase_4/maps/tt_t_chr_avt_shirt_victoryParty02.jpg",  # 108 Victory Party Shirt 2
    'phase_4/maps/tt_t_chr_avt_shirt_sellbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_sellbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_sellbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_jellyBeans.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_doodle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween5.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloweenTurtle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_greentoon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_getConnectedMoverShaker.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racingGrandPrix.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_lawbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_lawbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_lawbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_bee.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_supertoon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_vampire.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_dinosaur.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding3.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_winter03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_winter02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_anniversary.jpg']

BoyShirts = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (8, 8), (9, 9), (10, 0), (11, 0), (14, 10), (16, 0), (17, 0), (18, 12), (19, 13)]
GirlShirts = [(0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7), (9, 9), (12, 0), (13, 11), (15, 11), (16, 0), (20, 0), (21, 0), (22, 0)]

def isValidBoyShirt(index):
    for pair in BoyShirts:
        if (index == pair[0]):
            return 1
    return 0

def isValidGirlShirt(index):
    for pair in GirlShirts:
        if (index == pair[0]):
            return 1
    return 0

Sleeves = [
    "phase_3/maps/desat_sleeve_1.jpg", # 0
    "phase_3/maps/desat_sleeve_2.jpg", # 1
    "phase_3/maps/desat_sleeve_3.jpg", # 2 
    "phase_3/maps/desat_sleeve_4.jpg", # 3
    "phase_3/maps/desat_sleeve_5.jpg", # 4 
    "phase_3/maps/desat_sleeve_6.jpg", # 5
    "phase_3/maps/desat_sleeve_7.jpg", # 6
    "phase_3/maps/desat_sleeve_8.jpg", # 7 
    "phase_3/maps/desat_sleeve_9.jpg", # 8
    "phase_3/maps/desat_sleeve_10.jpg", # 9
    "phase_3/maps/desat_sleeve_15.jpg", # 10
    "phase_3/maps/desat_sleeve_16.jpg", # 11
    "phase_3/maps/desat_sleeve_19.jpg", # 12
    "phase_3/maps/desat_sleeve_20.jpg", # 13

    # Catalog exclusive shirt sleeves
    "phase_4/maps/female_sleeve1b.jpg", # 14 blue with 3 yellow stripes
    "phase_4/maps/female_sleeve2.jpg", # 15 pink and beige with flower
    "phase_4/maps/female_sleeve3.jpg", # 16 yellow hooded sweatshirt
    "phase_4/maps/male_sleeve1.jpg", # 17 blue stripes
    "phase_4/maps/male_sleeve2_palm.jpg", # 18 yellow with palm tree
    "phase_4/maps/male_sleeve3c.jpg", # 19 orange

    "phase_4/maps/shirt_Sleeve_ghost.jpg", # 20 ghost (Halloween)
    "phase_4/maps/shirt_Sleeve_pumkin.jpg", # 21 pumpkin (Halloween)

    "phase_4/maps/holidaySleeve1.jpg", # 22 (Winter Holiday)
    "phase_4/maps/holidaySleeve3.jpg", # 23 (Winter Holiday)

    # Catalog series 2
    "phase_4/maps/female_sleeve1b.jpg",   # 24 Blue and gold wavy stripes
    "phase_4/maps/female_sleeve5New.jpg", # 25 Blue and pink with bow
    "phase_4/maps/male_sleeve4New.jpg",   # 26 Lime green with stripe
    "phase_4/maps/sleeve6New.jpg",        # 27 Purple with stars
    "phase_4/maps/SleeveMaleNew7.jpg",    # 28 Red kimono/hockey shirt

    # Unused
    "phase_4/maps/female_sleeveNew6.jpg", # 29 Aqua kimono white stripe

    "phase_4/maps/Vday5Sleeve.jpg",       # 30 (Valentines)
    "phase_4/maps/Vda6Sleeve.jpg",        # 31 (Valentines)
    "phase_4/maps/Vday_shirt4sleeve.jpg", # 32 (Valentines)
    "phase_4/maps/Vday2cSleeve.jpg",      # 33 (Valentines)

    # Catalog series 3
    "phase_4/maps/sleeveTieDye.jpg",      # 34 Tie dye
    "phase_4/maps/male_sleeve1.jpg",      # 35 Blue with blue and white stripe

    # St. Patrick's day
    "phase_4/maps/StPats_sleeve.jpg",     # 36 (St. Pats) Four leaf clover
    "phase_4/maps/StPats_sleeve2.jpg",    # 37 (St. Pats) Pot o gold

    # T-Shirt Contest sleeves
    "phase_4/maps/ContestfishingVestSleeve1.jpg",    # 38 (T-Shirt Contest) fishing vest sleeve
    "phase_4/maps/ContestFishtankSleeve1.jpg",       # 39 (T-Shirt Contest) fish bowl sleeve
    "phase_4/maps/ContestPawSleeve1.jpg",            # 40 (T-Shirt Contest) paw print sleeve

    # Catalog Series 4
    "phase_4/maps/CowboySleeve1.jpg",    # 41 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve2.jpg",    # 42 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve3.jpg",    # 43 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve4.jpg",    # 44 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve5.jpg",    # 45 (Western) cowboy shirt sleeve
    "phase_4/maps/CowboySleeve6.jpg",    # 46 (Western) cowboy shirt sleeve

    # July 4th
    "phase_4/maps/4thJulySleeve1.jpg",   # 47 (July 4th) flag shirt sleeve
    "phase_4/maps/4thJulySleeve2.jpg",   # 48 (July 4th) fireworks shirt sleeve

    # Catlog series 7
    "phase_4/maps/shirt_sleeveCat7_01.jpg",   # 49 Green shirt w/ yellow buttons sleeve
    "phase_4/maps/shirt_sleeveCat7_02.jpg",   # 50 Purple shirt w/ big flower sleeve

    # T-Shirt Contest 2 sleeves
    "phase_4/maps/contest_backpack_sleeve.jpg",   # 51 (T-Shirt Contest) Multicolor shirt 2/ backpack sleeve
    "phase_4/maps/Contest_leder_sleeve.jpg",      # 52 (T-Shirt Contest) Lederhosen sleeve
    "phase_4/maps/contest_mellon_sleeve2.jpg",     # 53 (T-Shirt Contest) Watermelon sleeve
    "phase_4/maps/contest_race_sleeve.jpg",       # 54 (T-Shirt Contest) Race Shirt sleeve (UK winner)
    
    # Pajama sleeves
    "phase_4/maps/PJSleeveBlue.jpg",   # 55 Blue Pajama sleeve
    "phase_4/maps/PJSleeveRed.jpg",   # 56 Red Pajama sleeve
    "phase_4/maps/PJSleevePurple.jpg",   # 57 Purple Pajama sleeve
    
    # 2009 Valentines Day Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine1.jpg",   # 58 Valentines Sleeves 1
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine2.jpg",   # 59 Valentines Sleeves 2
    
    # Special Award Clothing
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_desat4.jpg",   # 60
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing1.jpg",   # 61
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing2.jpg",   # 62
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening1.jpg",   # 63
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening2.jpg",   # 64
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_party1.jpg",   # 65
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_party2.jpg",   # 66
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_racing1.jpg",   # 67
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_racing2.jpg",   # 68
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_summer1.jpg",   # 69
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_summer2.jpg",   # 70
    
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_golf1.jpg",    # 71
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_golf2.jpg",    # 72
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween1.jpg",    # 73
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween2.jpg",    # 74
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_marathon1.jpg",    # 75
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding1.jpg",    # 76
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding2.jpg",    # 77
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask1.jpg",    # 78
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask2.jpg",    # 79
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley1.jpg",    # 80
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley2.jpg",    # 81
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_winter1.jpg",    # 82
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween3.jpg",   # 83
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween4.jpg",   # 84
    
    # 2010 Valentines Day Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine3.jpg",   # 85 Valentines Sleeves 1
    
    # Scientist Sleeves
    "phase_4/maps/tt_t_chr_shirtSleeve_scientist.jpg",   # 86 Toon sceintist
    
    # Silly Story Shirt Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_mailbox.jpg",    # 87 Mailbox Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_trashcan.jpg",   # 88 Trash Can Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_loonyLabs.jpg",  # 89 Loony Labs Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_hydrant.jpg",    # 90 Hydrant Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_whistle.jpg",    # 91 Sillymeter Whistle Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_cogbuster.jpg",    # 92 Silly Cogbuster Sleeves
    
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated01.jpg",# 93 Most Cogs Defeated Sleeves
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty01.jpg",    # 94 Victory Party Sleeves 1
    "phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty02.jpg",    # 95 Victory Party Sleeves 2
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_jellyBeans.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_doodle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween5.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloweenTurtle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_greentoon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_getConnectedMoverShaker.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racingGrandPrix.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_bee.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_supertoon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_vampire.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_dinosaur.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding3.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_anniversary.jpg']

# len = 9 
BoyShorts = [
    "phase_3/maps/desat_shorts_1.jpg", # plain w/ pockets
    "phase_3/maps/desat_shorts_2.jpg", # belt
    "phase_3/maps/desat_shorts_4.jpg", # cargo
    "phase_3/maps/desat_shorts_6.jpg", # hawaiian
    "phase_3/maps/desat_shorts_7.jpg", # special, side stripes
    "phase_3/maps/desat_shorts_8.jpg", # soccer shorts 
    "phase_3/maps/desat_shorts_9.jpg", # special, flames side stripes
    "phase_3/maps/desat_shorts_10.jpg", # denim (2 darker colors)

    # Valentines
    "phase_4/maps/VdayShorts2.jpg",    # 8 valentines shorts

    # Catalog series 3 exclusive
    "phase_4/maps/shorts4.jpg",        # 9 Orange with blue side stripes
    "phase_4/maps/shorts1.jpg",        # 10 Blue with gold stripes on cuff

    # St. Pats
    "phase_4/maps/shorts5.jpg",        # 11 Leprechaun shorts

    # Catalog series 4 exclusive
    "phase_4/maps/CowboyShorts1.jpg",  # 12 Cowboy Shorts 1
    "phase_4/maps/CowboyShorts2.jpg",  # 13 Cowboy Shorts 2
    # July 4th
    "phase_4/maps/4thJulyShorts1.jpg", # 14 July 4th Shorts

    # Catalog series 7
    "phase_4/maps/shortsCat7_01.jpg",  # 15 Green stripes
    
    # Pajama Shorts
    "phase_4/maps/Blue_shorts_1.jpg",  # 16 Blue Pajama shorts
    "phase_4/maps/Red_shorts_1.jpg",  # 17 Red Pajama shorts
    "phase_4/maps/Purple_shorts_1.jpg",  # 18 Purple Pajama shorts
    
    # Winter Holiday Shorts
    "phase_4/maps/tt_t_chr_avt_shorts_winter1.jpg",  # 19 Winter Holiday Shorts Style 1
    "phase_4/maps/tt_t_chr_avt_shorts_winter2.jpg",  # 20 Winter Holiday Shorts Style 2
    "phase_4/maps/tt_t_chr_avt_shorts_winter3.jpg",  # 21 Winter Holiday Shorts Style 3
    "phase_4/maps/tt_t_chr_avt_shorts_winter4.jpg",  # 22 Winter Holiday Shorts Style 4
    
    # 2009 Valentines Day Shorts
    "phase_4/maps/tt_t_chr_avt_shorts_valentine1.jpg",  # 23 Valentines Shorts 1
    "phase_4/maps/tt_t_chr_avt_shorts_valentine2.jpg",  # 24 Valentines Shorts 2
    
    # Special award Clothes
    "phase_4/maps/tt_t_chr_avt_shorts_fishing1.jpg",   # 25
    "phase_4/maps/tt_t_chr_avt_shorts_gardening1.jpg",   # 26
    "phase_4/maps/tt_t_chr_avt_shorts_party1.jpg",   # 27
    "phase_4/maps/tt_t_chr_avt_shorts_racing1.jpg",   # 28
    "phase_4/maps/tt_t_chr_avt_shorts_summer1.jpg",   # 29
    
    "phase_4/maps/tt_t_chr_avt_shorts_golf1.jpg",   # 30
    "phase_4/maps/tt_t_chr_avt_shorts_halloween1.jpg",   # 31
    "phase_4/maps/tt_t_chr_avt_shorts_halloween2.jpg",   # 32
    "phase_4/maps/tt_t_chr_avt_shorts_saveBuilding1.jpg",   # 33
    "phase_4/maps/tt_t_chr_avt_shorts_trolley1.jpg",   # 34
    "phase_4/maps/tt_t_chr_avt_shorts_halloween4.jpg",   # 35
    "phase_4/maps/tt_t_chr_avt_shorts_halloween3.jpg",   # 36
    
    "phase_4/maps/tt_t_chr_shorts_scientistA.jpg",   # 37
    "phase_4/maps/tt_t_chr_shorts_scientistB.jpg",   # 38
    "phase_4/maps/tt_t_chr_shorts_scientistC.jpg",   # 39
    
    "phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg",  # 40 Silly Cogbuster Shorts     
    'phase_4/maps/tt_t_chr_avt_shorts_sellbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloween5.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloweenTurtle.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_greentoon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racingGrandPrix.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_lawbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_bee.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_supertoon.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_vampire.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_dinosaur.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf03.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing03.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf04.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf05.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing05.jpg']

SHORTS = 0
SKIRT = 1

# len = 14 
GirlBottoms = [
    ("phase_3/maps/desat_skirt_1.jpg", SKIRT), # 0 solid
    ("phase_3/maps/desat_skirt_2.jpg", SKIRT), # 1 special, polka dots
    ("phase_3/maps/desat_skirt_3.jpg", SKIRT), # 2 vertical stripes
    ("phase_3/maps/desat_skirt_4.jpg", SKIRT), # 3 horizontal stripe
    ("phase_3/maps/desat_skirt_5.jpg", SKIRT), # 4 flower print
    ("phase_3/maps/desat_shorts_1.jpg", SHORTS), # 5 plain w/ pockets
    ("phase_3/maps/desat_shorts_5.jpg", SHORTS), # 6 flower
    ("phase_3/maps/desat_skirt_6.jpg", SKIRT), # 7 special, 2 pockets
    ("phase_3/maps/desat_skirt_7.jpg", SKIRT), # 8 denim (2 darker colors)
    ("phase_3/maps/desat_shorts_10.jpg", SHORTS), # 9 denim (2 darker colors)

    # Catalog Series 1 exclusive
    ("phase_4/maps/female_skirt1.jpg", SKIRT), # 10 blue with tan border and button
    ("phase_4/maps/female_skirt2.jpg", SKIRT), # 11 purple with pink border and ribbon
    ("phase_4/maps/female_skirt3.jpg", SKIRT), # 12 teal with yellow border and star

    # Valentines
    ("phase_4/maps/VdaySkirt1.jpg", SKIRT),    # 13 valentines skirts

    # Catalog Series 3 exclusive
    ("phase_4/maps/skirtNew5.jpg", SKIRT),     # 14 rainbow skirt

    ("phase_4/maps/shorts5.jpg", SHORTS),      # 15 leprechaun shorts
    # St. Pats

    # Catalog Series 4 exclusive
    ("phase_4/maps/CowboySkirt1.jpg", SKIRT),     # 16 cowboy skirt 1
    ("phase_4/maps/CowboySkirt2.jpg", SKIRT),     # 17 cowboy skirt 2

    # July 4th Skirt
    ("phase_4/maps/4thJulySkirt1.jpg", SKIRT),    # 18 july 4th skirt 1

    # Catalog series 7
    ("phase_4/maps/skirtCat7_01.jpg", SKIRT),    # 19 blue with flower
    
    # Pajama Shorts
    ("phase_4/maps/Blue_shorts_1.jpg", SHORTS),  # 20 Blue Pajama shorts
    ("phase_4/maps/Red_shorts_1.jpg", SHORTS),   # 21 Red Pajama shorts
    ("phase_4/maps/Purple_shorts_1.jpg", SHORTS),# 22 Purple Pajama shorts
    
    # Winter Holiday Skirts
    ("phase_4/maps/tt_t_chr_avt_skirt_winter1.jpg", SKIRT),  # 23 Winter Holiday Skirt Style 1
    ("phase_4/maps/tt_t_chr_avt_skirt_winter2.jpg", SKIRT),  # 24 Winter Holiday Skirt Style 2
    ("phase_4/maps/tt_t_chr_avt_skirt_winter3.jpg", SKIRT),  # 25 Winter Holiday Skirt Style 3
    ("phase_4/maps/tt_t_chr_avt_skirt_winter4.jpg", SKIRT),  # 26 Winter Holiday Skirt Style 4
    
    # 2009 Valentines Day Skirts
    ("phase_4/maps/tt_t_chr_avt_skirt_valentine1.jpg", SKIRT),  # 27 Valentines Skirt 1
    ("phase_4/maps/tt_t_chr_avt_skirt_valentine2.jpg", SKIRT),  # 28 Valentines Skirt 2
    
    # Special award clothing
    ("phase_4/maps/tt_t_chr_avt_skirt_fishing1.jpg", SKIRT),   # 29
    ("phase_4/maps/tt_t_chr_avt_skirt_gardening1.jpg", SKIRT),   # 30
    ("phase_4/maps/tt_t_chr_avt_skirt_party1.jpg", SKIRT),   # 31
    ("phase_4/maps/tt_t_chr_avt_skirt_racing1.jpg", SKIRT),   # 32
    ("phase_4/maps/tt_t_chr_avt_skirt_summer1.jpg", SKIRT),   # 33
    
    ("phase_4/maps/tt_t_chr_avt_skirt_golf1.jpg", SKIRT),   # 34
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween1.jpg", SKIRT),   # 35
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween2.jpg", SKIRT),   # 36
    ("phase_4/maps/tt_t_chr_avt_skirt_saveBuilding1.jpg", SKIRT),   # 37
    ("phase_4/maps/tt_t_chr_avt_skirt_trolley1.jpg", SKIRT),   # 38
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween3.jpg", SKIRT),   # 39
    ("phase_4/maps/tt_t_chr_avt_skirt_halloween4.jpg", SKIRT),   # 40
    
    ("phase_4/maps/tt_t_chr_shorts_scientistA.jpg", SHORTS),   # 41
    ("phase_4/maps/tt_t_chr_shorts_scientistB.jpg", SHORTS),   # 42
    ("phase_4/maps/tt_t_chr_shorts_scientistC.jpg", SHORTS),   # 43
    
    ("phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg", SHORTS),   # 44 Silly Cogbuster Shorts 
    ('phase_4/maps/tt_t_chr_avt_shorts_sellbotCrusher.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_halloween5.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_halloweenTurtle.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_greentoon1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racingGrandPrix.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_shorts_lawbotCrusher.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_bee.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_pirate.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_pirate.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_shorts_supertoon.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_vampire.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_dinosaur.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf02.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing03.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf03.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf04.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing04.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing05.jpg', SKIRT)]

# len = 28
ClothesColors = [
    # Boy shirts (0 - 12)
    VBase4(0.933594, 0.265625, 0.28125, 1.0),  # (0) bright red
    VBase4(0.863281, 0.40625, 0.417969, 1.0),  # (1) light red
    VBase4(0.710938, 0.234375, 0.4375, 1.0),   # (2) plum
    VBase4(0.992188, 0.480469, 0.167969, 1.0), # (3) orange
    VBase4(0.996094, 0.898438, 0.320312, 1.0), # (4) yellow
    VBase4(0.550781, 0.824219, 0.324219, 1.0), # (5) light green
    VBase4(0.242188, 0.742188, 0.515625, 1.0), # (6) seafoam   
    VBase4(0.433594, 0.90625, 0.835938, 1.0),  # (7) light blue green
    VBase4(0.347656, 0.820312, 0.953125, 1.0), # (8) light blue
    VBase4(0.191406, 0.5625, 0.773438, 1.0),   # (9) medium blue
    VBase4(0.285156, 0.328125, 0.726562, 1.0),
    VBase4(0.460938, 0.378906, 0.824219, 1.0), # (11) purple blue
    VBase4(0.546875, 0.28125, 0.75, 1.0),      # (12) dark purple blue
    # Boy shorts
    VBase4(0.570312, 0.449219, 0.164062, 1.0),
    VBase4(0.640625, 0.355469, 0.269531, 1.0),
    VBase4(0.996094, 0.695312, 0.511719, 1.0),
    VBase4(0.832031, 0.5, 0.296875, 1.0),
    VBase4(0.992188, 0.480469, 0.167969, 1.0),
    VBase4(0.550781, 0.824219, 0.324219, 1.0),
    VBase4(0.433594, 0.90625, 0.835938, 1.0),
    VBase4(0.347656, 0.820312, 0.953125, 1.0),
    # Girl clothes
    VBase4(0.96875, 0.691406, 0.699219, 1.0),  # (21) light pink 
    VBase4(0.996094, 0.957031, 0.597656, 1.0), # (22) light yellow
    VBase4(0.855469, 0.933594, 0.492188, 1.0), # (23) light yellow green
    VBase4(0.558594, 0.589844, 0.875, 1.0),    # (24) light purple
    VBase4(0.726562, 0.472656, 0.859375, 1.0), # (25) medium purple
    VBase4(0.898438, 0.617188, 0.90625, 1.0),  # (26) purple
    # Special
    VBase4(1.0, 1.0, 1.0, 1.0),                # (27) white
    # Pajama colors
    # Not using these colors yet, possibly for gloves
    VBase4(0.0, 0.2, 0.956862, 1.0),           # (28) Blue Banana Pajama
    VBase4(0.972549, 0.094117, 0.094117, 1.0), # (29) Red Horn Pajama
    VBase4(0.447058, 0.0, 0.901960, 1.0),      # (30) Purple Glasses Pajama
    ]

ShirtStyles = {
    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]
    # -------------------------------------------------------------------------
    # Boy styles
    # -------------------------------------------------------------------------
    # solid 
    'bss1' : [ 0, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # single stripe
    'bss2' : [ 1, 1, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # collar
    'bss3' : [ 2, 2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # double stripe
    'bss4' : [ 3, 3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # multiple stripes
    'bss5' : [ 4, 4, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # collar w/ pocket
    'bss6' : [ 5, 5, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # hawaiian
    'bss7' : [ 8, 8, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (8, 8), (9, 9), (11, 11), (12, 12), (27, 27) ]],
    # collar w/ 2 pockets
    'bss8' : [ 9, 9, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # bowling shirt
    'bss9' : [ 10, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # vest (special)
    'bss10' : [ 11, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # collar w/ ruffles
    'bss11' : [ 14, 10, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # soccer jersey (special)
    'bss12' : [ 16, 0, [(27, 27), (27, 4), (27, 5), (27, 6), (27, 7),
                    (27, 8), (27, 9)]],
    # lightning bolt (special)
    'bss13' : [ 17, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12) ]],
    # jersey 19 (special)
    'bss14' : [ 18, 12, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (8, 8), (9, 9), (11, 11), (12, 12), (27, 27) ]],
    # guayavera 
    'bss15' : [ 19, 13, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (27, 27) ]],
    # -------------------------------------------------------------------------
    # Girl styles
    # -------------------------------------------------------------------------
    # solid
    'gss1' : [ 0, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26),
                    (27, 27)]],
    # single stripe
    'gss2' : [ 1, 1, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # collar
    'gss3' : [ 2, 2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # double stripes
    'gss4' : [ 3, 3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # collar w/ pocket
    'gss5' : [ 5, 5, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # flower print
    'gss6' : [ 6, 6, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # flower trim (special)
    'gss7' : [ 7, 7, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # collar w/ 2 pockets
    'gss8' : [ 9, 9, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (11, 11), (12, 12), (21, 21),
                    (22, 22), (23, 23), (24, 24), (25, 25), (26, 26)]],
    # denim vest (special)
    'gss9' : [ 12, 0, [(27, 27)]],
    # peasant
    'gss10' : [ 13, 11, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), 
                    (26, 26) ]],
    # peasant w/ mid stripe
    'gss11' : [ 15, 11, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],
    # soccer jersey (special)
    'gss12' : [ 16, 0, [(27, 27), (27, 4), (27, 5), (27, 6), (27, 7),
                    (27, 8), (27, 9)]],
    # hearts
    'gss13' : [ 20, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],
    # stars (special)
    'gss14' : [ 21, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],
    # flower
    'gss15' : [ 22, 0, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
                    (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
                    (21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
                    (26, 26) ]],


    # Special Catalog-only shirts.
    
    # yellow hooded - Series 1
    'c_ss1' : [ 25, 16, [(27, 27),]],

    # yellow with palm tree - Series 1
    'c_ss2' : [ 27, 18, [(27, 27),]],

    # purple with stars - Series 2
    'c_ss3' : [ 38, 27, [(27, 27),]],

    # blue stripes (boys only) - Series 1
    'c_bss1' : [ 26, 17, [(27, 27),]],

    # orange (boys only) - Series 1
    'c_bss2' : [ 28, 19, [(27, 27),]],

    # lime green with stripe (boys only) - Series 2
    'c_bss3' : [ 37, 26, [(27, 27),]],

    # red kimono with checkerboard (boys only) - Series 2
    'c_bss4' : [ 39, 28, [(27, 27),]],

    # blue with yellow stripes (girls only) - Series 1
    'c_gss1' : [ 23, 14, [(27, 27), ]],
    
    # pink and beige with flower (girls only) - Series 1
    'c_gss2' : [ 24, 15, [(27, 27), ]],

    # Blue and gold with wavy stripes (girls only) - Series 2
    'c_gss3' : [ 35, 24, [(27, 27), ]],

    # Blue and pink with bow (girls only) - Series 2
    'c_gss4' : [ 36, 25, [(27, 27), ]],

    # Aqua kimono white stripe (girls only) - UNUSED
    'c_gss5' : [ 40, 29, [(27, 27), ]],

    # Tie dye shirt (boys and girls) - Series 3
    'c_ss4'  : [45, 34, [(27, 27), ]],

    # light blue with blue and white stripe (boys only) - Series 3
    'c_ss5' : [ 46, 35, [(27, 27), ]],

    # cowboy shirt 1-6 : Series 4
    'c_ss6' : [ 52, 41, [(27, 27), ]],
    'c_ss7' : [ 53, 42, [(27, 27), ]],
    'c_ss8' : [ 54, 43, [(27, 27), ]],
    'c_ss9' : [ 55, 44, [(27, 27), ]],
    'c_ss10' : [ 56, 45, [(27, 27), ]],
    'c_ss11' : [ 57, 46, [(27, 27), ]],
    
    # Special Holiday-themed shirts.

    # Halloween ghost
    'hw_ss1' : [ 29, 20, [(27, 27), ]],
    # Halloween pumpkin
    'hw_ss2' : [ 30, 21, [(27, 27), ]],

    'hw_ss3': [114, 101, [(27, 27)]],
    'hw_ss4': [115, 102, [(27, 27)]],
    'hw_ss5': [122, 109, [(27, 27)]],
    'hw_ss6': [123, 110, [(27, 27)]],
    'hw_ss7': [124, 111, [(27, 27)]],
    'hw_ss8': [125, 112, [(27, 27)]],
    'hw_ss9': [126, 113, [(27, 27)]],
    # Winter Holiday
    'wh_ss1' : [ 31, 22, [(27, 27), ]],
    # Winter Holiday
    'wh_ss2' : [ 32, 22, [(27, 27), ]],
    # Winter Holiday
    'wh_ss3' : [ 33, 23, [(27, 27), ]],
    # Winter Holiday
    'wh_ss4' : [ 34, 23, [(27, 27), ]],

    # Valentines day, pink with red hearts (girls)
    'vd_ss1' : [ 41, 30, [(27, 27), ]],
    # Valentines day, red with white hearts
    'vd_ss2' : [ 42, 31, [(27, 27), ]],
    # Valentines day, white with winged hearts (boys)
    'vd_ss3' : [ 43, 32, [(27, 27), ]],
    # Valentines day, pink with red flamed heart
    'vd_ss4' : [ 44, 33, [(27, 27), ]],
    # 2009 Valentines day, white with red cupid
    'vd_ss5' : [ 69, 58, [(27, 27), ]],
    # 2009 Valentines day, blue with green and red hearts
    'vd_ss6' : [ 70, 59, [(27, 27), ]],
    # 2010 Valentines day, red with white wings
    'vd_ss7' : [ 96, 85, [(27, 27), ]],
    # St Pat's Day, four leaf clover shirt
    'sd_ss1' : [ 47, 36, [(27, 27), ]],
    # St Pat's Day, pot o gold shirt
    'sd_ss2' : [ 48, 37, [(27, 27), ]],
    'sd_ss3': [116, 103, [(27, 27)]],

    # T-Shirt Contest, Fishing Vest
    'tc_ss1' : [ 49, 38, [(27, 27), ]],
    # T-Shirt Contest, Fish Bowl    
    'tc_ss2' : [ 50, 39, [(27, 27), ]],
    # T-Shirt Contest, Paw Print    
    'tc_ss3' : [ 51, 40, [(27, 27), ]],
    # T-Shirt Contest, Backpack
    'tc_ss4' : [ 62, 51, [(27, 27), ]],
    # T-Shirt Contest, Lederhosen    
    'tc_ss5' : [ 63, 52, [(27, 27), ]],
    # T-Shirt Contest, Watermelon    
    'tc_ss6' : [ 64, 53, [(27, 27), ]],
    # T-Shirt Contest, Race Shirt    
    'tc_ss7' : [ 65, 54, [(27, 27), ]],

    # July 4th, Flag
    'j4_ss1' : [ 58, 47, [(27, 27), ]],
    # July 4th, Fireworks
    'j4_ss2' : [ 59, 48, [(27, 27), ]],

    # Catalog series 7, Green w/ yellow buttons
    'c_ss12' : [ 60, 49, [(27, 27), ]], 

    # Catalog series 7, Purple w/ big flower
    'c_ss13' : [ 61, 50, [(27, 27), ]],
    
    # Pajama series
    'pj_ss1' : [66, 55, [(27, 27),]], # Blue Banana Pajama shirt
    'pj_ss2' : [67, 56, [(27, 27),]], # Red Horn Pajama shirt
    'pj_ss3' : [68, 57, [(27, 27),]], # Purple Glasses Pajama shirt
    
    # Special Award Clothes    
    'sa_ss1' : [ 71, 60, [(27, 27),]],
    'sa_ss2' : [ 72, 61, [(27, 27),]],
    'sa_ss3' : [ 73, 62, [(27, 27),]],
    'sa_ss4' : [ 74, 63, [(27, 27),]],
    'sa_ss5' : [ 75, 64, [(27, 27),]],
    'sa_ss6' : [ 76, 65, [(27, 27),]],
    'sa_ss7' : [ 77, 66, [(27, 27),]],
    'sa_ss8' : [ 78, 67, [(27, 27),]],
    'sa_ss9' : [ 79, 68, [(27, 27),]],
    'sa_ss10' : [ 80, 69, [(27, 27),]],
    'sa_ss11' : [ 81, 70, [(27, 27),]],
    'sa_ss12' : [ 82, 71, [(27, 27),]],
    'sa_ss13' : [ 83, 72, [(27, 27),]],
    'sa_ss14' : [ 84, 73, [(27, 27),]],
    'sa_ss15' : [ 85, 74, [(27, 27),]],
    'sa_ss16' : [ 86, 75, [(27, 27),]],
    'sa_ss17' : [ 87, 76, [(27, 27),]],
    'sa_ss18' : [ 88, 77, [(27, 27),]],
    'sa_ss19' : [ 89, 78, [(27, 27),]],
    'sa_ss20' : [ 90, 79, [(27, 27),]],
    'sa_ss21' : [ 91, 80, [(27, 27),]],
    'sa_ss22' : [ 92, 81, [(27, 27),]],
    'sa_ss23' : [ 93, 82, [(27, 27),]],
    'sa_ss24' : [ 94, 83, [(27, 27),]],
    'sa_ss25' : [ 95, 84, [(27, 27),]],
    'sa_ss26' : [ 106, 93, [(27, 27), ]], # Most Cogs Defeated Shirt
    'sa_ss27': [110, 97, [(27, 27)]],
    'sa_ss28': [111, 98, [(27, 27)]],
    'sa_ss29': [120, 107, [(27, 27)]],
    'sa_ss30': [121, 108, [(27, 27)]],
    'sa_ss31': [118, 105, [(27, 27)]],
    'sa_ss32': [127, 114, [(27, 27)]],
    'sa_ss33': [128, 115, [(27, 27)]],
    'sa_ss34': [129, 116, [(27, 27)]],
    'sa_ss35': [130, 117, [(27, 27)]],
    'sa_ss36': [131, 118, [(27, 27)]],
    'sa_ss37': [132, 119, [(27, 27)]],
    'sa_ss38': [133, 120, [(27, 27)]],
    'sa_ss39': [134, 121, [(27, 27)]],
    'sa_ss40': [135, 122, [(27, 27)]],
    'sa_ss41': [136, 123, [(27, 27)]],
    'sa_ss42': [137, 124, [(27, 27)]],
    'sa_ss43': [138, 125, [(27, 27)]],
    'sa_ss44': [139, 126, [(27, 27)]],
    'sa_ss45': [140, 127, [(27, 27)]],
    'sa_ss46': [141, 128, [(27, 27)]],
    'sa_ss47': [142, 129, [(27, 27)]],
    'sa_ss48': [143, 130, [(27, 27)]],
    'sa_ss49': [144, 116, [(27, 27)]],
    'sa_ss50': [145, 131, [(27, 27)]],
    'sa_ss51': [146, 133, [(27, 27)]],
    'sa_ss52': [147, 134, [(27, 27)]],
    'sa_ss53': [148, 135, [(27, 27)]],
    'sa_ss54': [149, 136, [(27, 27)]],
    'sa_ss55': [150, 137, [(27, 27)]],
    # Scientists
    'sc_1' : [ 97, 86, [(27, 27),]],
    'sc_2' : [ 98, 86, [(27, 27),]],
    'sc_3' : [ 99, 86, [(27, 27),]],
    
    # Silly Story Shirts
    'sil_1' : [ 100, 87, [(27, 27),]],   # Silly Mailbox Shirt
    'sil_2' : [ 101, 88, [(27, 27),]],   # Silly Trashcan Shirt
    'sil_3' : [ 102, 89, [(27, 27),]],   # Loony Labs Shirt
    'sil_4' : [ 103, 90, [(27, 27),]],   # Silly Hydrant Shirt
    'sil_5' : [ 104, 91, [(27, 27),]],   # Sillymeter Whistle Shirt
    'sil_6' : [ 105, 92, [(27, 27),]],   # Silly Cogbuster Shirt
    'sil_7' : [ 107, 94, [(27, 27),]],   # Victory Party Shirt 1
    'sil_8' : [ 108, 95, [(27, 27),]],   # Victory Party Shirt 2
    # name : [ shirtIdx, sleeveIdx, [(ShirtColorIdx, sleeveColorIdx), ... ]]

 'emb_us1': [103, 90, [(27, 27)]],
 'emb_us2': [100, 87, [(27, 27)]],
 'emb_us3': [101, 88, [(27, 27)]],
 'sb_1': [109, 96, [(27, 27)]],
 'jb_1': [112, 99, [(27, 27)]],
 'jb_2': [113, 100, [(27, 27)]],
 'ugcms': [117, 104, [(27, 27)]],
 'lb_1': [119, 106, [(27, 27)]]
 }


# If you add to this, please add to TTLocalizer.BottomStylesDescriptions
BottomStyles = {
    # name : [ bottomIdx, [bottomColorIdx, ...]]
    # -------------------------------------------------------------------------
    # Boy styles (shorts)
    # -------------------------------------------------------------------------
    # plain w/ pockets
    'bbs1' : [ 0, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # belt
    'bbs2' : [ 1, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # cargo
    'bbs3' : [ 2, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # hawaiian
    'bbs4' : [ 3, [0, 1, 2, 4, 6, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 
                                                                        27]],
    # side stripes (special)
    'bbs5' : [ 4, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                        20]],
    # soccer shorts
    'bbs6' : [ 5, [0, 1, 2, 4, 6, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20,
                                                                        27]],
    # side flames (special) 
    'bbs7' : [ 6, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                                                                   20, 27]],
    # denim
    'bbs8' : [ 7, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                                                                   20, 27]],
    # Valentines shorts
    'vd_bs1' : [ 8, [ 27, ]],
    # Green with red heart
    'vd_bs2' : [ 23, [ 27, ]],
    # Blue denim with green and red heart
    'vd_bs3' : [ 24, [ 27, ]],

    # Catalog only shorts
    # Orange with blue side stripes
    'c_bs1' : [ 9, [ 27, ]],
    
    # Blue with gold cuff stripes
    'c_bs2' : [ 10, [ 27, ]],

    # Green stripes - series 7
    'c_bs5' : [ 15, [ 27, ]],
    
    # St. Pats leprechaun shorts
    'sd_bs1' : [ 11, [27, ]],
    'sd_bs2': [44, [27]],

    # Pajama shorts
    'pj_bs1' : [ 16, [27, ]], # Blue Banana Pajama pants
    'pj_bs2' : [ 17, [27, ]], # Red Horn Pajama pants
    'pj_bs3' : [ 18, [27, ]], # Purple Glasses Pajama pants
    
    # Winter Holiday Shorts
    'wh_bs1' : [ 19, [27, ]], # Winter Holiday Shorts Style 1
    'wh_bs2' : [ 20, [27, ]], # Winter Holiday Shorts Style 2
    'wh_bs3' : [ 21, [27, ]], # Winter Holiday Shorts Style 3
    'wh_bs4' : [ 22, [27, ]], # Winter Holiday Shorts Style 4

   # Halloween Holiday Shorts
    'hw_bs1': [47, [27]],
    'hw_bs2': [48, [27]],
    'hw_bs5': [49, [27]],
    'hw_bs6': [50, [27]],
    'hw_bs7': [51, [27]],

    # -------------------------------------------------------------------------
    # Girl styles (shorts and skirts)
    # -------------------------------------------------------------------------
    # skirts
    # -------------------------------------------------------------------------
    # solid
    'gsk1' : [ 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],
    # polka dots (special)
    'gsk2' : [ 1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # vertical stripes
    'gsk3' : [ 2, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # horizontal stripe
    'gsk4' : [ 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # flower print
    'gsk5' : [ 4, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                        26]],
    # 2 pockets (special) 
    'gsk6' : [ 7, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                   26, 27]],
    # denim
    'gsk7' : [ 8, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                   26, 27]],
    
    # shorts
    # -------------------------------------------------------------------------
    # plain w/ pockets
    'gsh1' : [ 5, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],
    # flower
    'gsh2' : [ 6, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],
    # denim
    'gsh3' : [ 9, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25,
                                                                    26, 27]],

    # Special catalog-only skirts and shorts.

    # blue skirt with tan border and button
    'c_gsk1' : [ 10, [ 27, ]],

    # purple skirt with pink and ribbon
    'c_gsk2' : [ 11, [ 27, ]],
    
    # teal skirt with yellow and star
    'c_gsk3' : [ 12, [ 27, ]],

    # Valentines skirt (note, do not name with gsk, otherwise NPC might randomly get this skirt)
    # red skirt with hearts
    'vd_gs1' : [ 13, [ 27, ]],
    # Pink flair skirt with polka hearts
    'vd_gs2' : [ 27, [ 27, ]],
    # Blue denim skirt with green and red heart
    'vd_gs3' : [ 28, [ 27, ]],

    # rainbow skirt - Series 3
    'c_gsk4' : [ 14, [ 27, ]],

    # St. Pats day shorts
    'sd_gs1' : [ 15, [ 27, ]],
    'sd_gs2': [48, [27]],

    # Western skirts
    'c_gsk5' : [ 16, [ 27, ]],
    'c_gsk6' : [ 17, [ 27, ]],

    # Western shorts
    'c_bs3' : [ 12, [ 27, ]],
    'c_bs4' : [ 13, [ 27, ]],

    # July 4th shorts
    'j4_bs1' : [ 14, [ 27, ]],
    
    # July 4th Skirt
    'j4_gs1' : [ 18, [ 27, ]],    

    # Blue with flower - series 7
    'c_gsk7' : [ 19, [ 27, ]], 
    
    # pajama shorts
    'pj_gs1' : [ 20, [27, ]], # Blue Banana Pajama pants
    'pj_gs2' : [ 21, [27, ]], # Red Horn Pajama pants
    'pj_gs3' : [ 22, [27, ]], # Purple Glasses Pajama pants
    
    # Winter Holiday Skirts
    'wh_gsk1' : [ 23, [27, ]], # Winter Holiday Skirt Style 1
    'wh_gsk2' : [ 24, [27, ]], # Winter Holiday Skirt Style 2
    'wh_gsk3' : [ 25, [27, ]], # Winter Holiday Skirt Style 3
    'wh_gsk4' : [ 26, [27, ]], # Winter Holiday Skirt Style 4

    # Special award clothes
    'sa_bs1' : [25, [27, ]],
    'sa_bs2' : [26, [27, ]],
    'sa_bs3' : [27, [27, ]],
    'sa_bs4' : [28, [27, ]],
    'sa_bs5' : [29, [27, ]],
    'sa_bs6' : [30, [27, ]],
    'sa_bs7' : [31, [27, ]],
    'sa_bs8' : [32, [27, ]],
    'sa_bs9' : [33, [27, ]],
    'sa_bs10' : [34, [27, ]],    
    'sa_bs11' : [35, [27, ]],
    'sa_bs12' : [36, [27, ]],
    'sa_bs13': [41, [27]],
    'sa_bs14': [46, [27]],
    'sa_bs15': [45, [27]],
    'sa_bs16': [52, [27]],
    'sa_bs17': [53, [27]],
    'sa_bs18': [54, [27]],
    'sa_bs19': [55, [27]],
    'sa_bs20': [56, [27]],
    'sa_bs21': [57, [27]],   
    # Special award clothes
    'sa_gs1' : [29, [27, ]],
    'sa_gs2' : [30, [27, ]],
    'sa_gs3' : [31, [27, ]],
    'sa_gs4' : [32, [27, ]],
    'sa_gs5' : [33, [27, ]],
    'sa_gs6' : [34, [27, ]],
    'sa_gs7' : [35, [27, ]],
    'sa_gs8' : [36, [27, ]],
    'sa_gs9' : [37, [27, ]],
    'sa_gs10' : [38, [27, ]],
    'sa_gs11' : [39, [27, ]],
    'sa_gs12' : [40, [27, ]],
    'sa_gs13': [45, [27]],
    'sa_gs14': [50, [27]],
    'sa_gs15': [49, [27]],
    'sa_gs16': [57, [27]],
    'sa_gs17': [58, [27]],
    'sa_gs18': [59, [27]],
    'sa_gs19': [60, [27]],
    'sa_gs20': [61, [27]],
    'sa_gs21': [62, [27]],
    # Scientists
    'sc_bs1' : [37, [27, ]],
    'sc_bs2' : [38, [27, ]],
    'sc_bs3' : [39, [27, ]],
    
    'sc_gs1' : [41, [27, ]],
    'sc_gs2' : [42, [27, ]],
    'sc_gs3' : [43, [27, ]],
    
    'sil_bs1' : [ 40, [27, ]], # Silly Cogbuster Shorts
    'sil_gs1' : [44, [27, ]], # Silly Cogbuster Shorts
 'hw_bs3': [42, [27]],
 'hw_gs3': [46, [27]],
 'hw_bs4': [43, [27]],
 'hw_gs4': [47, [27]],
 'hw_gs1': [51, [27]],
 'hw_gs2': [52, [27]],
 'hw_gs5': [54, [27]],
 'hw_gs6': [55, [27]],
 'hw_gs7': [56, [27]],
 'hw_gsk1': [53, [27]]
    }

MAKE_A_TOON = 1
TAMMY_TAILOR = 2004 # TTC
LONGJOHN_LEROY = 1007 # DD
TAILOR_HARMONY = 4008 # MM
BONNIE_BLOSSOM = 5007 # DG
WARREN_BUNDLES = 3008 # TB
WORNOUT_WAYLON = 9010 # DDR

TailorCollections = {
    # TailorId : [ [ boyShirts ], [ girlShirts ], [boyShorts], [girlBottoms] ]
    MAKE_A_TOON : [ ['bss1', 'bss2'],
                    ['gss1', 'gss2'],
                    ['bbs1', 'bbs2'],
                    ['gsk1', 'gsh1'] ],
    TAMMY_TAILOR : [ ['bss1', 'bss2'],
                     ['gss1', 'gss2'],
                     ['bbs1', 'bbs2'],
                     ['gsk1', 'gsh1'] ],
    LONGJOHN_LEROY : [ ['bss3', 'bss4', 'bss14'], ['gss3', 'gss4', 'gss14'], ['bbs3', 'bbs4'], ['gsk2', 'gsh2'] ],
    TAILOR_HARMONY : [ ['bss5', 'bss6', 'bss10'], ['gss5', 'gss6', 'gss9'], ['bbs5'], ['gsk3', 'gsh3'] ],
    BONNIE_BLOSSOM : [ ['bss7', 'bss8', 'bss12'], ['gss8', 'gss10', 'gss12'], ['bbs6'], ['gsk4', 'gsk5'] ],
    WARREN_BUNDLES : [ ['bss9','bss13'], ['gss7', 'gss11'], ['bbs7'], ['gsk6'] ],
    WORNOUT_WAYLON : [ ['bss11', 'bss15'], ['gss13', 'gss15'], ['bbs8'], ['gsk7'] ],
    }

BOY_SHIRTS = 0
GIRL_SHIRTS = 1
BOY_SHORTS = 2
GIRL_BOTTOMS = 3
HAT = 1
GLASSES = 2
BACKPACK = 4
SHOES = 8

MakeAToonBoyBottoms = []
MakeAToonBoyShirts = []
MakeAToonGirlBottoms = []
MakeAToonGirlShirts = []
MakeAToonGirlSkirts = []
MakeAToonGirlShorts = []
for style in TailorCollections[MAKE_A_TOON][BOY_SHORTS]:
    index = BottomStyles[style][0]
    MakeAToonBoyBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][BOY_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonBoyShirts.append(index)

for style in TailorCollections[MAKE_A_TOON][GIRL_BOTTOMS]:
    index = BottomStyles[style][0]
    MakeAToonGirlBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][GIRL_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonGirlShirts.append(index)

for index in MakeAToonGirlBottoms:
    flag = GirlBottoms[index][1]
    if flag == SKIRT:
        MakeAToonGirlSkirts.append(index)
    elif flag == SHORTS:
        MakeAToonGirlShorts.append(index)
    else:
        notify.error('Invalid flag')

def getRandomTop(gender, tailorId = MAKE_A_TOON, generator = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        topStyle = generator.choice(collection[BOY_SHIRTS])
    else:
        topStyle = generator.choice(collection[GIRL_SHIRTS])
    styleList = ShirtStyles[topStyle]
    colors = generator.choice(styleList[2])
    return (styleList[0],
     colors[0],
     styleList[1],
     colors[1])
def getRandomBottom(gender, tailorId = MAKE_A_TOON, generator = None, girlBottomType = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        bottomStyle = generator.choice(collection[BOY_SHORTS])
    elif girlBottomType is None:
        bottomStyle = generator.choice(collection[GIRL_BOTTOMS])
    elif girlBottomType == SKIRT:
        skirtCollection = [style for style in collection[GIRL_BOTTOMS] if GirlBottoms[BottomStyles[style][0]][1] == SKIRT]
        bottomStyle = generator.choice(skirtCollection)
    elif girlBottomType == SHORTS:
        shortsCollection = [style for style in collection[GIRL_BOTTOMS] if GirlBottoms[BottomStyles[style][0]][1] == SHORTS]
        bottomStyle = generator.choice(shortsCollection)
    else:
        bottomStyle = None
        notify.error(f'Bad girlBottomType: {girlBottomType}')
    styleList = BottomStyles[bottomStyle]
    color = generator.choice(styleList[1])
    return (styleList[0], color)


def getRandomGirlBottom(type):
    bottoms = []
    bottomIndex = 0
    for bottom in GirlBottoms:
        if bottom[1] == type:
            bottoms.append(bottomIndex)
        bottomIndex += 1
    return random.choice(bottoms)
def getRandomGirlBottomAndColor(type):
    bottoms = []
    if type == SHORTS:
        typeStr = 'gsh'
    else:
        typeStr = 'gsk'
    for bottom in BottomStyles.keys():
        if bottom.find(typeStr) >= 0:
            bottoms.append(bottom)

    style = BottomStyles[random.choice(bottoms)]
    return (style[0], random.choice(style[1]))


def getRandomizedTops(gender, tailorId = MAKE_A_TOON, generator = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        collection = collection[BOY_SHIRTS][:]
    else:
        collection = collection[GIRL_SHIRTS][:]
    tops = []
    random.shuffle(collection)
    for style in collection:
        colors = ShirtStyles[style][2][:]
        random.shuffle(colors)
        for color in colors:
            tops.append((ShirtStyles[style][0],
             color[0],
             ShirtStyles[style][1],
             color[1]))

    return tops


def getRandomizedBottoms(gender, tailorId = MAKE_A_TOON, generator = None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        collection = collection[BOY_SHORTS][:]
    else:
        collection = collection[GIRL_BOTTOMS][:]
    bottoms = []
    random.shuffle(collection)
    for style in collection:
        colors = BottomStyles[style][1][:]
        random.shuffle(colors)
        for color in colors:
            bottoms.append((BottomStyles[style][0], color))

    return bottoms


def getTops(gender, tailorId = MAKE_A_TOON):
    if gender == 'm':
        collection = TailorCollections[tailorId][BOY_SHIRTS]
    else:
        collection = TailorCollections[tailorId][GIRL_SHIRTS]
    tops = []
    for style in collection:
        for color in ShirtStyles[style][2]:
            tops.append((ShirtStyles[style][0],
             color[0],
             ShirtStyles[style][1],
             color[1]))

    return tops


def getAllTops(gender):
    tops = []
    for topStyle in ShirtStyles.keys():
        if gender == 'm':
            if topStyle[0] == 'g' or topStyle[:3] == 'c_g':
                continue
        elif topStyle[0] == 'b' or topStyle[:3] == 'c_b':
            continue
        for color in ShirtStyles[topStyle][2]:
            tops.append((ShirtStyles[style][0],
             color[0],
             ShirtStyles[topStyle][1],
             color[1]))

    return tops


def getBottoms(gender, tailorId = MAKE_A_TOON):
    if gender == 'm':
        collection = TailorCollections[tailorId][BOY_SHORTS]
    else:
        collection = TailorCollections[tailorId][GIRL_BOTTOMS]
    bottoms = []
    for bottomStyle in collection:
        for color in BottomStyles[bottomStyle][1]:
            bottoms.append((BottomStyles[bottomStyle][0], color))

    return bottoms


def getAllBottoms(gender, output = 'both'):
    bottoms = []
    for bottomStyle in BottomStyles.keys():
        if gender == 'm':
            if bottomStyle[0] == 'g' or bottomStyle[:3] == 'c_g' or bottomStyle[:4] == 'vd_g' or bottomStyle[:4] == 'sd_g' or bottomStyle[:4] == 'j4_g' or bottomStyle[:4] == 'pj_g' or bottomStyle[:4] == 'wh_g' or bottomStyle[:4] == 'sa_g' or bottomStyle[:4] == 'sc_g' or bottomStyle[:5] == 'sil_g' or bottomStyle[:4] == 'hw_g':
                continue
        elif bottomStyle[0] == 'b' or bottomStyle[:3] == 'c_b' or bottomStyle[:4] == 'vd_b' or bottomStyle[:4] == 'sd_b' or bottomStyle[:4] == 'j4_b' or bottomStyle[:4] == 'pj_b' or bottomStyle[:4] == 'wh_b' or bottomStyle[:4] == 'sa_b' or bottomStyle[:4] == 'sc_b' or bottomStyle[:5] == 'sil_b' or bottomStyle[:4] == 'hw_b':
            continue
        bottomIdx = BottomStyles[bottomStyle][0]
        if gender == 'f':
            textureType = GirlBottoms[bottomIdx][1]
        else:
            textureType = SHORTS
        if output == 'both' or output == 'skirts' and textureType == SKIRT or output == 'shorts' and textureType == SHORTS:
            for color in BottomStyles[bottomStyle][1]:
                bottoms.append((bottomIdx, color))

    return bottoms

allColorsList = [VBase4(1.0, 1.0, 1.0, 1.0), # 0, White
 VBase4(0.96875, 0.691406, 0.699219, 1.0),   # 1, Peach 
 VBase4(0.933594, 0.265625, 0.28125, 1.0),   # 2, Bright Red 
 VBase4(0.863281, 0.40625, 0.417969, 1.0),   # 3, Red
 VBase4(0.710938, 0.234375, 0.4375, 1.0),    # 4, Maroon
 VBase4(0.570312, 0.449219, 0.164062, 1.0),  # 5, Sienna
 VBase4(0.640625, 0.355469, 0.269531, 1.0),  # 6, Brown
 VBase4(0.996094, 0.695312, 0.511719, 1.0),  # 7, Tan  
 VBase4(0.832031, 0.5, 0.296875, 1.0),       # 8, Coral
 VBase4(0.992188, 0.480469, 0.167969, 1.0),  # 9, Orange
 VBase4(0.996094, 0.898438, 0.320312, 1.0),  # 10, Yellow
 VBase4(0.996094, 0.957031, 0.597656, 1.0),  # 11, Cream
 VBase4(0.855469, 0.933594, 0.492188, 1.0),  # 12, Citrine
 VBase4(0.550781, 0.824219, 0.324219, 1.0),  # 13, Lime
 VBase4(0.242188, 0.742188, 0.515625, 1.0),  # 14, Sea Green
 VBase4(0.304688, 0.96875, 0.402344, 1.0),   # 15, Green
 VBase4(0.433594, 0.90625, 0.835938, 1.0),   # 16, Light Blue
 VBase4(0.347656, 0.820312, 0.953125, 1.0),  # 17, Aqua
 VBase4(0.191406, 0.5625, 0.773438, 1.0),    # 18, Blue
 VBase4(0.558594, 0.589844, 0.875, 1.0),     # 19, Periwinkle
 VBase4(0.285156, 0.328125, 0.726562, 1.0),  # 20, Royal Blue
 VBase4(0.460938, 0.378906, 0.824219, 1.0),  # 21, Slate Blue
 VBase4(0.546875, 0.28125, 0.75, 1.0),       # 22, Purple
 VBase4(0.726562, 0.472656, 0.859375, 1.0),  # 23, Lavender
 VBase4(0.898438, 0.617188, 0.90625, 1.0),   # 24, Pink
 VBase4(0.7, 0.7, 0.8, 1.0),                 # 25, Plum
 VBase4(0.3, 0.3, 0.35, 1.0),                # 26, Black
 ########################### TTR COLORS #################################
 VBase4(0.891, 0.439, 0.698, 1.0),           # 27, Rose Pink
 VBase4(0.741, 0.873, 0.957, 1.0),           # 28, Ice Blue
 VBase4(0.641, 0.857, 0.673, 1.0),           # 29, Mint Green
 VBase4(0.039, 0.862, 0.654, 1.0),           # 30, Emerald
 VBase4(0.196, 0.725, 0.714, 1.0),           # 31, Teal
 VBase4(0.984, 0.537, 0.396, 1.0),           # 32, Apricot
 VBase4(0.968, 0.749, 0.349, 1.0),           # 33, Amber
 VBase4(0.658, 0.175, 0.258, 1.0),           # 34, Crimson
 VBase4(0.411, 0.644, 0.282, 1.0),           # 35, Dark Green
 VBase4(0.325, 0.407, 0.601, 1.0),           # 36, Steel Blue
 VBase4(0.235, 0.573, 0.984, 1.0),           # 37, Toonfest Blue
 ########################## TTPA / TTCC COLORS ##########################
 VBase4(0.0, 0.635294, 0.258823, 1.0),       # 38, Mountain Green
 VBase4(0.674509, 0.925490, 1.0, 1.0),       # 39, Icy Blue
 VBase4(0.988235, 0.894117, 0.745098, 1.0),  # 40, Desert Sand
 VBase4(0.749019, 1.0, 0.847058, 1.0),       # 41, Mint
 VBase4(0.470588, 0.443137, 0.447058, 1.0),  # 42, Charcoal
 VBase4(0.996078, 0.254901, 0.392156, 1.0),  # 43, Hot Pink
 VBase4(0.811764, 0.709803, 0.231372, 1.0),  # 44, Honey Mustard
 VBase4(0.749019, 0.756862, 0.760784, 1.0),  # 45, Gray
 VBase4(1.0, 0.639215, 0.262745, 1.0),       # 46, Neon Orange
 VBase4(0.0, 0.403921, 0.647058, 1.0),       # 47, Sapphire
 VBase4(0.862745, 0.078431, 0.235294, 1.0),  # 48, Bright Crimson
 VBase4(0.0, 0.635294, 0.513725, 1.0),       # 49, Gamma Emerald
 VBase4(0.803921, 0.498039, 0.196078, 1.0),  # 50, Bronze
 VBase4(0.70, 0.52, 0.75, 1.0),              # 51, African Violet
 VBase4(1.0, 0, 1.0, 1.0),                   # 52, Neon Pink
 VBase4(0.5764, 0.4392, 0.8588, 1.0),        # 53, Medium Purple
 VBase4(1.0, 1.0, 0.94117, 1.0),             # 54, Ivory
 VBase4(0.9333, 0.8235, 0.9333, 1.0),        # 55, Thistle
 VBase4(0.0, 1.0, 0.4980, 1.0),              # 56, Spring Green
 VBase4(0.8549, 0.6470, 0.1254, 1.0),        # 57, Goldenrod
 VBase4(1.0, 0.59607, 0.0705, 1.0),          # 58, Cadium Yellow
 VBase4(0.8039, 0.6862, 0.5843, 1.0),        # 59, Peach Puff
 VBase4(0.2196, 0.5568, 0.5568, 1.0),        # 60, Toony Teal
 VBase4(0.7764, 0.4431, 0.4431, 1.0),        # 61, Salmon
 VBase4(0.8901, 0.8117, 0.3411, 1.0),        # 62, Banana Yellow
 VBase4(0.4117, 0.4117, 0.4117, 1.0),        # 63, Dim Gray
 VBase4(1.0, 0.8431, 0.0, 1.0),              # 64, Radiant Yellow
 VBase4(0.9333, 0.7882, 0.0, 1.0),           # 65, Gold
########################### USER DEFINED COLORS #########################
 VBase4(0.37, 0.3, 0.65, 1.0),               # 66, Spooky Purple
 VBase4(0.62, 0.14, 0.14, 1.0),              # 67, Doppler Crimson
 VBase4(0.34, 0.51, 0.86, 1.0),              # 68, Lapis Blue
 VBase4(0.25, 0.28, 0.5, 1.0),               # 69, Abyssopelagic Blue
 VBase4(0.2627, 0.1686, 0.5, 1.0),           # 70, Very Spooky Purple
 ]
 
 
### TT-CL COLORS ###
"""
 VBase4(0.372549, 0, 0, 1.0),
 VBase4(1.0, 0.760784, 0.454901, 1.0),
 VBase4(0.278431, 0.0, 1.0, 1.0),
 VBase4(0.870588, 1.0, 0.988235, 1.0),
 VBase4(0.764705, 1.0, 0.745098, 1.0),
 VBase4(1.0, 0.878431, 0.878431, 1.0),
 VBase4(0.745098, 0.792156, 1.0, 1.0),
 VBase4(1.0, 0.168627, 0.0, 1.0),
 VBase4(1.0, 1.0, 0.0, 1.0),
 VBase4(1.0, 0.0, 1.0, 1.0),
 VBase4(0.847058, 0.847058, 0.847058, 0.2),
 VBase4(0.891, 0.439, 0.698, 1.0),
 VBase4(0.741, 0.873, 0.957, 1.0),
 VBase4(0.641, 0.857, 0.673, 1.0),
 VBase4(0.039, 0.862, 0.654, 1.0),
 VBase4(0.196, 0.725, 0.714, 1.0),
 VBase4(0.984, 0.537, 0.396, 1.0),
 VBase4(0.968, 0.749, 0.349, 1.0),
 VBase4(0.658, 0.175, 0.258, 1.0),
 VBase4(0.411, 0.644, 0.282, 1.0),
 VBase4(0.325, 0.407, 0.601, 1.0),
 VBase4(0.235, 0.573, 0.984, 1.0),
 VBase4(0.0, 0.635294, 0.258823, 1.0),
 VBase4(0.674509, 0.92549, 1.0, 1.0),
 VBase4(0.988235, 0.894117, 0.745098, 1.0),
 VBase4(0.749019, 1.0, 0.847058, 1.0),
 VBase4(0.470588, 0.443137, 0.447058, 1.0),
 VBase4(0.996078, 0.254901, 0.392156, 1.0),
 VBase4(0.811764, 0.709803, 0.231372, 1.0),
 VBase4(0.749019, 0.756862, 0.760784, 1.0),
 VBase4(1.0, 0.639215, 0.262745, 1.0),
 VBase4(0.0, 0.403921, 0.647058, 1.0),
 VBase4(0.862745, 0.078431, 0.235294, 1.0),
 VBase4(0.0, 0.635294, 0.513725, 1.0),
 VBase4(0.803921, 0.498039, 0.196078, 1.0),
 VBase4(0.7, 0.52, 0.75, 1.0),
 VBase4(1.0, 0, 1.0, 1.0),
 VBase4(0.5764, 0.4392, 0.8588, 1.0),
 VBase4(1.0, 1.0, 0.94117, 1.0),
 VBase4(0.9333, 0.8235, 0.9333, 1.0),
 VBase4(0.0, 1.0, 0.498, 1.0),
 VBase4(0.8549, 0.647, 0.1254, 1.0),
 VBase4(1.0, 0.59607, 0.0705, 1.0),
 VBase4(0.8039, 0.6862, 0.5843, 1.0),
 VBase4(0.2196, 0.5568, 0.5568, 1.0),
 VBase4(0.7764, 0.4431, 0.4431, 1.0),
 VBase4(0.8901, 0.8117, 0.3411, 1.0),
 VBase4(0.4117, 0.4117, 0.4117, 1.0),
 VBase4(0.54118, 0.74902, 0.89804, 1.0),
 VBase4(1.0, 0.8431, 0.0, 1.0),
 VBase4(0.37, 0.3, 0.65, 1.0),]
 """
 
defaultBoyColorList = [x for x in range(0, len(allColorsList))]
defaultGirlColorList = [x for x in range(0, len(allColorsList))]
allColorsListApproximations = [VBase4(round(x[0], 3), round(x[1], 3), round(x[2], 3), round(x[3], 3)) for x in allColorsList]
allowedColors = set([allColorsListApproximations[x] for x in set(defaultBoyColorList + defaultGirlColorList + [26])])
HatModels = [None,
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_baseball',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_safari',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_ribbon',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_heart',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_topHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_anvil',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_flowerPot',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sandbag',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_weight',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fez',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_golfHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_partyHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pillBox',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_crown',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_cowboyHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pirateHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_propellerHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fishingHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sombreroHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_strawHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sunHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_antenna',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_beeHiveHairdo',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bowler',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_chefsHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_detective',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_feathers',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fedora',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_mickeysBandConductorHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_nativeAmericanFeather',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pompadorHairdo',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_princess',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_robinHoodHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_romanHelmet',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_spiderAntennaThingy',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_tiara',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_vikingHelmet',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_witch',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_wizard',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_conquistadorHelmet',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_firefighterHelmet',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_foilPyramid',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_minersHardhatWithLight',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_napoleonHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pilotsCap',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_policeHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_rainbowAfroWig',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sailorHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_carmenMirandaFruitHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bobbyHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_jugheadHat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_winter',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bandana',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_dinosaur',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_band',
 'phase_4/models/accessories/tt_m_chr_avt_acc_hat_birdNest']
HatTextures = [None,
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_heartYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_topHatBlue.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_safariBrown.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_safariGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballBlue.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballOrange.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonChecker.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonLtRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonRainbow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballTeal.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonPinkDots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_baseballPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonCheckerGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_hat_partyToon.jpg']
GlassesModels = [None,
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_roundGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_miniblinds',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_narrowGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_starGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_3dGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_aviator',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_catEyeGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_dorkGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_jackieOShades',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_scubaMask',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_goggles',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_grouchoMarxEyebrow',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_heartGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_insectEyeGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_masqueradeTypeMask',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_masqueradeTypeMask3',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_monocle',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_mouthGlasses',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_squareRims',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_eyepatch',
 'phase_4/models/accessories/tt_m_chr_avt_acc_msk_alienGlasses']
GlassesTextures = [None,
 'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask2.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask4.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask5.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_msk_eyepatchGems.jpg']
BackpackModels = [None,
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_backpack',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_batWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_beeWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dragonFlyWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_scubaTank',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_sharkFin',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_angelWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_backpackWithToys',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_butterflyWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dragonWing',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_jetPack',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_spiderLegs',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackA',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_birdWings',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackCat',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackDog',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_airplane',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_woodenSword',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_supertoonCape',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_vampireCape',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dinosaurTail',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_band',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_gags',
 'phase_4/models/accessories/tt_m_chr_avt_acc_pac_flunky']
BackpackTextures = [None,
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackOrange.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPolkaDotRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPolkaDotYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_angelWingsMultiColor.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_pac_butterflyWingsStyle2.jpg']
ShoesModels = ['feet',
 'shoes',
 'boots_short',
 'boots_long']
ShoesTextures = ['phase_3/maps/tt_t_chr_avt_acc_sho_athleticGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_athleticRed.jpg',
 'phase_3/maps/tt_t_chr_avt_acc_sho_docMartinBootsGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_wingtips.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoes.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_deckShoes.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_athleticYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleBlack.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleWhite.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStylePink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_cowboyBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakers.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesBrown.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_superToonRedBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesGreen.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleRed.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsAqua.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsBrown.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsBlueSquares.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreenHearts.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreyDots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsOrangeStars.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPinkStars.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_loafers.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_motorcycleBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_oxfords.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_santaBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsBeige.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_workBoots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakersPink.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsRedDots.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPurple.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesViolet.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsBlue.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellow.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_athleticBlack.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_pirate.jpg',
 'phase_4/maps/tt_t_chr_avt_acc_sho_dinosaur.jpg']
HatStyles = {'none': [0, 0, 0],
 'hbb1': [1, 0, 0],
 'hsf1': [2, 0, 0],
 'hsf2': [2, 5, 0],
 'hsf3': [2, 6, 0],
 'hht1': [4, 0, 0],
 'hht2': [4, 3, 0],
 'htp1': [5, 0, 0],
 'htp2': [5, 4, 0],
 'hav1': [6, 0, 0],
 'hfp1': [7, 0, 0],
 'hsg1': [8, 0, 0],
 'hwt1': [9, 0, 0],
 'hfz1': [10, 0, 0],
 'hgf1': [11, 0, 0],
 'hpt1': [12, 0, 0],
 'hpt2': [12, 19, 0],
 'hpb1': [13, 0, 0],
 'hcr1': [14, 0, 0],
 'hbb2': [1, 7, 0],
 'hbb3': [1, 8, 0],
 'hcw1': [15, 0, 0],
 'hpr1': [16, 0, 0],
 'hpp1': [17, 0, 0],
 'hfs1': [18, 0, 0],
 'hsb1': [19, 0, 0],
 'hst1': [20, 0, 0],
 'hat1': [22, 0, 0],
 'hhd1': [23, 0, 0],
 'hbw1': [24, 0, 0],
 'hch1': [25, 0, 0],
 'hdt1': [26, 0, 0],
 'hft1': [27, 0, 0],
 'hfd1': [28, 0, 0],
 'hmk1': [29, 0, 0],
 'hft2': [30, 0, 0],
 'hhd2': [31, 0, 0],
 'hrh1': [33, 0, 0],
 'hhm1': [34, 0, 0],
 'hat2': [35, 0, 0],
 'htr1': [36, 0, 0],
 'hhm2': [37, 0, 0],
 'hwz1': [38, 0, 0],
 'hwz2': [39, 0, 0],
 'hhm3': [40, 0, 0],
 'hhm4': [41, 0, 0],
 'hfp2': [42, 0, 0],
 'hhm5': [43, 0, 0],
 'hnp1': [44, 0, 0],
 'hpc2': [45, 0, 0],
 'hph1': [46, 0, 0],
 'hwg1': [47, 0, 0],
 'hbb4': [1, 13, 0],
 'hbb5': [1, 14, 0],
 'hbb6': [1, 15, 0],
 'hsl1': [48, 0, 0],
 'hfr1': [49, 0, 0],
 'hby1': [50, 0, 0],
 'hjh1': [51, 0, 0],
 'hbb7': [1, 17, 0],
 'hwt2': [52, 0, 0],
 'hhw2': [54, 0, 0],
 'hob1': [55, 0, 0],
 'hbn1': [56, 0, 0],
 'hrb1': [3, 0, 0],
 'hrb2': [3, 1, 0],
 'hrb3': [3, 2, 0],
 'hsu1': [21, 0, 0],
 'hrb4': [3, 9, 0],
 'hrb5': [3, 10, 0],
 'hrb6': [3, 11, 0],
 'hrb7': [3, 12, 0],
 'hpc1': [32, 0, 0],
 'hrb8': [3, 16, 0],
 'hrb9': [3, 18, 0],
 'hhw1': [53, 0, 0]}
GlassesStyles = {'none': [0, 0, 0],
 'grd1': [1, 0, 0],
 'gmb1': [2, 0, 0],
 'gnr1': [3, 0, 0],
 'gst1': [4, 0, 0],
 'g3d1': [5, 0, 0],
 'gav1': [6, 0, 0],
 'gjo1': [9, 0, 0],
 'gsb1': [10, 0, 0],
 'ggl1': [11, 0, 0],
 'ggm1': [12, 0, 0],
 'ghg1': [13, 0, 0],
 'gie1': [14, 0, 0],
 'gmt1': [15, 0, 0],
 'gmt2': [15, 1, 0],
 'gmt3': [16, 0, 0],
 'gmt4': [16, 2, 0],
 'gmt5': [16, 3, 0],
 'gmn1': [17, 0, 0],
 'gmo1': [18, 0, 0],
 'gsr1': [19, 0, 0],
 'gce1': [7, 0, 0],
 'gdk1': [8, 0, 0],
 'gag1': [21, 0, 0],
 'ghw1': [20, 0, 0],
 'ghw2': [20, 4, 0]}
BackpackStyles = {'none': [0, 0, 0],
 'bpb1': [1, 0, 0],
 'bpb2': [1, 1, 0],
 'bpb3': [1, 2, 0],
 'bpd1': [1, 3, 0],
 'bpd2': [1, 4, 0],
 'bwg1': [2, 0, 0],
 'bwg2': [3, 0, 0],
 'bwg3': [4, 0, 0],
 'bst1': [5, 0, 0],
 'bfn1': [6, 0, 0],
 'baw1': [7, 0, 0],
 'baw2': [7, 5, 0],
 'bwt1': [8, 0, 0],
 'bwg4': [9, 0, 0],
 'bwg5': [9, 6, 0],
 'bwg6': [10, 0, 0],
 'bjp1': [11, 0, 0],
 'blg1': [12, 0, 0],
 'bsa1': [13, 0, 0],
 'bwg7': [14, 0, 0],
 'bsa2': [15, 0, 0],
 'bsa3': [16, 0, 0],
 'bap1': [17, 0, 0],
 'bhw1': [18, 0, 0],
 'bhw2': [19, 0, 0],
 'bhw3': [20, 0, 0],
 'bhw4': [21, 0, 0],
 'bob1': [22, 0, 0],
 'bfg1': [23, 0, 0],
 'bfl1': [24, 0, 0]}
ShoesStyles = {'none': [0, 0, 0],
 'sat1': [1, 0, 0],
 'sat2': [1, 1, 0],
 'smb1': [3, 2, 0],
 'scs1': [2, 3, 0],
 'sdk1': [1, 6, 0],
 'sat3': [1, 7, 0],
 'scs2': [2, 8, 0],
 'scs3': [2, 9, 0],
 'scs4': [2, 10, 0],
 'scb1': [3, 11, 0],
 'sht1': [2, 13, 0],
 'ssb1': [3, 16, 0],
 'sts1': [1, 17, 0],
 'sts2': [1, 18, 0],
 'scs5': [2, 19, 0],
 'smb2': [3, 20, 0],
 'smb3': [3, 21, 0],
 'smb4': [3, 22, 0],
 'slf1': [1, 28, 0],
 'smt1': [3, 30, 0],
 'sox1': [1, 31, 0],
 'srb1': [3, 32, 0],
 'sst1': [3, 33, 0],
 'swb1': [3, 34, 0],
 'swb2': [3, 35, 0],
 'swk1': [2, 36, 0],
 'scs6': [2, 37, 0],
 'smb5': [3, 38, 0],
 'sht2': [2, 39, 0],
 'srb2': [3, 40, 0],
 'sts3': [1, 41, 0],
 'sts4': [1, 42, 0],
 'sts5': [1, 43, 0],
 'srb3': [3, 44, 0],
 'srb4': [3, 45, 0],
 'sat4': [1, 46, 0],
 'shw1': [3, 47, 0],
 'shw2': [3, 48, 0],
 'swt1': [1, 4, 0],
 'smj1': [2, 5, 0],
 'sfb1': [3, 12, 0],
 'smj2': [2, 14, 0],
 'smj3': [2, 15, 0],
 'sfb2': [3, 23, 0],
 'sfb3': [3, 24, 0],
 'sfb4': [3, 25, 0],
 'sfb5': [3, 26, 0],
 'sfb6': [3, 27, 0],
 'smj4': [2, 29, 0]}

def isValidHat(itemIdx, textureIdx, colorIdx):
    for style in list(HatStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidGlasses(itemIdx, textureIdx, colorIdx):
    for style in list(GlassesStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidBackpack(itemIdx, textureIdx, colorIdx):
    for style in list(BackpackStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidShoes(itemIdx, textureIdx, colorIdx):
    for style in list(ShoesStyles.values()):
        if itemIdx == style[0] and textureIdx == style[1] and colorIdx == style[2]:
            return True

    return False


def isValidAccessory(itemIdx, textureIdx, colorIdx, which):
    if which == HAT:
        return isValidHat(itemIdx, textureIdx, colorIdx)
    elif which == GLASSES:
        return isValidGlasses(itemIdx, textureIdx, colorIdx)
    elif which == BACKPACK:
        return isValidBackpack(itemIdx, textureIdx, colorIdx)
    elif which == SHOES:
        return isValidShoes(itemIdx, textureIdx, colorIdx)
    else:
        return False
        
class ToonDNA(BytestringParser, version=1):
    head = Packers.string
    torso = Packers.string
    legs = Packers.string
    gender = Packers.string
    topTex = Packers.uint8
    topTexColor = Packers.uint8
    sleeveTex = Packers.uint8
    sleeveTexColor = Packers.uint8
    botTex = Packers.uint8
    botTexColor = Packers.uint8
    armColor = Packers.uint8
    gloveColor = Packers.uint8
    legColor = Packers.uint8
    headColor = Packers.uint8

    def __init__(self, head='dls', torso='m', legs='m', gender='m', topTex=0, 
                 topTexColor=0, sleeveTex=0, sleeveTexColor=0, botTex=0, 
                 botTexColor=0, armColor=0, gloveColor=0, legColor=0, 
                 headColor=0):
        self.cache = ()
        super().__init__(head, torso, legs, gender, topTex, 
                         topTexColor, sleeveTex, sleeveTexColor, botTex,
                         botTexColor, armColor, gloveColor, legColor, headColor)
        
    def __str__(self):
        string = ''
        string += f'gender = {self.gender}\n'
        string += f'head = {self.head}, torso = {self.torso}, legs = {self.legs}\n'
        string += f'arm color = {self.armColor}\n'
        string += f'glove color = {self.gloveColor}\n'
        string += f'leg color = {self.legColor}\n'
        string += f'head color = {self.headColor}\n'
        string += f'top texture = {self.topTex}\n'
        string += f'top texture color = {self.topTexColor}\n'
        string += f'sleeve texture = {self.sleeveTex}\n'
        string += f'sleeve texture color = {self.sleeveTexColor}\n'
        string += f'bottom texture = {self.botTex}\n'
        string += f'bottom texture color = {self.botTexColor}'
        return string

    def clone(self):
        """
        Returns a new ToonDNA object with the same values as the current one.
        """
        return ToonDNA(
            head=self.head,
            torso=self.torso,
            legs=self.legs,
            gender=self.gender,
            topTex=self.topTex,
            topTexColor=self.topTexColor,
            sleeveTex=self.sleeveTex,
            sleeveTexColor=self.sleeveTexColor,
            botTex=self.botTex,
            botTexColor=self.botTexColor,
            armColor=self.armColor,
            gloveColor=self.gloveColor,
            legColor=self.legColor,
            headColor=self.headColor
        )

    def newToonRandom(self, seed=None, gender='m', npc=0, stage=None):
        if seed:
            generator = random.Random()
            generator.seed(seed)
        else:
            generator = random
        
        self.legs = generator.choice(toonLegTypes + ["m", "l", "l", "l"])
        self.gender = gender

        if not npc:
            if (stage == MAKE_A_TOON):
                if not base.cr.isPaid():
                    animalIndicesToUse = allToonHeadAnimalIndicesTrial
                else:
                    animalIndicesToUse = allToonHeadAnimalIndices
                animal = generator.choice(animalIndicesToUse)
                self.head = toonHeadTypes[animal]
            else:
                self.head = generator.choice(toonHeadTypes)
        else:
            self.head = generator.choice(toonHeadTypes[:22])
        top, topColor, sleeve, sleeveColor = getRandomTop(gender, generator = generator)
        bottom, bottomColor = getRandomBottom(gender, generator = generator)
        if gender == "m":
            self.torso = generator.choice(toonTorsoTypes[:3])
            self.topTex = top
            self.topTexColor = topColor 
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            self.botTex = bottom 
            self.botTexColor = bottomColor
            color = generator.choice(defaultBoyColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color
        else:
            self.torso = generator.choice(toonTorsoTypes[:6])
            self.topTex = top
            self.topTexColor = topColor
            self.sleeveTex = sleeve
            self.sleeveTexColor = sleeveColor
            if (self.torso[1] == 'd'):
                bottom, bottomColor = getRandomBottom(gender, generator = generator, girlBottomType = SKIRT)
            else:
                bottom, bottomColor = getRandomBottom(gender, generator = generator, girlBottomType = SHORTS)
            self.botTex = bottom 
            self.botTexColor = bottomColor
            color = generator.choice(defaultGirlColorList)
            self.armColor = color
            self.legColor = color
            self.headColor = color

        self.gloveColor = 0

    def asTuple(self):
        return (
        self.head, self.torso, self.legs, self.gender,
        self.topTex, self.topTexColor, self.sleeveTex, self.sleeveTexColor,
        self.botTex, self.botTexColor, self.armColor, self.gloveColor,
        self.legColor, self.headColor
        )
    
    def updateToonProperties(self, head=None, torso=None, legs=None,
                             gender=None, armColor=None, gloveColor=None,
                                legColor=None, headColor=None, topTex=None,
                                topTexColor=None, sleeveTex=None, sleeveTexColor=None,
                                botTex=None, botTexColor=None,
                                shirt=None, bottom=None):
        if head is not None:
            self.head = head
        if torso is not None:
            self.torso = torso
        if legs is not None:
            self.legs = legs
        if gender is not None:
            self.gender = gender
        if armColor is not None:
            self.armColor = armColor
        if gloveColor is not None:
            self.gloveColor = gloveColor
        if legColor is not None:
            self.legColor = legColor
        if headColor is not None:
            self.headColor = headColor
        if topTex is not None:
            self.topTex = topTex
        if topTexColor is not None:
            self.topTexColor = topTexColor
        if sleeveTex is not None:
            self.sleeveTex = sleeveTex
        if sleeveTexColor is not None:
            self.sleeveTexColor = sleeveTexColor
        if botTex is not None:
            self.botTex = botTex
        if botTexColor is not None:
            self.botTexColor = botTexColor
            return
        if shirt:
            _str, colorIndex = shirt
            defn = ShirtStyles[_str]
            self.topTex = defn[0]
            self.topTexColor = defn[2][colorIndex][0]
            self.sleeveTex = defn[1]
            self.sleeveTexColor = defn[2][colorIndex][1]
        if bottom:
            _str, colorIndex = bottom
            defn = BottomStyles[_str]
            self.botTex = defn[0]
            self.botTexColor = defn[1][colorIndex]
    
    def getType(self):
        _type = self.getAnimal()
        return _type

    def getAnimal(self):
        headAnimalMap = {
            'd': 'dog',
            'c': 'cat',
            'm': 'mouse',
            'h': 'horse',
            'r': 'rabbit',
            'f': 'duck',
            'p': 'monkey',
            'b': 'bear',
            's': 'pig',
            'x': 'deer',
            'z': 'beaver',
            'a': 'alligator',
            'v': 'fox',
            'n': 'bat',
            't': 'raccoon',
            'g': 'turkey',
            'e': 'koala',
            'j': 'kangaroo',
            'k': 'kiwi',
            'l': 'armadillo'
        }
        headKey = self.head[0]
        if headKey in headAnimalMap:
            return headAnimalMap[headKey]
        else:
            notify.error('unknown headStyle: ', headKey)

    def getHeadSize(self):
        if self.head[1] == 'l':
            return 'long'
        elif self.head[1] == 's':
            return 'short'
        else:
            notify.error('unknown head size: ', self.head[1])

    def getMuzzleSize(self):
        if self.head[2] == 'l':
            return 'long'
        elif self.head[2] == 's':
            return 'short'
        else:
            notify.error('unknown muzzle size: ', self.head[2])

    def getTorsoSize(self):
        if self.torso[0] == 'l':
            return 'long'
        elif self.torso[0] == 'm':
            return 'medium'
        elif self.torso[0] == 's':
            return 'short'
        else:
            notify.error('unknown torso size: ', self.torso[0])

    def getLegSize(self):
        if self.legs == 'l':
            return 'long'
        elif self.legs == 'm':
            return 'medium'
        elif self.legs == 's':
            return 'short'
        else:
            notify.error('unknown leg size: ', self.legs)

    def getGender(self):
        return self.gender

    def getClothes(self):
        if len(self.torso) == 1:
            return 'naked'
        elif self.torso[1] == 's':
            return 'shorts'
        elif self.torso[1] == 'd':
            return 'dress'
        else:
            notify.error('unknown clothing type: ', self.torso[1])

    def getArmColor(self):
        try:
            return allColorsList[self.armColor]
        except:
            return allColorsList[0]

    def getLegColor(self):
        try:
            return allColorsList[self.legColor]
        except:
            return allColorsList[0]

    def getHeadColor(self):
        try:
            return allColorsList[self.headColor]
        except:
            return allColorsList[0]

    def getGloveColor(self):
        try:
            return allColorsList[self.gloveColor]
        except:
            return allColorsList[0]

    def getBlackColor(self):
        try:
            return allColorsList[26]
        except:
            return allColorsList[0]

    def setTemporary(self, newHead, newArmColor, newLegColor, newHeadColor):
        if not self.cache and self.getArmColor != newArmColor:
            self.cache = (self.head,
             self.armColor,
             self.legColor,
             self.headColor)
            self.updateToonProperties(head=newHead, armColor=newArmColor, legColor=newLegColor, headColor=newHeadColor)

    def restoreTemporary(self, oldStyle):
        cache = ()
        if oldStyle:
            cache = oldStyle.cache
        if cache:
            self.updateToonProperties(head=cache[0], armColor=cache[1], legColor=cache[2], headColor=cache[3])
            if oldStyle:
                oldStyle.cache = ()
        
    def defaultColor(self):
        return 25

    def __defaultColors(self):
        color = self.defaultColor()
        self.armColor = color
        self.gloveColor = 0
        self.legColor = color
        self.headColor = color
        
    def newToon(self, dna, color = None):
        if len(dna) == 4:
            self.head = dna[0]
            self.torso = dna[1]
            self.legs = dna[2]
            self.gender = dna[3]
            self.topTex = 0
            self.topTexColor = 0
            self.sleeveTex = 0
            self.sleeveTexColor = 0
            self.botTex = 0
            self.botTexColor = 0
            if color is None:
                color = self.defaultColor()
            self.armColor = color
            self.legColor = color
            self.headColor = color
            self.gloveColor = 0
        else:
            notify.error("tuple must be in format ('%s', '%s', '%s', '%s')")
        return