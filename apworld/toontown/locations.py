from dataclasses import dataclass, field
from enum import IntEnum, Enum, auto
from typing import List, Dict

from BaseClasses import LocationProgressType
from . import consts
from .regions import ToontownRegionName
from .rules import Rule, ItemRule


class ToontownLocationName(Enum):
    STARTING_NEW_GAME =                         "Create a Toon (Create a Toon)"
    STARTING_TRACK_ONE =                        "Starter Track #1 (Create a Toon)"
    STARTING_TRACK_TWO =                        "Starter Track #2 (Create a Toon)"
    COLD_CALLER_DEFEATED =                      "Cog Gallery (Cold Caller)"
    SHORT_CHANGE_DEFEATED =                     "Cog Gallery (Short Change)"
    BOTTOM_FEEDER_DEFEATED =                    "Cog Gallery (Bottom Feeder)"
    FLUNKY_DEFEATED =                           "Cog Gallery (Flunky)"
    TELEMARKETER_DEFEATED =                     "Cog Gallery (Telemarketer)"
    PENNY_PINCHER_DEFEATED =                    "Cog Gallery (Penny Pincher)"
    BLOODSUCKER_DEFEATED =                      "Cog Gallery (Bloodsucker)"
    PENCIL_PUSHER_DEFEATED =                    "Cog Gallery (Pencil Pusher)"
    NAME_DROPPER_DEFEATED =                     "Cog Gallery (Name Dropper)"
    TIGHTWAD_DEFEATED =                         "Cog Gallery (Tightwad)"
    DOUBLE_TALKER_DEFEATED =                    "Cog Gallery (Double Talker)"
    YESMAN_DEFEATED =                           "Cog Gallery (Yesman)"
    GLAD_HANDER_DEFEATED =                      "Cog Gallery (Glad Hander)"
    BEAN_COUNTER_DEFEATED =                     "Cog Gallery (Bean Counter)"
    AMBULANCE_CHASER_DEFEATED =                 "Cog Gallery (Ambulance Chaser)"
    MICROMANAGER_DEFEATED =                     "Cog Gallery (Micromanager)"
    MOVER_AND_SHAKER_DEFEATED =                 "Cog Gallery (Mover and Shaker)"
    NUMBER_CRUNCHER_DEFEATED =                  "Cog Gallery (Number Cruncher)"
    BACKSTABBER_DEFEATED =                      "Cog Gallery (Backstabber)"
    DOWNSIZER_DEFEATED =                        "Cog Gallery (Downsizer)"
    TWO_FACE_DEFEATED =                         "Cog Gallery (Two Face)"
    MONEY_BAGS_DEFEATED =                       "Cog Gallery (Money Bags)"
    SPIN_DOCTOR_DEFEATED =                      "Cog Gallery (Spin Doctor)"
    HEAD_HUNTER_DEFEATED =                      "Cog Gallery (Head Hunter)"
    MINGLER_DEFEATED =                          "Cog Gallery (Mingler)"
    LOAN_SHARK_DEFEATED =                       "Cog Gallery (Loan Shark)"
    LEGAL_EAGLE_DEFEATED =                      "Cog Gallery (Legal Eagle)"
    CORPORATE_RAIDER_DEFEATED =                 "Cog Gallery (Corporate Raider)"
    MR_HOLLYWOOD_DEFEATED =                     "Cog Gallery (Mr. Hollywood)"
    ROBBER_BARRON_DEFEATED =                    "Cog Gallery (Robber Baron)"
    BIG_WIG_DEFEATED =                          "Cog Gallery (Big Wig)"
    BIG_CHEESE_DEFEATED =                       "Cog Gallery (Big Cheese)"
    COLD_CALLER_MAXED =                         "Cog Gallery Maxed (Cold Caller)"
    SHORT_CHANGE_MAXED =                        "Cog Gallery Maxed (Short Change)"
    BOTTOM_FEEDER_MAXED =                       "Cog Gallery Maxed (Bottom Feeder)"
    FLUNKY_MAXED =                              "Cog Gallery Maxed (Flunky)"
    TELEMARKETER_MAXED =                        "Cog Gallery Maxed (Telemarketer)"
    PENNY_PINCHER_MAXED =                       "Cog Gallery Maxed (Penny Pincher)"
    BLOODSUCKER_MAXED =                         "Cog Gallery Maxed (Bloodsucker)"
    PENCIL_PUSHER_MAXED =                       "Cog Gallery Maxed (Pencil Pusher)"
    NAME_DROPPER_MAXED =                        "Cog Gallery Maxed (Name Dropper)"
    TIGHTWAD_MAXED =                            "Cog Gallery Maxed (Tightwad)"
    DOUBLE_TALKER_MAXED =                       "Cog Gallery Maxed (Double Talker)"
    YESMAN_MAXED =                              "Cog Gallery Maxed (Yesman)"
    GLAD_HANDER_MAXED =                         "Cog Gallery Maxed (Glad Hander)"
    BEAN_COUNTER_MAXED =                        "Cog Gallery Maxed (Bean Counter)"
    AMBULANCE_CHASER_MAXED =                    "Cog Gallery Maxed (Ambulance Chaser)"
    MICROMANAGER_MAXED =                        "Cog Gallery Maxed (Micromanager)"
    MOVER_AND_SHAKER_MAXED =                    "Cog Gallery Maxed (Mover and Shaker)"
    NUMBER_CRUNCHER_MAXED =                     "Cog Gallery Maxed (Number Cruncher)"
    BACKSTABBER_MAXED =                         "Cog Gallery Maxed (Backstabber)"
    DOWNSIZER_MAXED =                           "Cog Gallery Maxed (Downsizer)"
    TWO_FACE_MAXED =                            "Cog Gallery Maxed (Two Face)"
    MONEY_BAGS_MAXED =                          "Cog Gallery Maxed (Money Bags)"
    SPIN_DOCTOR_MAXED =                         "Cog Gallery Maxed (Spin Doctor)"
    HEAD_HUNTER_MAXED =                         "Cog Gallery Maxed (Head Hunter)"
    MINGLER_MAXED =                             "Cog Gallery Maxed (Mingler)"
    LOAN_SHARK_MAXED =                          "Cog Gallery Maxed (Loan Shark)"
    LEGAL_EAGLE_MAXED =                         "Cog Gallery Maxed (Legal Eagle)"
    CORPORATE_RAIDER_MAXED =                    "Cog Gallery Maxed (Corporate Raider)"
    MR_HOLLYWOOD_MAXED =                        "Cog Gallery Maxed (Mr. Hollywood)"
    ROBBER_BARRON_MAXED =                       "Cog Gallery Maxed (Robber Baron)"
    BIG_WIG_MAXED =                             "Cog Gallery Maxed (Big Wig)"
    BIG_CHEESE_MAXED =                          "Cog Gallery Maxed (Big Cheese)"
    TOONUP_FEATHER_UNLOCKED =                   "Feather Trained (Toon-up Training)"
    TOONUP_MEGAPHONE_UNLOCKED =                 "Megaphone Trained (Toon-up Training)"
    TOONUP_LIPSTICK_UNLOCKED =                  "Lipstick Trained (Toon-up Training)"
    TOONUP_CANE_UNLOCKED =                      "Bamboo Cane Trained (Toon-up Training)"
    TOONUP_PIXIE_UNLOCKED =                     "Pixie Dust Trained (Toon-up Training)"
    TOONUP_JUGGLING_UNLOCKED =                  "Juggling Cubes Trained (Toon-up Training)"
    TOONUP_HIGHDIVE_UNLOCKED =                  "High Dive Trained (MAXED Toon-up)"
    TRAP_BANANA_UNLOCKED =                      "Banana Peel Trained (Trap Training)"
    TRAP_RAKE_UNLOCKED =                        "Rake Trained (Trap Training)"
    TRAP_MARBLES_UNLOCKED =                     "Marbles Trained (Trap Training)"
    TRAP_QUICKSAND_UNLOCKED =                   "Quicksand Trained (Trap Training)"
    TRAP_TRAPDOOR_UNLOCKED =                    "Trapdoor Trained (Trap Training)"
    TRAP_TNT_UNLOCKED =                         "TNT Trained (Trap Training)"
    TRAP_TRAIN_UNLOCKED =                       "Railroad Trained (MAXED Trap)"
    LURE_ONEBILL_UNLOCKED =                     "$1 Bill Trained (Lure Training)"
    LURE_SMALLMAGNET_UNLOCKED =                 "Small Magnet Trained (Lure Training)"
    LURE_FIVEBILL_UNLOCKED =                    "$5 Bill Trained (Lure Training)"
    LURE_BIGMAGNET_UNLOCKED =                   "Big Magnet Trained (Lure Training)"
    LURE_TENBILL_UNLOCKED =                     "$10 Bill Trained (Lure Training)"
    LURE_HYPNO_UNLOCKED =                       "Hypno-Goggles Trained (Lure Training)"
    LURE_PRESENTATION_UNLOCKED =                "Presentation Trained (MAXED Lure)"
    SOUND_BIKEHORN_UNLOCKED =                   "Bike Horn Trained (Sound Training)"
    SOUND_WHISTLE_UNLOCKED =                    "Whistle Trained (Sound Training)"
    SOUND_BUGLE_UNLOCKED =                      "Bugle Trained (Sound Training)"
    SOUND_AOOGAH_UNLOCKED =                     "Aoogah Trained (Sound Training)"
    SOUND_TRUNK_UNLOCKED =                      "Elephant Trunk Trained (Sound Training)"
    SOUND_FOG_UNLOCKED =                        "Foghorn Trained (Sound Training)"
    SOUND_OPERA_UNLOCKED =                      "Opera Singer Trained (MAXED Sound)"
    THROW_CUPCAKE_UNLOCKED =                    "Cupcake Trained (Throw Training)"
    THROW_FRUITPIESLICE_UNLOCKED =              "Fruit Pie Slice Trained (Throw Training)"
    THROW_CREAMPIESLICE_UNLOCKED =              "Cream Pie Slice Trained (Throw Training)"
    THROW_WHOLEFRUIT_UNLOCKED =                 "Whole Fruit Pie Trained (Throw Training)"
    THROW_WHOLECREAM_UNLOCKED =                 "Whole Cream Pie Trained (Throw Training)"
    THROW_CAKE_UNLOCKED =                       "Birthday Cake Trained (Throw Training)"
    THROW_WEDDING_UNLOCKED =                    "Wedding Cake Trained (MAXED Throw)"
    SQUIRT_SQUIRTFLOWER_UNLOCKED =              "Squirting Flower Trained (Squirt Training)"
    SQUIRT_GLASS_UNLOCKED =                     "Glass of Water Trained (Squirt Training)"
    SQUIRT_SQUIRTGUN_UNLOCKED =                 "Squirt Gun Trained (Squirt Training)"
    SQUIRT_SELTZER_UNLOCKED =                   "Seltzer Bottle Trained (Squirt Training)"
    SQUIRT_HOSE_UNLOCKED =                      "Firehose Trained (Squirt Training)"
    SQUIRT_CLOUD_UNLOCKED =                     "Stormcloud Trained (Squirt Training)"
    SQUIRT_GEYSER_UNLOCKED =                    "Geyser Trained (MAXED Squirt)"
    DROP_FLOWERPOT_UNLOCKED =                   "Flowerpot Trained (Drop Training)"
    DROP_SANDBAG_UNLOCKED =                     "Sandbag Trained (Drop Training)"
    DROP_ANVIL_UNLOCKED =                       "Anvil Trained (Drop Training)"
    DROP_BIGWEIGHT_UNLOCKED =                   "Big Weight Trained (Drop Training)"
    DROP_SAFE_UNLOCKED =                        "Safe Trained (Drop Training)"
    DROP_PIANO_UNLOCKED =                       "Piano Trained (Drop Training)"
    DROP_BOAT_UNLOCKED =                        "Toontanic Trained (MAXED Drop)"
    BALLOON_FISH_0 =                            "Balloon Fish"
    BALLOON_FISH_1 =                            "Hot Air Balloon Fish"
    BALLOON_FISH_2 =                            "Weather Balloon Fish"
    BALLOON_FISH_3 =                            "Water Balloon Fish"
    BALLOON_FISH_4 =                            "Red Balloon Fish"
    JELLYFISH_0 =                               "Peanut Butter & Jellyfish"
    JELLYFISH_1 =                               "Grape PB&J Jellyfish"
    JELLYFISH_2 =                               "Crunchy PB&J Jellyfish"
    JELLYFISH_3 =                               "Strawberry PB&J Jellyfish"
    JELLYFISH_4 =                               "Concord Grape PB&J Jellyfish"
    CAT_FISH_0 =                                "Cat Fish"
    CAT_FISH_1 =                                "Siamese Cat Fish"
    CAT_FISH_2 =                                "Alley Cat Fish"
    CAT_FISH_3 =                                "Tabby Cat Fish"
    CAT_FISH_4 =                                "Tom Cat Fish"
    CLOWN_FISH_0 =                              "Clown Fish"
    CLOWN_FISH_1 =                              "Sad Clown Fish"
    CLOWN_FISH_2 =                              "Party Clown Fish"
    CLOWN_FISH_3 =                              "Circus Clown Fish"
    FROZEN_FISH_0 =                             "Frozen Fish"
    STAR_FISH_0 =                               "Star Fish"
    STAR_FISH_1 =                               "Five Star Fish"
    STAR_FISH_2 =                               "Rock Star Fish"
    STAR_FISH_3 =                               "Shining Star Fish"
    STAR_FISH_4 =                               "All Star Fish"
    HOLEY_MACKEREL_0 =                          "Holey Mackerel"
    DOG_FISH_0 =                                "Dog Fish"
    DOG_FISH_1 =                                "Bull Dog Fish"
    DOG_FISH_2 =                                "Hot Dog Fish"
    DOG_FISH_3 =                                "Dalmation Dog Fish"
    DOG_FISH_4 =                                "Puppy Dog Fish"
    DEVIL_RAY_0 =                               "Devil Ray"
    AMORE_EEL_0 =                               "Amore Eel"
    AMORE_EEL_1 =                               "Electric Amore Eel"
    NURSE_SHARK_0 =                             "Nurse Shark"
    NURSE_SHARK_1 =                             "Clara Nurse Shark"
    NURSE_SHARK_2 =                             "Florence Nurse Shark"
    KING_CRAB_0 =                               "King Crab"
    KING_CRAB_1 =                               "Alaskan King Crab"
    KING_CRAB_2 =                               "Old King Crab"
    MOON_FISH_0 =                               "Moon Fish"
    MOON_FISH_1 =                               "Full Moon Fish"
    MOON_FISH_2 =                               "Half Moon Fish"
    MOON_FISH_3 =                               "New Moon Fish"
    MOON_FISH_4 =                               "Crescent Moon Fish"
    MOON_FISH_5 =                               "Harvest Moon Fish"
    SEA_HORSE_0 =                               "Sea Horse"
    SEA_HORSE_1 =                               "Rocking Sea Horse"
    SEA_HORSE_2 =                               "Clydesdale Sea Horse"
    SEA_HORSE_3 =                               "Arabian Sea Horse"
    POOL_SHARK_0 =                              "Pool Shark"
    POOL_SHARK_1 =                              "Kiddie Pool Shark"
    POOL_SHARK_2 =                              "Swimming Pool Shark"
    POOL_SHARK_3 =                              "Olympic Pool Shark"
    BEAR_ACUDA_0 =                              "Brown Bear Acuda"
    BEAR_ACUDA_1 =                              "Black Bear Acuda"
    BEAR_ACUDA_2 =                              "Koala Bear Acuda"
    BEAR_ACUDA_3 =                              "Honey Bear Acuda"
    BEAR_ACUDA_4 =                              "Polar Bear Acuda"
    BEAR_ACUDA_5 =                              "Panda Bear Acuda"
    BEAR_ACUDA_6 =                              "Kodiac Bear Acuda"
    BEAR_ACUDA_7 =                              "Grizzly Bear Acuda"
    CUTTHROAT_TROUT_0 =                         "Cutthroat Trout"
    CUTTHROAT_TROUT_1 =                         "Captain Cutthroat Trout"
    CUTTHROAT_TROUT_2 =                         "Scurvy Cutthroat Trout"
    PIANO_TUNA_0 =                              "Piano Tuna"
    PIANO_TUNA_1 =                              "Grand Piano Tuna"
    PIANO_TUNA_2 =                              "Baby Grand Piano Tuna"
    PIANO_TUNA_3 =                              "Upright Piano Tuna"
    PIANO_TUNA_4 =                              "Player Piano Tuna"
    GENUS_BALLOON_FISH =                        "Balloon Fish (Genus)"
    GENUS_JELLYFISH =                           "Jellyfish (Genus)"
    GENUS_CAT_FISH =                            "Cat Fish (Genus)"
    GENUS_CLOWN_FISH =                          "Clown Fish (Genus)"
    GENUS_FROZEN_FISH =                         "Frozen Fish (Genus)"
    GENUS_STAR_FISH =                           "Star Fish (Genus)"
    GENUS_HOLEY_MACKEREL =                      "Holey Mackerel (Genus)"
    GENUS_DOG_FISH =                            "Dog Fish (Genus)"
    GENUS_DEVIL_RAY =                           "Devil Ray (Genus)"
    GENUS_AMORE_EEL =                           "Amore Eel (Genus)"
    GENUS_NURSE_SHARK =                         "Nurse Shark (Genus)"
    GENUS_KING_CRAB =                           "King Crab (Genus)"
    GENUS_MOON_FISH =                           "Moon Fish (Genus)"
    GENUS_SEA_HORSE =                           "Sea Horse (Genus)"
    GENUS_POOL_SHARK =                          "Pool Shark (Genus)"
    GENUS_BEAR_ACUDA =                          "Bear Acuda (Genus)"
    GENUS_CUTTHROAT_TROUT =                     "Cutthroat Trout (Genus)"
    GENUS_PIANO_TUNA =                          "Piano Tuna (Genus)"
    FISHING_10_SPECIES =                        "(Fishing) 10 Species Caught Trophy"
    FISHING_20_SPECIES =                        "(Fishing) 20 Species Caught Trophy"
    FISHING_30_SPECIES =                        "(Fishing) 30 Species Caught Trophy"
    FISHING_40_SPECIES =                        "(Fishing) 40 Species Caught Trophy"
    FISHING_50_SPECIES =                        "(Fishing) 50 Species Caught Trophy"
    FISHING_60_SPECIES =                        "(Fishing) 60 Species Caught Trophy"
    FISHING_COMPLETE_ALBUM =                    "(Fishing) All 70 Species Caught Trophy"
    EASY_GOLF_1 =                               "Walk in the Par (Hole 1)"
    EASY_GOLF_2 =                               "Walk in the Par (Hole 2)"
    EASY_GOLF_3 =                               "Walk in the Par (Hole 3)"
    MED_GOLF_1 =                                "Hole Some Fun (Hole 1)"
    MED_GOLF_2 =                                "Hole Some Fun (Hole 2)"
    MED_GOLF_3 =                                "Hole Some Fun (Hole 3)"
    MED_GOLF_4 =                                "Hole Some Fun (Hole 4)"
    MED_GOLF_5 =                                "Hole Some Fun (Hole 5)"
    MED_GOLF_6 =                                "Hole Some Fun (Hole 6)"
    HARD_GOLF_1 =                               "The Hole Kit and Caboodle (Hole 1)"
    HARD_GOLF_2 =                               "The Hole Kit and Caboodle (Hole 2)"
    HARD_GOLF_3 =                               "The Hole Kit and Caboodle (Hole 3)"
    HARD_GOLF_4 =                               "The Hole Kit and Caboodle (Hole 4)"
    HARD_GOLF_5 =                               "The Hole Kit and Caboodle (Hole 5)"
    HARD_GOLF_6 =                               "The Hole Kit and Caboodle (Hole 6)"
    HARD_GOLF_7 =                               "The Hole Kit and Caboodle (Hole 7)"
    HARD_GOLF_8 =                               "The Hole Kit and Caboodle (Hole 8)"
    HARD_GOLF_9 =                               "The Hole Kit and Caboodle (Hole 9)"
    SPEEDWAY_1_CLEAR =                          "Screwball Stadium Cleared"
    SPEEDWAY_1_QUALIFY =                        "Screwball Stadium Qualified"
    SPEEDWAY_2_CLEAR =                          "Corkscrew Coliseum Cleared"
    SPEEDWAY_2_QUALIFY =                        "Corkscrew Coliseum Qualified"
    RURAL_1_CLEAR =                             "Rustic Raceway Cleared"
    RURAL_1_QUALIFY =                           "Rustic Raceway Qualified"
    RURAL_2_CLEAR =                             "Airborne Acres Cleared"
    RURAL_2_QUALIFY =                           "Airborne Acres Qualified"
    URBAN_1_CLEAR =                             "City Circuit Cleared"
    URBAN_1_QUALIFY =                           "City Circuit Qualified"
    URBAN_2_CLEAR =                             "Blizzard Boulevard Clear"
    URBAN_2_QUALIFY =                           "Blizzard Boulevard Qualified"
    TOONTOWN_CENTRAL_TASK_1 =                   "Toontown Central Task #1"
    TOONTOWN_CENTRAL_TASK_2 =                   "Toontown Central Task #2"
    TOONTOWN_CENTRAL_TASK_3 =                   "Toontown Central Task #3"
    TOONTOWN_CENTRAL_TASK_4 =                   "Toontown Central Task #4"
    TOONTOWN_CENTRAL_TASK_5 =                   "Toontown Central Task #5"
    TOONTOWN_CENTRAL_TASK_6 =                   "Toontown Central Task #6"
    TOONTOWN_CENTRAL_TASK_7 =                   "Toontown Central Task #7"
    TOONTOWN_CENTRAL_TASK_8 =                   "Toontown Central Task #8"
    TOONTOWN_CENTRAL_TASK_9 =                   "Toontown Central Task #9"
    TOONTOWN_CENTRAL_TASK_10 =                  "Toontown Central Task #10"
    TOONTOWN_CENTRAL_TASK_11 =                  "Toontown Central Task #11"
    TOONTOWN_CENTRAL_TASK_12 =                  "Toontown Central Task #12"
    DONALDS_DOCK_TASK_1 =                       "Donald's Dock Task #1"
    DONALDS_DOCK_TASK_2 =                       "Donald's Dock Task #2"
    DONALDS_DOCK_TASK_3 =                       "Donald's Dock Task #3"
    DONALDS_DOCK_TASK_4 =                       "Donald's Dock Task #4"
    DONALDS_DOCK_TASK_5 =                       "Donald's Dock Task #5"
    DONALDS_DOCK_TASK_6 =                       "Donald's Dock Task #6"
    DONALDS_DOCK_TASK_7 =                       "Donald's Dock Task #7"
    DONALDS_DOCK_TASK_8 =                       "Donald's Dock Task #8"
    DONALDS_DOCK_TASK_9 =                       "Donald's Dock Task #9"
    DONALDS_DOCK_TASK_10 =                      "Donald's Dock Task #10"
    DONALDS_DOCK_TASK_11 =                      "Donald's Dock Task #11"
    DONALDS_DOCK_TASK_12 =                      "Donald's Dock Task #12"
    DAISYS_GARDENS_TASK_1 =                     "Daisy Gardens Task #1"
    DAISYS_GARDENS_TASK_2 =                     "Daisy Gardens Task #2"
    DAISYS_GARDENS_TASK_3 =                     "Daisy Gardens Task #3"
    DAISYS_GARDENS_TASK_4 =                     "Daisy Gardens Task #4"
    DAISYS_GARDENS_TASK_5 =                     "Daisy Gardens Task #5"
    DAISYS_GARDENS_TASK_6 =                     "Daisy Gardens Task #6"
    DAISYS_GARDENS_TASK_7 =                     "Daisy Gardens Task #7"
    DAISYS_GARDENS_TASK_8 =                     "Daisy Gardens Task #8"
    DAISYS_GARDENS_TASK_9 =                     "Daisy Gardens Task #9"
    DAISYS_GARDENS_TASK_10 =                    "Daisy Gardens Task #10"
    DAISYS_GARDENS_TASK_11 =                    "Daisy Gardens Task #11"
    DAISYS_GARDENS_TASK_12 =                    "Daisy Gardens Task #12"
    MINNIES_MELODYLAND_TASK_1 =                 "Minnie's Melodyland Task #1"
    MINNIES_MELODYLAND_TASK_2 =                 "Minnie's Melodyland Task #2"
    MINNIES_MELODYLAND_TASK_3 =                 "Minnie's Melodyland Task #3"
    MINNIES_MELODYLAND_TASK_4 =                 "Minnie's Melodyland Task #4"
    MINNIES_MELODYLAND_TASK_5 =                 "Minnie's Melodyland Task #5"
    MINNIES_MELODYLAND_TASK_6 =                 "Minnie's Melodyland Task #6"
    MINNIES_MELODYLAND_TASK_7 =                 "Minnie's Melodyland Task #7"
    MINNIES_MELODYLAND_TASK_8 =                 "Minnie's Melodyland Task #8"
    MINNIES_MELODYLAND_TASK_9 =                 "Minnie's Melodyland Task #9"
    MINNIES_MELODYLAND_TASK_10 =                "Minnie's Melodyland Task #10"
    MINNIES_MELODYLAND_TASK_11 =                "Minnie's Melodyland Task #11"
    MINNIES_MELODYLAND_TASK_12 =                "Minnie's Melodyland Task #12"
    THE_BRRRGH_TASK_1 =                         "The Brrrgh Task #1"
    THE_BRRRGH_TASK_2 =                         "The Brrrgh Task #2"
    THE_BRRRGH_TASK_3 =                         "The Brrrgh Task #3"
    THE_BRRRGH_TASK_4 =                         "The Brrrgh Task #4"
    THE_BRRRGH_TASK_5 =                         "The Brrrgh Task #5"
    THE_BRRRGH_TASK_6 =                         "The Brrrgh Task #6"
    THE_BRRRGH_TASK_7 =                         "The Brrrgh Task #7"
    THE_BRRRGH_TASK_8 =                         "The Brrrgh Task #8"
    THE_BRRRGH_TASK_9 =                         "The Brrrgh Task #9"
    THE_BRRRGH_TASK_10 =                        "The Brrrgh Task #10"
    THE_BRRRGH_TASK_11 =                        "The Brrrgh Task #11"
    THE_BRRRGH_TASK_12 =                        "The Brrrgh Task #12"
    DONALDS_DREAMLAND_TASK_1 =                  "Donald's Dreamland Task #1"
    DONALDS_DREAMLAND_TASK_2 =                  "Donald's Dreamland Task #2"
    DONALDS_DREAMLAND_TASK_3 =                  "Donald's Dreamland Task #3"
    DONALDS_DREAMLAND_TASK_4 =                  "Donald's Dreamland Task #4"
    DONALDS_DREAMLAND_TASK_5 =                  "Donald's Dreamland Task #5"
    DONALDS_DREAMLAND_TASK_6 =                  "Donald's Dreamland Task #6"
    DONALDS_DREAMLAND_TASK_7 =                  "Donald's Dreamland Task #7"
    DONALDS_DREAMLAND_TASK_8 =                  "Donald's Dreamland Task #8"
    DONALDS_DREAMLAND_TASK_9 =                  "Donald's Dreamland Task #9"
    DONALDS_DREAMLAND_TASK_10 =                 "Donald's Dreamland Task #10"
    DONALDS_DREAMLAND_TASK_11 =                 "Donald's Dreamland Task #11"
    DONALDS_DREAMLAND_TASK_12 =                 "Donald's Dreamland Task #12"
    ONE_STORY =                                 "One Story Building Clear"
    TWO_STORY =                                 "Two Story Building Clear"
    THREE_STORY =                               "Three Story Building Clear"
    FOUR_STORY =                                "Four Story Building Clear"
    FIVE_STORY =                                "Five Story Building Clear"
    TTC_SHOP_1 =                                "Thickie (TTC Pet Shop)"
    TTC_SHOP_2 =                                "Bowser (TTC Pet Shop)"
    TTC_SHOP_3 =                                "Snowman (TTC Pet Shop)"
    DD_SHOP_1 =                                 "Jo (DD Pet Shop)"
    DD_SHOP_2 =                                 "Joe (DD Pet Shop)"
    DD_SHOP_3 =                                 "Jojo (DD Pet Shop)"
    DG_SHOP_1 =                                 "Lambchop (DG Pet Shop)"
    DG_SHOP_2 =                                 "Pudgette (DG Pet Shop)"
    DG_SHOP_3 =                                 "Yum Yum (DG Pet Shop)"
    MML_SHOP_1 =                                "Zsa Zsa (MML Pet Shop)"
    MML_SHOP_2 =                                "Arf (MML Pet Shop)"
    MML_SHOP_3 =                                "Banana (MML Pet Shop)"
    TB_SHOP_1 =                                 "Big Shot (TB Pet Shop)"
    TB_SHOP_2 =                                 "Big Red (TB Pet Shop)"
    TB_SHOP_3 =                                 "Bigbelly (TB Pet Shop)"
    DDL_SHOP_1 =                                "Bozo (DDL Pet Shop)"
    DDL_SHOP_2 =                                "Brainchild (DDL Pet Shop)"
    DDL_SHOP_3 =                                "Critter (DDL Pet Shop)"
    TTC_TREASURE_1 =                            "Toontown Central AP Treasure 1"
    TTC_TREASURE_2 =                            "Toontown Central AP Treasure 2"
    TTC_TREASURE_3 =                            "Toontown Central AP Treasure 3"
    TTC_TREASURE_4 =                            "Toontown Central AP Treasure 4"
    TTC_TREASURE_5 =                            "Toontown Central AP Treasure 5"
    TTC_TREASURE_6 =                            "Toontown Central AP Treasure 6"
    DD_TREASURE_1 =                             "Donald's Dock AP Treasure 1"
    DD_TREASURE_2 =                             "Donald's Dock AP Treasure 2"
    DD_TREASURE_3 =                             "Donald's Dock AP Treasure 3"
    DD_TREASURE_4 =                             "Donald's Dock AP Treasure 4"
    DD_TREASURE_5 =                             "Donald's Dock AP Treasure 5"
    DD_TREASURE_6 =                             "Donald's Dock AP Treasure 6"
    DG_TREASURE_1 =                             "Daisy Gardens AP Treasure 1"
    DG_TREASURE_2 =                             "Daisy Gardens AP Treasure 2"
    DG_TREASURE_3 =                             "Daisy Gardens AP Treasure 3"
    DG_TREASURE_4 =                             "Daisy Gardens AP Treasure 4"
    DG_TREASURE_5 =                             "Daisy Gardens AP Treasure 5"
    DG_TREASURE_6 =                             "Daisy Gardens AP Treasure 6"
    MML_TREASURE_1 =                            "Minnie's Melodyland AP Treasure 1"
    MML_TREASURE_2 =                            "Minnie's Melodyland AP Treasure 2"
    MML_TREASURE_3 =                            "Minnie's Melodyland AP Treasure 3"
    MML_TREASURE_4 =                            "Minnie's Melodyland AP Treasure 4"
    MML_TREASURE_5 =                            "Minnie's Melodyland AP Treasure 5"
    MML_TREASURE_6 =                            "Minnie's Melodyland AP Treasure 6"
    TB_TREASURE_1 =                             "The Brrrgh AP Treasure 1"
    TB_TREASURE_2 =                             "The Brrrgh AP Treasure 2"
    TB_TREASURE_3 =                             "The Brrrgh AP Treasure 3"
    TB_TREASURE_4 =                             "The Brrrgh AP Treasure 4"
    TB_TREASURE_5 =                             "The Brrrgh AP Treasure 5"
    TB_TREASURE_6 =                             "The Brrrgh AP Treasure 6"
    DDL_TREASURE_1 =                            "Donald's Dreamland AP Treasure 1"
    DDL_TREASURE_2 =                            "Donald's Dreamland AP Treasure 2"
    DDL_TREASURE_3 =                            "Donald's Dreamland AP Treasure 3"
    DDL_TREASURE_4 =                            "Donald's Dreamland AP Treasure 4"
    DDL_TREASURE_5 =                            "Donald's Dreamland AP Treasure 5"
    DDL_TREASURE_6 =                            "Donald's Dreamland AP Treasure 6"
    GS_TREASURE_1 =                             "Goofy Speedway AP Treasure 1"
    GS_TREASURE_2 =                             "Goofy Speedway AP Treasure 2"
    GS_TREASURE_3 =                             "Goofy Speedway AP Treasure 3"
    GS_TREASURE_4 =                             "Goofy Speedway AP Treasure 4"
    GS_TREASURE_5 =                             "Goofy Speedway AP Treasure 5"
    GS_TREASURE_6 =                             "Goofy Speedway AP Treasure 6"
    AA_TREASURE_1 =                             "Acorn Acres AP Treasure 1"
    AA_TREASURE_2 =                             "Acorn Acres AP Treasure 2"
    AA_TREASURE_3 =                             "Acorn Acres AP Treasure 3"
    AA_TREASURE_4 =                             "Acorn Acres AP Treasure 4"
    AA_TREASURE_5 =                             "Acorn Acres AP Treasure 5"
    AA_TREASURE_6 =                             "Acorn Acres AP Treasure 6"
    SBHQ_TREASURE_1 =                           "Sellbot HQ AP Treasure 1"
    SBHQ_TREASURE_2 =                           "Sellbot HQ AP Treasure 2"
    SBHQ_TREASURE_3 =                           "Sellbot HQ AP Treasure 3"
    SBHQ_TREASURE_4 =                           "Sellbot HQ AP Treasure 4"
    SBHQ_TREASURE_5 =                           "Sellbot HQ AP Treasure 5"
    SBHQ_TREASURE_6 =                           "Sellbot HQ AP Treasure 6"
    CBHQ_TREASURE_1 =                           "Cashbot HQ AP Treasure 1"
    CBHQ_TREASURE_2 =                           "Cashbot HQ AP Treasure 2"
    CBHQ_TREASURE_3 =                           "Cashbot HQ AP Treasure 3"
    CBHQ_TREASURE_4 =                           "Cashbot HQ AP Treasure 4"
    CBHQ_TREASURE_5 =                           "Cashbot HQ AP Treasure 5"
    CBHQ_TREASURE_6 =                           "Cashbot HQ AP Treasure 6"
    LBHQ_TREASURE_1 =                           "Lawbot HQ AP Treasure 1"
    LBHQ_TREASURE_2 =                           "Lawbot HQ AP Treasure 2"
    LBHQ_TREASURE_3 =                           "Lawbot HQ AP Treasure 3"
    LBHQ_TREASURE_4 =                           "Lawbot HQ AP Treasure 4"
    LBHQ_TREASURE_5 =                           "Lawbot HQ AP Treasure 5"
    LBHQ_TREASURE_6 =                           "Lawbot HQ AP Treasure 6"
    BBHQ_TREASURE_1 =                           "Bossbot HQ AP Treasure 1"
    BBHQ_TREASURE_2 =                           "Bossbot HQ AP Treasure 2"
    BBHQ_TREASURE_3 =                           "Bossbot HQ AP Treasure 3"
    BBHQ_TREASURE_4 =                           "Bossbot HQ AP Treasure 4"
    BBHQ_TREASURE_5 =                           "Bossbot HQ AP Treasure 5"
    BBHQ_TREASURE_6 =                           "Bossbot HQ AP Treasure 6"
    FRONT_FACTORY_BARREL_1 =                    "Front Factory West Silo Barrel"
    FRONT_FACTORY_BARREL_2 =                    "Front Factory East Silo Barrel"
    FRONT_FACTORY_BARREL_3 =                    "Front Factory Warehouse Barrel"
    CLEAR_FRONT_FACTORY =                       "Front Factory Cleared"
    SIDE_FACTORY_BARREL_1 =                     "Side Factory West Silo Barrel"
    SIDE_FACTORY_BARREL_2 =                     "Side Factory East Silo Barrel"
    SIDE_FACTORY_BARREL_3 =                     "Side Factory Warehouse Barrel"
    CLEAR_SIDE_FACTORY =                        "Side Factory Cleared"
    COIN_MINT_BARREL_1 =                        "Coin Mint Parkour Barrel"
    COIN_MINT_BARREL_2 =                        "Coin Mint Stomper Barrel"
    COIN_MINT_BARREL_3 =                        "Coin Mint Paint Mixer Barrel"
    CLEAR_COIN_MINT =                           "Coin Mint Cleared"
    DOLLAR_MINT_BARREL_1 =                      "Dollar Mint Parkour Barrel"
    DOLLAR_MINT_BARREL_2 =                      "Dollar Mint Stomper Barrel"
    DOLLAR_MINT_BARREL_3 =                      "Dollar Mint Paint Mixer Barrel"
    CLEAR_DOLLAR_MINT =                         "Dollar Mint Cleared"
    BULLION_MINT_BARREL_1 =                     "Bullion Mint Parkour Barrel"
    BULLION_MINT_BARREL_2 =                     "Bullion Mint Stomper Barrel"
    BULLION_MINT_BARREL_3 =                     "Bullion Mint Paint Mixer Barrel"
    CLEAR_BULLION_MINT =                        "Bullion Mint Cleared"
    A_OFFICE_BARREL_1 =                         "A Office Platform Barrel (Floor 1)"
    A_OFFICE_BARREL_2 =                         "A Office Platform Barrel (Floor 2)"
    A_OFFICE_BARREL_3 =                         "A Office Battle Barrel (Floor 1)"
    A_OFFICE_BARREL_4 =                         "A Office Battle Barrel (Floor 2)"
    CLEAR_A_OFFICE =                            "A Office Cleared"
    B_OFFICE_BARREL_1 =                         "B Office Platform Barrel (Floor 1)"
    B_OFFICE_BARREL_2 =                         "B Office Platform Barrel (Floor 2)"
    B_OFFICE_BARREL_3 =                         "B Office Battle Barrel (Floor 1)"
    B_OFFICE_BARREL_4 =                         "B Office Battle Barrel (Floor 2)"
    CLEAR_B_OFFICE =                            "B Office Cleared"
    C_OFFICE_BARREL_1 =                         "C Office Platform Barrel (Floor 1)"
    C_OFFICE_BARREL_2 =                         "C Office Platform Barrel (Floor 2)"
    C_OFFICE_BARREL_3 =                         "C Office Battle Barrel (Floor 1)"
    C_OFFICE_BARREL_4 =                         "C Office Battle Barrel (Floor 2)"
    CLEAR_C_OFFICE =                            "C Office Cleared"
    D_OFFICE_BARREL_1 =                         "D Office Platform Barrel (Floor 1)"
    D_OFFICE_BARREL_2 =                         "D Office Platform Barrel (Floor 2)"
    D_OFFICE_BARREL_3 =                         "D Office Battle Barrel (Floor 1)"
    D_OFFICE_BARREL_4 =                         "D Office Battle Barrel (Floor 2)"
    CLEAR_D_OFFICE =                            "D Office Cleared"
    FRONT_ONE_BARREL_1 =                        "Front One Fairway Barrel"
    FRONT_ONE_BARREL_2 =                        "Front One Golfing Barrel"
    CLEAR_FRONT_ONE =                           "Front One Cleared"
    MIDDLE_TWO_BARREL_1 =                       "Middle Two Fairway Barrel (Hole 1)"
    MIDDLE_TWO_BARREL_2 =                       "Middle Two Fairway Barrel (Hole 2)"
    MIDDLE_TWO_BARREL_3 =                       "Middle Two Golfing Barrel (Hole 1)"
    MIDDLE_TWO_BARREL_4 =                       "Middle Two Golfing Barrel (Hole 2)"
    CLEAR_MIDDLE_TWO =                          "Middle Two Cleared"
    BACK_THREE_BARREL_1 =                       "Back Three Fairway Barrel (Hole 1)"
    BACK_THREE_BARREL_2 =                       "Back Three Fairway Barrel (Hole 2)"
    BACK_THREE_BARREL_3 =                       "Back Three Fairway Barrel (Hole 3)"
    BACK_THREE_BARREL_4 =                       "Back Three Golfing Barrel (Hole 1)"
    BACK_THREE_BARREL_5 =                       "Back Three Golfing Barrel (Hole 2)"
    BACK_THREE_BARREL_6 =                       "Back Three Golfing Barrel (Hole 3)"
    CLEAR_BACK_THREE =                          "Back Three Cleared"
    SELLBOT_PROOF_1 =                           "Sellbot Proof Bundle 1"
    SELLBOT_PROOF_2 =                           "Sellbot Proof Bundle 2"
    SELLBOT_PROOF_3 =                           "Sellbot Proof Bundle 3"
    SELLBOT_PROOF_4 =                           "Sellbot Proof Bundle 4"
    SELLBOT_PROOF_5 =                           "Sellbot Proof Bundle 5"
    CASHBOT_PROOF_1 =                           "Cashbot Proof Bundle 1"
    CASHBOT_PROOF_2 =                           "Cashbot Proof Bundle 2"
    CASHBOT_PROOF_3 =                           "Cashbot Proof Bundle 3"
    CASHBOT_PROOF_4 =                           "Cashbot Proof Bundle 4"
    CASHBOT_PROOF_5 =                           "Cashbot Proof Bundle 5"
    LAWBOT_PROOF_1 =                            "Lawbot Proof Bundle 1"
    LAWBOT_PROOF_2 =                            "Lawbot Proof Bundle 2"
    LAWBOT_PROOF_3 =                            "Lawbot Proof Bundle 3"
    LAWBOT_PROOF_4 =                            "Lawbot Proof Bundle 4"
    LAWBOT_PROOF_5 =                            "Lawbot Proof Bundle 5"
    BOSSBOT_PROOF_1 =                           "Bossbot Proof Bundle 1"
    BOSSBOT_PROOF_2 =                           "Bossbot Proof Bundle 2"
    BOSSBOT_PROOF_3 =                           "Bossbot Proof Bundle 3"
    BOSSBOT_PROOF_4 =                           "Bossbot Proof Bundle 4"
    BOSSBOT_PROOF_5 =                           "Bossbot Proof Bundle 5"
    SAVED_TOONTOWN =                            "Save Toontown"


class ToontownLocationType(IntEnum):
    STARTER         = auto()  # Location that is considered a "starting" check on login, typically we force checks here
    GALLERY         = auto()  # Locations for discovering cogs in the gallery
    GALLERY_MAX     = auto()  # Locations for maxing cogs in the gallery
    FACILITIES      = auto()  # Locations for clearing facilities
    BUILDINGS       = auto()  # Locations for clearing cog buildings
    BOSSES_1        = auto()  # Locations for clearing bosses
    BOSSES_2        = auto()  # Locations for clearing bosses
    BOSSES_3        = auto()  # Locations for clearing bosses
    BOSSES_4        = auto()  # Locations for clearing bosses
    BOSSES_5        = auto()  # Locations for clearing bosses
    FISHING         = auto()  # Locations for fishing trophies
    FISHING_GENUS   = auto()  # Locations for catching unique genus
    FISHING_GALLERY = auto()  # Locations for fishing gallery
    RACING          = auto()  # Locations for racing
    GOLF            = auto()  # Location for golf
    PLAYGROUND_1    = auto()  # Locations for discovering playground treasures
    PLAYGROUND_2    = auto()  # Locations for discovering playground treasures
    PLAYGROUND_3    = auto()  # Locations for discovering playground treasures
    PLAYGROUND_4    = auto()  # Locations for discovering playground treasures
    PLAYGROUND_5    = auto()  # Locations for discovering playground treasures
    PLAYGROUND_6    = auto()  # Locations for discovering playground treasures
    GAG_TRAINING    = auto()  # Locations for training gags
    PET_SHOP        = auto()  # Locations for purchasing checks from pet shop clerks
    TTC_TASKS       = auto()  # Locations for TTC tasks
    DD_TASKS        = auto()  # Locations for DD tasks
    DG_TASKS        = auto()  # Locations for DG tasks
    MML_TASKS       = auto()  # Locations for MML tasks
    TB_TASKS        = auto()  # Locations for TB tasks
    DDL_TASKS       = auto()  # Locations for DDL tasks

    MISC = auto()


@dataclass
class ToontownLocationDefinition:
    name: ToontownLocationName
    type: ToontownLocationType
    region: ToontownRegionName
    rules: List[Rule] = field(default_factory=list)       # rules for if the player can access this location
    item_rules: List[ItemRule] = field(default_factory=list)  # rules for if certain items should fill this location
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    rule_logic_or: bool = False  # By default, rule logic ANDs values in the list
    unique_id: int = 0  # Set in post


# region Treasure Location Definitions
REGION_TO_TREASURE_LOCATIONS: dict[ToontownRegionName, list[ToontownLocationName]] = {
    ToontownRegionName.TTC:  [
        ToontownLocationName.TTC_TREASURE_1,
        ToontownLocationName.TTC_TREASURE_2,
        ToontownLocationName.TTC_TREASURE_3,
        ToontownLocationName.TTC_TREASURE_4,
        ToontownLocationName.TTC_TREASURE_5,
        ToontownLocationName.TTC_TREASURE_6,
    ],
    ToontownRegionName.DD:   [
        ToontownLocationName.DD_TREASURE_1,
        ToontownLocationName.DD_TREASURE_2,
        ToontownLocationName.DD_TREASURE_3,
        ToontownLocationName.DD_TREASURE_4,
        ToontownLocationName.DD_TREASURE_5,
        ToontownLocationName.DD_TREASURE_6,
    ],
    ToontownRegionName.DG:   [
        ToontownLocationName.DG_TREASURE_1,
        ToontownLocationName.DG_TREASURE_2,
        ToontownLocationName.DG_TREASURE_3,
        ToontownLocationName.DG_TREASURE_4,
        ToontownLocationName.DG_TREASURE_5,
        ToontownLocationName.DG_TREASURE_6,
    ],
    ToontownRegionName.MML:  [
        ToontownLocationName.MML_TREASURE_1,
        ToontownLocationName.MML_TREASURE_2,
        ToontownLocationName.MML_TREASURE_3,
        ToontownLocationName.MML_TREASURE_4,
        ToontownLocationName.MML_TREASURE_5,
        ToontownLocationName.MML_TREASURE_6,
    ],
    ToontownRegionName.TB:   [
        ToontownLocationName.TB_TREASURE_1,
        ToontownLocationName.TB_TREASURE_2,
        ToontownLocationName.TB_TREASURE_3,
        ToontownLocationName.TB_TREASURE_4,
        ToontownLocationName.TB_TREASURE_5,
        ToontownLocationName.TB_TREASURE_6,
    ],
    ToontownRegionName.DDL:  [
        ToontownLocationName.DDL_TREASURE_1,
        ToontownLocationName.DDL_TREASURE_2,
        ToontownLocationName.DDL_TREASURE_3,
        ToontownLocationName.DDL_TREASURE_4,
        ToontownLocationName.DDL_TREASURE_5,
        ToontownLocationName.DDL_TREASURE_6,
    ],
    ToontownRegionName.GS:   [
        ToontownLocationName.GS_TREASURE_1,
        ToontownLocationName.GS_TREASURE_2,
        ToontownLocationName.GS_TREASURE_3,
        ToontownLocationName.GS_TREASURE_4,
        ToontownLocationName.GS_TREASURE_5,
        ToontownLocationName.GS_TREASURE_6,
    ],
    ToontownRegionName.AA:   [
        ToontownLocationName.AA_TREASURE_1,
        ToontownLocationName.AA_TREASURE_2,
        ToontownLocationName.AA_TREASURE_3,
        ToontownLocationName.AA_TREASURE_4,
        ToontownLocationName.AA_TREASURE_5,
        ToontownLocationName.AA_TREASURE_6,
    ],
    ToontownRegionName.SBHQ: [
        ToontownLocationName.SBHQ_TREASURE_1,
        ToontownLocationName.SBHQ_TREASURE_2,
        ToontownLocationName.SBHQ_TREASURE_3,
        ToontownLocationName.SBHQ_TREASURE_4,
        ToontownLocationName.SBHQ_TREASURE_5,
        ToontownLocationName.SBHQ_TREASURE_6,
    ],
    ToontownRegionName.CBHQ: [
        ToontownLocationName.CBHQ_TREASURE_1,
        ToontownLocationName.CBHQ_TREASURE_2,
        ToontownLocationName.CBHQ_TREASURE_3,
        ToontownLocationName.CBHQ_TREASURE_4,
        ToontownLocationName.CBHQ_TREASURE_5,
        ToontownLocationName.CBHQ_TREASURE_6,
    ],
    ToontownRegionName.LBHQ: [
        ToontownLocationName.LBHQ_TREASURE_1,
        ToontownLocationName.LBHQ_TREASURE_2,
        ToontownLocationName.LBHQ_TREASURE_3,
        ToontownLocationName.LBHQ_TREASURE_4,
        ToontownLocationName.LBHQ_TREASURE_5,
        ToontownLocationName.LBHQ_TREASURE_6,
    ],
    ToontownRegionName.BBHQ: [
        ToontownLocationName.BBHQ_TREASURE_1,
        ToontownLocationName.BBHQ_TREASURE_2,
        ToontownLocationName.BBHQ_TREASURE_3,
        ToontownLocationName.BBHQ_TREASURE_4,
        ToontownLocationName.BBHQ_TREASURE_5,
        ToontownLocationName.BBHQ_TREASURE_6,
    ],
}


TREASURE_LOCATION_TYPES: list[ToontownLocationType] = [
    ToontownLocationType.PLAYGROUND_1,
    ToontownLocationType.PLAYGROUND_2,
    ToontownLocationType.PLAYGROUND_3,
    ToontownLocationType.PLAYGROUND_4,
    ToontownLocationType.PLAYGROUND_5,
    ToontownLocationType.PLAYGROUND_6,
]


TREASURE_LOCATION_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(location_name,  location_type, region_name)
    for region_name in REGION_TO_TREASURE_LOCATIONS.keys()
    for location_name, location_type in zip(
        REGION_TO_TREASURE_LOCATIONS.get(region_name), TREASURE_LOCATION_TYPES
    )
]
# endregion

# region Boss Check Definitions
REGION_TO_BOSS_LOCATIONS: dict[ToontownRegionName, list[ToontownLocationName]] = {
    ToontownRegionName.SBHQ: [
        ToontownLocationName.SELLBOT_PROOF_1,
        ToontownLocationName.SELLBOT_PROOF_2,
        ToontownLocationName.SELLBOT_PROOF_3,
        ToontownLocationName.SELLBOT_PROOF_4,
        ToontownLocationName.SELLBOT_PROOF_5,
    ],
    ToontownRegionName.CBHQ: [
        ToontownLocationName.CASHBOT_PROOF_1,
        ToontownLocationName.CASHBOT_PROOF_2,
        ToontownLocationName.CASHBOT_PROOF_3,
        ToontownLocationName.CASHBOT_PROOF_4,
        ToontownLocationName.CASHBOT_PROOF_5,
    ],
    ToontownRegionName.LBHQ: [
        ToontownLocationName.LAWBOT_PROOF_1,
        ToontownLocationName.LAWBOT_PROOF_2,
        ToontownLocationName.LAWBOT_PROOF_3,
        ToontownLocationName.LAWBOT_PROOF_4,
        ToontownLocationName.LAWBOT_PROOF_5,
    ],
    ToontownRegionName.BBHQ: [
        ToontownLocationName.BOSSBOT_PROOF_1,
        ToontownLocationName.BOSSBOT_PROOF_2,
        ToontownLocationName.BOSSBOT_PROOF_3,
        ToontownLocationName.BOSSBOT_PROOF_4,
        ToontownLocationName.BOSSBOT_PROOF_5,
    ],
}

BOSS_LOCATION_TYPES: list[ToontownLocationType] = [
    ToontownLocationType.BOSSES_1,
    ToontownLocationType.BOSSES_2,
    ToontownLocationType.BOSSES_3,
    ToontownLocationType.BOSSES_4,
    ToontownLocationType.BOSSES_5,
]

REGION_TO_BOSS_RULES: dict[ToontownRegionName, list[list]] = {
    ToontownRegionName.SBHQ: [[Rule.CanFightVP], [Rule.CanFightVP], [Rule.CanFightVP], [Rule.CanFightVP], [Rule.CanFightVP]],
    ToontownRegionName.CBHQ: [[Rule.CanFightCFO], [Rule.CanFightCFO], [Rule.CanFightCFO], [Rule.CanFightCFO], [Rule.CanFightCFO]],
    ToontownRegionName.LBHQ: [[Rule.CanFightCJ], [Rule.CanFightCJ], [Rule.CanFightCJ], [Rule.CanFightCJ], [Rule.CanFightCJ]],
    ToontownRegionName.BBHQ: [[Rule.CanFightCEO], [Rule.CanFightCEO], [Rule.CanFightCEO], [Rule.CanFightCEO], [Rule.CanFightCEO]]
}

BOSS_LOCATION_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(location_name,  location_type, region_name, rule_set, [ItemRule.RestrictDisguises])
    for region_name in REGION_TO_BOSS_LOCATIONS.keys()
    for location_name, location_type, rule_set in zip(
        REGION_TO_BOSS_LOCATIONS.get(region_name), BOSS_LOCATION_TYPES, REGION_TO_BOSS_RULES.get(region_name)
    )
]
# endregion

LOCATION_DEFINITIONS: List[ToontownLocationDefinition] = [
    # region Login Locations
    ToontownLocationDefinition(ToontownLocationName.STARTING_NEW_GAME,  ToontownLocationType.STARTER, ToontownRegionName.LOGIN),
    ToontownLocationDefinition(ToontownLocationName.STARTING_TRACK_ONE, ToontownLocationType.STARTER, ToontownRegionName.LOGIN),
    ToontownLocationDefinition(ToontownLocationName.STARTING_TRACK_TWO, ToontownLocationType.STARTER, ToontownRegionName.LOGIN),
    # endregion
    # region Cog Gallery Defeated
    ToontownLocationDefinition(ToontownLocationName.COLD_CALLER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.SHORT_CHANGE_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.BOTTOM_FEEDER_DEFEATED,     ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.FLUNKY_DEFEATED,            ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.TELEMARKETER_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.PENNY_PINCHER_DEFEATED,     ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.BLOODSUCKER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.PENCIL_PUSHER_DEFEATED,     ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.NAME_DROPPER_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.TIGHTWAD_DEFEATED,          ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.DOUBLE_TALKER_DEFEATED,     ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.YESMAN_DEFEATED,            ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.GLAD_HANDER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.BEAN_COUNTER_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.AMBULANCE_CHASER_DEFEATED,  ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.MICROMANAGER_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.MOVER_AND_SHAKER_DEFEATED,  ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.NUMBER_CRUNCHER_DEFEATED,   ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.BACKSTABBER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.DOWNSIZER_DEFEATED,         ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.TWO_FACE_DEFEATED,          ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.MONEY_BAGS_DEFEATED,        ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.SPIN_DOCTOR_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.HEAD_HUNTER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.MINGLER_DEFEATED,           ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.LOAN_SHARK_DEFEATED,        ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.LEGAL_EAGLE_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.CORPORATE_RAIDER_DEFEATED,  ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MR_HOLLYWOOD_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.ROBBER_BARRON_DEFEATED,     ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_WIG_DEFEATED,           ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_CHEESE_DEFEATED,        ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierEightBossbot]),
    # endregion
    # region Cog Gallery Maxing
    ToontownLocationDefinition(ToontownLocationName.COLD_CALLER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.SHORT_CHANGE_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.BOTTOM_FEEDER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.FLUNKY_MAXED,               ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.TELEMARKETER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.PENNY_PINCHER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.BLOODSUCKER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.PENCIL_PUSHER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.NAME_DROPPER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.TIGHTWAD_MAXED,             ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.DOUBLE_TALKER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.YESMAN_MAXED,               ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.GLAD_HANDER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.BEAN_COUNTER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.AMBULANCE_CHASER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.MICROMANAGER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.MOVER_AND_SHAKER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.NUMBER_CRUNCHER_MAXED,      ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.BACKSTABBER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.DOWNSIZER_MAXED,            ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.TWO_FACE_MAXED,             ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.MONEY_BAGS_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.SPIN_DOCTOR_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.HEAD_HUNTER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.MINGLER_MAXED,              ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.LOAN_SHARK_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.LEGAL_EAGLE_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.CORPORATE_RAIDER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MR_HOLLYWOOD_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.ROBBER_BARRON_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_WIG_MAXED,              ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_CHEESE_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightBossbot]),
    # endregion
    # region racing
    ToontownLocationDefinition(ToontownLocationName.SPEEDWAY_1_CLEAR,           ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.SPEEDWAY_1_QUALIFY,         ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.SPEEDWAY_2_CLEAR,           ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.SPEEDWAY_2_QUALIFY,         ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.RURAL_1_CLEAR,              ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.RURAL_1_QUALIFY,            ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.RURAL_2_CLEAR,              ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.RURAL_2_QUALIFY,            ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.URBAN_1_CLEAR,              ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.URBAN_1_QUALIFY,            ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.URBAN_2_CLEAR,              ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    ToontownLocationDefinition(ToontownLocationName.URBAN_2_QUALIFY,            ToontownLocationType.RACING, ToontownRegionName.GS, [Rule.CanReachGS, Rule.Racing]),
    # endregion
    # region Minigolf
    ToontownLocationDefinition(ToontownLocationName.EASY_GOLF_1,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.EASY_GOLF_2,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.EASY_GOLF_3,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.MED_GOLF_1,            ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.MED_GOLF_2,            ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.MED_GOLF_3,            ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.MED_GOLF_4,            ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.MED_GOLF_5,            ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.MED_GOLF_6,            ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_1,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_2,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_3,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_4,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_5,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_6,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_7,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_8,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    ToontownLocationDefinition(ToontownLocationName.HARD_GOLF_9,           ToontownLocationType.GOLF, ToontownRegionName.AA, [Rule.CanReachAA, Rule.Golfing]),
    # endregion
    # region Fishing
    ToontownLocationDefinition(ToontownLocationName.BALLOON_FISH_0,         ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BALLOON_FISH_1,         ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BALLOON_FISH_2,         ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BALLOON_FISH_3,         ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BALLOON_FISH_4,         ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.JELLYFISH_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.JELLYFISH_1,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.JELLYFISH_2,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.JELLYFISH_3,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.JELLYFISH_4,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CAT_FISH_0,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CAT_FISH_1,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CAT_FISH_2,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CAT_FISH_3,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CAT_FISH_4,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CLOWN_FISH_0,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CLOWN_FISH_1,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CLOWN_FISH_2,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CLOWN_FISH_3,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.FROZEN_FISH_0,          ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.STAR_FISH_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.STAR_FISH_1,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.STAR_FISH_2,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.STAR_FISH_3,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.STAR_FISH_4,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.HOLEY_MACKEREL_0,       ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.DOG_FISH_0,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.DOG_FISH_1,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.DOG_FISH_2,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.DOG_FISH_3,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.DOG_FISH_4,             ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.DEVIL_RAY_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.AMORE_EEL_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.AMORE_EEL_1,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.NURSE_SHARK_0,          ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.NURSE_SHARK_1,          ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.NURSE_SHARK_2,          ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.KING_CRAB_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.KING_CRAB_1,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.KING_CRAB_2,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.MOON_FISH_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.MOON_FISH_1,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.MOON_FISH_2,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.MOON_FISH_3,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.MOON_FISH_4,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.MOON_FISH_5,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.SEA_HORSE_0,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.SEA_HORSE_1,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.SEA_HORSE_2,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.SEA_HORSE_3,            ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.POOL_SHARK_0,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.POOL_SHARK_1,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.POOL_SHARK_2,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.POOL_SHARK_3,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_0,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_1,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_2,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_3,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_4,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_5,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_6,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.BEAR_ACUDA_7,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CUTTHROAT_TROUT_0,      ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CUTTHROAT_TROUT_1,      ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.CUTTHROAT_TROUT_2,      ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.PIANO_TUNA_0,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.PIANO_TUNA_1,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.PIANO_TUNA_2,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.PIANO_TUNA_3,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.PIANO_TUNA_4,           ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.FishCatch]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_BALLOON_FISH,     ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_JELLYFISH,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_CAT_FISH,         ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_CLOWN_FISH,       ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_FROZEN_FISH,      ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_STAR_FISH,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_HOLEY_MACKEREL,   ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_DOG_FISH,         ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_DEVIL_RAY,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_AMORE_EEL,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_NURSE_SHARK,      ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_KING_CRAB,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_MOON_FISH,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_SEA_HORSE,        ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_POOL_SHARK,       ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_BEAR_ACUDA,       ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_CUTTHROAT_TROUT,  ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.GENUS_PIANO_TUNA,       ToontownLocationType.FISHING_GENUS, ToontownRegionName.FISHING, [Rule.FishGenus]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_10_SPECIES,     ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_20_SPECIES,     ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_30_SPECIES,     ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_40_SPECIES,     ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_50_SPECIES,     ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_60_SPECIES,     ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_COMPLETE_ALBUM, ToontownLocationType.FISHING_GALLERY, ToontownRegionName.FISHING, [Rule.FishGallery]),
    # endregion
    # region shopping
    ToontownLocationDefinition(ToontownLocationName.TTC_SHOP_1,  ToontownLocationType.PET_SHOP, ToontownRegionName.TTC, [Rule.CanReachTTC, Rule.CanBuyTTCDoodle]),
    ToontownLocationDefinition(ToontownLocationName.TTC_SHOP_2,  ToontownLocationType.PET_SHOP, ToontownRegionName.TTC, [Rule.CanReachTTC, Rule.CanBuyTTCDoodle]),
    ToontownLocationDefinition(ToontownLocationName.TTC_SHOP_3,  ToontownLocationType.PET_SHOP, ToontownRegionName.TTC, [Rule.CanReachTTC, Rule.CanBuyTTCDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DD_SHOP_1,  ToontownLocationType.PET_SHOP, ToontownRegionName.DD, [Rule.CanReachDD, Rule.CanBuyDDDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DD_SHOP_2,  ToontownLocationType.PET_SHOP, ToontownRegionName.DD, [Rule.CanReachDD, Rule.CanBuyDDDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DD_SHOP_3,  ToontownLocationType.PET_SHOP, ToontownRegionName.DD, [Rule.CanReachDD, Rule.CanBuyDDDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DG_SHOP_1,  ToontownLocationType.PET_SHOP, ToontownRegionName.DG, [Rule.CanReachDG, Rule.CanBuyDGDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DG_SHOP_2,  ToontownLocationType.PET_SHOP, ToontownRegionName.DG, [Rule.CanReachDG, Rule.CanBuyDGDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DG_SHOP_3,  ToontownLocationType.PET_SHOP, ToontownRegionName.DG, [Rule.CanReachDG, Rule.CanBuyDGDoodle]),
    ToontownLocationDefinition(ToontownLocationName.MML_SHOP_1,  ToontownLocationType.PET_SHOP, ToontownRegionName.MML, [Rule.CanReachMML, Rule.CanBuyMMLDoodle]),
    ToontownLocationDefinition(ToontownLocationName.MML_SHOP_2,  ToontownLocationType.PET_SHOP, ToontownRegionName.MML, [Rule.CanReachMML, Rule.CanBuyMMLDoodle]),
    ToontownLocationDefinition(ToontownLocationName.MML_SHOP_3,  ToontownLocationType.PET_SHOP, ToontownRegionName.MML, [Rule.CanReachMML, Rule.CanBuyMMLDoodle]),
    ToontownLocationDefinition(ToontownLocationName.TB_SHOP_1,  ToontownLocationType.PET_SHOP, ToontownRegionName.TB, [Rule.CanReachTB, Rule.CanBuyTBDoodle]),
    ToontownLocationDefinition(ToontownLocationName.TB_SHOP_2,  ToontownLocationType.PET_SHOP, ToontownRegionName.TB, [Rule.CanReachTB, Rule.CanBuyTBDoodle]),
    ToontownLocationDefinition(ToontownLocationName.TB_SHOP_3,  ToontownLocationType.PET_SHOP, ToontownRegionName.TB, [Rule.CanReachTB, Rule.CanBuyTBDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DDL_SHOP_1,  ToontownLocationType.PET_SHOP, ToontownRegionName.DDL, [Rule.CanReachDDL, Rule.CanBuyDDLDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DDL_SHOP_2,  ToontownLocationType.PET_SHOP, ToontownRegionName.DDL, [Rule.CanReachDDL, Rule.CanBuyDDLDoodle]),
    ToontownLocationDefinition(ToontownLocationName.DDL_SHOP_3,  ToontownLocationType.PET_SHOP, ToontownRegionName.DDL, [Rule.CanReachDDL, Rule.CanBuyDDLDoodle]),
    # endregion
    # region Tasking
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_1,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_2,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_3,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_4,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_5,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_6,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_7,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_8,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_9,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_10,   ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_11,   ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_12,   ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_1,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_2,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_3,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_4,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_5,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_6,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_7,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_8,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_9,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_10,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_11,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_12,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_1,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_2,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_3,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_4,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_5,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_6,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_7,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_8,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_9,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.CanReachSBHQ, Rule.CanReachLBHQ]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_10,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_11,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_12,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_1,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_2,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_3,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_4,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_5,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_6,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_7,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_8,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_9,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_10, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_11, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_12, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_1,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_2,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_3,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_4,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_5,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_6,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.TierEightSellbot, Rule.TierEightCashbot, Rule.TierEightLawbot, Rule.TierEightBossbot]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_7,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_8,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_9,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_10,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_11,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_12,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_1,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_2,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_3,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_4,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_5,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_6,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.TierEightSellbot, Rule.TierEightCashbot, Rule.TierEightLawbot, Rule.TierEightBossbot]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_7,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_8,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_9,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.CanReachBBHQ]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_10,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_11,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_12,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag]),
    # endregion
    # region Buildings
    ToontownLocationDefinition(ToontownLocationName.ONE_STORY,                  ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelThreeOffenseGag, Rule.OneStory]),
    ToontownLocationDefinition(ToontownLocationName.TWO_STORY,                  ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.THREE_STORY,                ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFiveOffenseGag,  Rule.ThreeStory]),
    ToontownLocationDefinition(ToontownLocationName.FOUR_STORY,                 ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSixOffenseGag,   Rule.FourStory]),
    ToontownLocationDefinition(ToontownLocationName.FIVE_STORY,                 ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSevenOffenseGag, Rule.FiveStory]),
    # endregion
] + TREASURE_LOCATION_DEFINITIONS + [
    # region Facilities
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_1, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_2, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_3, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_FRONT_FACTORY,    ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_1,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_2,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_3,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_SIDE_FACTORY,     ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_1,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_2,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_3,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_COIN_MINT,        ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_1,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_2,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_3,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_DOLLAR_MINT,      ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_1,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_2,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_3,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_BULLION_MINT,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_A_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_B_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_C_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_D_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_ONE_BARREL_1,     ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_ONE_BARREL_2,     ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_FRONT_ONE,        ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_1,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_2,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_3,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_4,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_MIDDLE_TWO,       ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_1,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_2,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_3,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_4,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_5,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_6,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelEightOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_BACK_THREE,       ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelEightOffenseGag]),
    # endregion
    # region Gag Unlocks
    ToontownLocationDefinition(ToontownLocationName.TOONUP_FEATHER_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpOne]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_MEGAPHONE_UNLOCKED,    ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpTwo]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_LIPSTICK_UNLOCKED,     ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpThree]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_CANE_UNLOCKED,         ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpFour]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_PIXIE_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpFive]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_JUGGLING_UNLOCKED,     ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpSix]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_HIGHDIVE_UNLOCKED,     ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpSeven]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_BANANA_UNLOCKED,         ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapOne]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_RAKE_UNLOCKED,           ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapTwo]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_MARBLES_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapThree]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_QUICKSAND_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapFour]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_TRAPDOOR_UNLOCKED,       ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapFive]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_TNT_UNLOCKED,            ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapSix]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_TRAIN_UNLOCKED,          ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapSeven]),
    ToontownLocationDefinition(ToontownLocationName.LURE_ONEBILL_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureOne]),
    ToontownLocationDefinition(ToontownLocationName.LURE_SMALLMAGNET_UNLOCKED,    ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureTwo]),
    ToontownLocationDefinition(ToontownLocationName.LURE_FIVEBILL_UNLOCKED,       ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureThree]),
    ToontownLocationDefinition(ToontownLocationName.LURE_BIGMAGNET_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureFour]),
    ToontownLocationDefinition(ToontownLocationName.LURE_TENBILL_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureFive]),
    ToontownLocationDefinition(ToontownLocationName.LURE_HYPNO_UNLOCKED,          ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureSix]),
    ToontownLocationDefinition(ToontownLocationName.LURE_PRESENTATION_UNLOCKED,   ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureSeven]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_BIKEHORN_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundOne]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_WHISTLE_UNLOCKED,       ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundTwo]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_BUGLE_UNLOCKED,         ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundThree]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_AOOGAH_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundFour]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_TRUNK_UNLOCKED,         ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundFive]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_FOG_UNLOCKED,           ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundSix]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_OPERA_UNLOCKED,         ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundSeven]),
    ToontownLocationDefinition(ToontownLocationName.THROW_CUPCAKE_UNLOCKED,       ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowOne]),
    ToontownLocationDefinition(ToontownLocationName.THROW_FRUITPIESLICE_UNLOCKED, ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowTwo]),
    ToontownLocationDefinition(ToontownLocationName.THROW_CREAMPIESLICE_UNLOCKED, ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowThree]),
    ToontownLocationDefinition(ToontownLocationName.THROW_WHOLEFRUIT_UNLOCKED,    ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowFour]),
    ToontownLocationDefinition(ToontownLocationName.THROW_WHOLECREAM_UNLOCKED,    ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowFive]),
    ToontownLocationDefinition(ToontownLocationName.THROW_CAKE_UNLOCKED,          ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowSix]),
    ToontownLocationDefinition(ToontownLocationName.THROW_WEDDING_UNLOCKED,       ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowSeven]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_SQUIRTFLOWER_UNLOCKED, ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtOne]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_GLASS_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtTwo]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_SQUIRTGUN_UNLOCKED,    ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtThree]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_SELTZER_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtFour]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_HOSE_UNLOCKED,         ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtFive]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_CLOUD_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtSix]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_GEYSER_UNLOCKED,       ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtSeven]),
    ToontownLocationDefinition(ToontownLocationName.DROP_FLOWERPOT_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropOne]),
    ToontownLocationDefinition(ToontownLocationName.DROP_SANDBAG_UNLOCKED,        ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropTwo]),
    ToontownLocationDefinition(ToontownLocationName.DROP_ANVIL_UNLOCKED,          ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropThree]),
    ToontownLocationDefinition(ToontownLocationName.DROP_BIGWEIGHT_UNLOCKED,      ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropFour]),
    ToontownLocationDefinition(ToontownLocationName.DROP_SAFE_UNLOCKED,           ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropFive]),
    ToontownLocationDefinition(ToontownLocationName.DROP_PIANO_UNLOCKED,          ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropSix]),
    ToontownLocationDefinition(ToontownLocationName.DROP_BOAT_UNLOCKED,           ToontownLocationType.GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropSeven]),
    # endregion
    ] + BOSS_LOCATION_DEFINITIONS

LOCATION_NAME_TO_DEFINITION: dict[ToontownLocationName, ToontownLocationDefinition] = {
    locdef.name: locdef for locdef in LOCATION_DEFINITIONS
}

EVENT_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(ToontownLocationName.SAVED_TOONTOWN, ToontownLocationType.MISC,   ToontownRegionName.TTC, [Rule.CanWinGame]),
]


for i in range(len(LOCATION_DEFINITIONS)):
    LOCATION_DEFINITIONS[i].unique_id = i + consts.BASE_ID

LOCATION_DESCRIPTIONS: Dict[str, str] = {

}

FISH_LOCATIONS = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.FISHING]
SHOP_LOCATIONS = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.PET_SHOP]

TTC_TASK_LOCATIONS = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.TTC_TASKS]
DD_TASK_LOCATIONS  = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.DD_TASKS]
DG_TASK_LOCATIONS  = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.DG_TASKS]
MML_TASK_LOCATIONS = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.MML_TASKS]
TB_TASK_LOCATIONS  = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.TB_TASKS]
DDL_TASK_LOCATIONS = [loc_def.name for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.DDL_TASKS]
ALL_TASK_LOCATIONS_SPLIT = (
    TTC_TASK_LOCATIONS, DD_TASK_LOCATIONS, DG_TASK_LOCATIONS,
    MML_TASK_LOCATIONS, TB_TASK_LOCATIONS, DDL_TASK_LOCATIONS,
)
ALL_TASK_LOCATIONS = (
    TTC_TASK_LOCATIONS + DD_TASK_LOCATIONS + DG_TASK_LOCATIONS
    + MML_TASK_LOCATIONS + TB_TASK_LOCATIONS + DDL_TASK_LOCATIONS
)

SCOUTING_REQUIRED_LOCATIONS = ALL_TASK_LOCATIONS.copy() + SHOP_LOCATIONS.copy()

LOCATION_NAME_TO_ID = {location.name.value: i + consts.BASE_ID for i, location in enumerate(LOCATION_DEFINITIONS)}
LOCATION_ID_TO_NAME = {i + consts.BASE_ID: location.name.value for i, location in enumerate(LOCATION_DEFINITIONS)}


def get_location_def_from_name(name: ToontownLocationName) -> ToontownLocationDefinition:
    return LOCATION_NAME_TO_DEFINITION[name]
