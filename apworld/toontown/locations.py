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
    LEVEL_ONE_COG_DEFEATED =                    "Level 1 Cog Defeated"
    LEVEL_TWO_COG_DEFEATED =                    "Level 2 Cog Defeated"
    LEVEL_THREE_COG_DEFEATED =                  "Level 3 Cog Defeated"
    LEVEL_FOUR_COG_DEFEATED =                   "Level 4 Cog Defeated"
    LEVEL_FIVE_COG_DEFEATED =                   "Level 5 Cog Defeated"
    LEVEL_SIX_COG_DEFEATED =                    "Level 6 Cog Defeated"
    LEVEL_SEVEN_COG_DEFEATED =                  "Level 7 Cog Defeated"
    LEVEL_EIGHT_COG_DEFEATED =                  "Level 8 Cog Defeated"
    LEVEL_NINE_COG_DEFEATED =                   "Level 9 Cog Defeated"
    LEVEL_TEN_COG_DEFEATED =                    "Level 10 Cog Defeated"
    LEVEL_ELEVEN_COG_DEFEATED =                 "Level 11 Cog Defeated"
    LEVEL_TWELVE_COG_DEFEATED =                 "Level 12 Cog Defeated"
    LEVEL_THIRTEEN_COG_DEFEATED =               "Level 13 Cog Defeated"
    LEVEL_FOURTEEN_COG_DEFEATED =               "Level 14 Cog Defeated"
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
    DOG_FISH_3 =                                "Dalmatian Dog Fish"
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
    URBAN_2_CLEAR =                             "Blizzard Boulevard Cleared"
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
    ONE_STORY_FIRST_FLOOR =                     "One Story Building First Floor"
    TWO_STORY_FIRST_FLOOR =                     "Two Story Building First Floor"
    TWO_STORY_SECOND_FLOOR =                    "Two Story Building Second Floor"
    THREE_STORY_FIRST_FLOOR =                   "Three Story Building First Floor"
    THREE_STORY_SECOND_FLOOR =                  "Three Story Building Second Floor"
    THREE_STORY_THIRD_FLOOR =                   "Three Story Building Third Floor"
    FOUR_STORY_FIRST_FLOOR =                    "Four Story Building First Floor"
    FOUR_STORY_SECOND_FLOOR =                   "Four Story Building Second Floor"
    FOUR_STORY_THIRD_FLOOR =                    "Four Story Building Third Floor"
    FOUR_STORY_FOURTH_FLOOR =                   "Four Story Building Fourth Floor"
    FIVE_STORY_FIRST_FLOOR =                    "Five Story Building First Floor"
    FIVE_STORY_SECOND_FLOOR =                   "Five Story Building Second Floor"
    FIVE_STORY_THIRD_FLOOR =                    "Five Story Building Third Floor"
    FIVE_STORY_FOURTH_FLOOR =                   "Five Story Building Fourth Floor"
    FIVE_STORY_FIFTH_FLOOR =                    "Five Story Building Fifth Floor"
    TOONTOWN_CENTRAL_BUILDING =                 "Toontown Central Building Cleared"
    DONALDS_DOCK_BUILDING =                     "Donald's Dock Building Cleared"
    DAISYS_GARDENS_BUILDING =                   "Daisy Gardens Building Cleared"
    MINNIES_MELODYLAND_BUILDING =               "Minnie's Melodyland Building Cleared"
    THE_BRRRGH_BUILDING =                       "The Brrrgh Building Cleared"
    DONALDS_DREAMLAND_BUILDING =                "Donald's Dreamland Building Cleared"
    BOSSBOT_BUILDING =                          "Bossbot Building Cleared"
    LAWBOT_BUILDING =                           "Lawbot Building Cleared"
    CASHBOT_BUILDING =                          "Cashbot Building Cleared"
    SELLBOT_BUILDING =                          "Sellbot Building Cleared"
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
    LOOPY_JOKE_1 =                              "Loopy Lane Knock Knock Joke 1"
    LOOPY_JOKE_2 =                              "Loopy Lane Knock Knock Joke 2"
    LOOPY_JOKE_3 =                              "Loopy Lane Knock Knock Joke 3"
    LOOPY_JOKE_4 =                              "Loopy Lane Knock Knock Joke 4"
    LOOPY_JOKE_5 =                              "Loopy Lane Knock Knock Joke 5"
    LOOPY_JOKE_6 =                              "Loopy Lane Knock Knock Joke 6"
    LOOPY_JOKE_7 =                              "Loopy Lane Knock Knock Joke 7"
    LOOPY_JOKE_8 =                              "Loopy Lane Knock Knock Joke 8"
    LOOPY_JOKE_9 =                              "Loopy Lane Knock Knock Joke 9"
    LOOPY_JOKE_10 =                             "Loopy Lane Knock Knock Joke 10"
    PUNCHLINE_JOKE_1 =                          "Punchline Place Knock Knock Joke 1"
    PUNCHLINE_JOKE_2 =                          "Punchline Place Knock Knock Joke 2"
    PUNCHLINE_JOKE_3 =                          "Punchline Place Knock Knock Joke 3"
    PUNCHLINE_JOKE_4 =                          "Punchline Place Knock Knock Joke 4"
    PUNCHLINE_JOKE_5 =                          "Punchline Place Knock Knock Joke 5"
    PUNCHLINE_JOKE_6 =                          "Punchline Place Knock Knock Joke 6"
    PUNCHLINE_JOKE_7 =                          "Punchline Place Knock Knock Joke 7"
    PUNCHLINE_JOKE_8 =                          "Punchline Place Knock Knock Joke 8"
    PUNCHLINE_JOKE_9 =                          "Punchline Place Knock Knock Joke 9"
    PUNCHLINE_JOKE_10 =                         "Punchline Place Knock Knock Joke 10"
    SILLY_JOKE_1 =                              "Silly Street Knock Knock Joke 1"
    SILLY_JOKE_2 =                              "Silly Street Knock Knock Joke 2"
    SILLY_JOKE_3 =                              "Silly Street Knock Knock Joke 3"
    SILLY_JOKE_4 =                              "Silly Street Knock Knock Joke 4"
    SILLY_JOKE_5 =                              "Silly Street Knock Knock Joke 5"
    SILLY_JOKE_6 =                              "Silly Street Knock Knock Joke 6"
    SILLY_JOKE_7 =                              "Silly Street Knock Knock Joke 7"
    SILLY_JOKE_8 =                              "Silly Street Knock Knock Joke 8"
    SILLY_JOKE_9 =                              "Silly Street Knock Knock Joke 9"
    SILLY_JOKE_10 =                             "Silly Street Knock Knock Joke 10"
    BARNACLE_JOKE_1 =                           "Barnacle Boulevard Knock Knock Joke 1"
    BARNACLE_JOKE_2 =                           "Barnacle Boulevard Knock Knock Joke 2"
    BARNACLE_JOKE_3 =                           "Barnacle Boulevard Knock Knock Joke 3"
    BARNACLE_JOKE_4 =                           "Barnacle Boulevard Knock Knock Joke 4"
    BARNACLE_JOKE_5 =                           "Barnacle Boulevard Knock Knock Joke 5"
    BARNACLE_JOKE_6 =                           "Barnacle Boulevard Knock Knock Joke 6"
    BARNACLE_JOKE_7 =                           "Barnacle Boulevard Knock Knock Joke 7"
    BARNACLE_JOKE_8 =                           "Barnacle Boulevard Knock Knock Joke 8"
    BARNACLE_JOKE_9 =                           "Barnacle Boulevard Knock Knock Joke 9"
    BARNACLE_JOKE_10 =                          "Barnacle Boulevard Knock Knock Joke 10"
    SEAWEED_JOKE_1 =                            "Seaweed Street Knock Knock Joke 1"
    SEAWEED_JOKE_2 =                            "Seaweed Street Knock Knock Joke 2"
    SEAWEED_JOKE_3 =                            "Seaweed Street Knock Knock Joke 3"
    SEAWEED_JOKE_4 =                            "Seaweed Street Knock Knock Joke 4"
    SEAWEED_JOKE_5 =                            "Seaweed Street Knock Knock Joke 5"
    SEAWEED_JOKE_6 =                            "Seaweed Street Knock Knock Joke 6"
    SEAWEED_JOKE_7 =                            "Seaweed Street Knock Knock Joke 7"
    SEAWEED_JOKE_8 =                            "Seaweed Street Knock Knock Joke 8"
    SEAWEED_JOKE_9 =                            "Seaweed Street Knock Knock Joke 9"
    SEAWEED_JOKE_10 =                           "Seaweed Street Knock Knock Joke 10"
    LIGHTHOUSE_JOKE_1 =                         "Lighthouse Lane Knock Knock Joke 1"
    LIGHTHOUSE_JOKE_2 =                         "Lighthouse Lane Knock Knock Joke 2"
    LIGHTHOUSE_JOKE_3 =                         "Lighthouse Lane Knock Knock Joke 3"
    LIGHTHOUSE_JOKE_4 =                         "Lighthouse Lane Knock Knock Joke 4"
    LIGHTHOUSE_JOKE_5 =                         "Lighthouse Lane Knock Knock Joke 5"
    LIGHTHOUSE_JOKE_6 =                         "Lighthouse Lane Knock Knock Joke 6"
    LIGHTHOUSE_JOKE_7 =                         "Lighthouse Lane Knock Knock Joke 7"
    LIGHTHOUSE_JOKE_8 =                         "Lighthouse Lane Knock Knock Joke 8"
    LIGHTHOUSE_JOKE_9 =                         "Lighthouse Lane Knock Knock Joke 9"
    LIGHTHOUSE_JOKE_10 =                        "Lighthouse Lane Knock Knock Joke 10"
    ELM_JOKE_1 =                                "Elm Street Knock Knock Joke 1"
    ELM_JOKE_2 =                                "Elm Street Knock Knock Joke 2"
    ELM_JOKE_3 =                                "Elm Street Knock Knock Joke 3"
    ELM_JOKE_4 =                                "Elm Street Knock Knock Joke 4"
    ELM_JOKE_5 =                                "Elm Street Knock Knock Joke 5"
    ELM_JOKE_6 =                                "Elm Street Knock Knock Joke 6"
    ELM_JOKE_7 =                                "Elm Street Knock Knock Joke 7"
    ELM_JOKE_8 =                                "Elm Street Knock Knock Joke 8"
    ELM_JOKE_9 =                                "Elm Street Knock Knock Joke 9"
    ELM_JOKE_10 =                               "Elm Street Knock Knock Joke 10"
    MAPLE_JOKE_1 =                              "Maple Street Knock Knock Joke 1"
    MAPLE_JOKE_2 =                              "Maple Street Knock Knock Joke 2"
    MAPLE_JOKE_3 =                              "Maple Street Knock Knock Joke 3"
    MAPLE_JOKE_4 =                              "Maple Street Knock Knock Joke 4"
    MAPLE_JOKE_5 =                              "Maple Street Knock Knock Joke 5"
    MAPLE_JOKE_6 =                              "Maple Street Knock Knock Joke 6"
    MAPLE_JOKE_7 =                              "Maple Street Knock Knock Joke 7"
    MAPLE_JOKE_8 =                              "Maple Street Knock Knock Joke 8"
    MAPLE_JOKE_9 =                              "Maple Street Knock Knock Joke 9"
    MAPLE_JOKE_10 =                             "Maple Street Knock Knock Joke 10"
    OAK_JOKE_1 =                                "Oak Street Knock Knock Joke 1"
    OAK_JOKE_2 =                                "Oak Street Knock Knock Joke 2"
    OAK_JOKE_3 =                                "Oak Street Knock Knock Joke 3"
    OAK_JOKE_4 =                                "Oak Street Knock Knock Joke 4"
    OAK_JOKE_5 =                                "Oak Street Knock Knock Joke 5"
    OAK_JOKE_6 =                                "Oak Street Knock Knock Joke 6"
    OAK_JOKE_7 =                                "Oak Street Knock Knock Joke 7"
    OAK_JOKE_8 =                                "Oak Street Knock Knock Joke 8"
    OAK_JOKE_9 =                                "Oak Street Knock Knock Joke 9"
    OAK_JOKE_10 =                               "Oak Street Knock Knock Joke 10"
    ALTO_JOKE_1 =                               "Alto Avenue Knock Knock Joke 1"
    ALTO_JOKE_2 =                               "Alto Avenue Knock Knock Joke 2"
    ALTO_JOKE_3 =                               "Alto Avenue Knock Knock Joke 3"
    ALTO_JOKE_4 =                               "Alto Avenue Knock Knock Joke 4"
    ALTO_JOKE_5 =                               "Alto Avenue Knock Knock Joke 5"
    ALTO_JOKE_6 =                               "Alto Avenue Knock Knock Joke 6"
    ALTO_JOKE_7 =                               "Alto Avenue Knock Knock Joke 7"
    ALTO_JOKE_8 =                               "Alto Avenue Knock Knock Joke 8"
    ALTO_JOKE_9 =                               "Alto Avenue Knock Knock Joke 9"
    ALTO_JOKE_10 =                              "Alto Avenue Knock Knock Joke 10"
    BARITONE_JOKE_1 =                           "Baritone Boulevard Knock Knock Joke 1"
    BARITONE_JOKE_2 =                           "Baritone Boulevard Knock Knock Joke 2"
    BARITONE_JOKE_3 =                           "Baritone Boulevard Knock Knock Joke 3"
    BARITONE_JOKE_4 =                           "Baritone Boulevard Knock Knock Joke 4"
    BARITONE_JOKE_5 =                           "Baritone Boulevard Knock Knock Joke 5"
    BARITONE_JOKE_6 =                           "Baritone Boulevard Knock Knock Joke 6"
    BARITONE_JOKE_7 =                           "Baritone Boulevard Knock Knock Joke 7"
    BARITONE_JOKE_8 =                           "Baritone Boulevard Knock Knock Joke 8"
    BARITONE_JOKE_9 =                           "Baritone Boulevard Knock Knock Joke 9"
    BARITONE_JOKE_10 =                          "Baritone Boulevard Knock Knock Joke 10"
    TENOR_JOKE_1 =                              "Tenor Terrace Knock Knock Joke 1"
    TENOR_JOKE_2 =                              "Tenor Terrace Knock Knock Joke 2"
    TENOR_JOKE_3 =                              "Tenor Terrace Knock Knock Joke 3"
    TENOR_JOKE_4 =                              "Tenor Terrace Knock Knock Joke 4"
    TENOR_JOKE_5 =                              "Tenor Terrace Knock Knock Joke 5"
    TENOR_JOKE_6 =                              "Tenor Terrace Knock Knock Joke 6"
    TENOR_JOKE_7 =                              "Tenor Terrace Knock Knock Joke 7"
    TENOR_JOKE_8 =                              "Tenor Terrace Knock Knock Joke 8"
    TENOR_JOKE_9 =                              "Tenor Terrace Knock Knock Joke 9"
    TENOR_JOKE_10 =                             "Tenor Terrace Knock Knock Joke 10"
    SLEET_JOKE_1 =                              "Sleet Street Knock Knock Joke 1"
    SLEET_JOKE_2 =                              "Sleet Street Knock Knock Joke 2"
    SLEET_JOKE_3 =                              "Sleet Street Knock Knock Joke 3"
    SLEET_JOKE_4 =                              "Sleet Street Knock Knock Joke 4"
    SLEET_JOKE_5 =                              "Sleet Street Knock Knock Joke 5"
    SLEET_JOKE_6 =                              "Sleet Street Knock Knock Joke 6"
    SLEET_JOKE_7 =                              "Sleet Street Knock Knock Joke 7"
    SLEET_JOKE_8 =                              "Sleet Street Knock Knock Joke 8"
    SLEET_JOKE_9 =                              "Sleet Street Knock Knock Joke 9"
    SLEET_JOKE_10 =                             "Sleet Street Knock Knock Joke 10"
    WALRUS_JOKE_1 =                             "Walrus Way Knock Knock Joke 1"
    WALRUS_JOKE_2 =                             "Walrus Way Knock Knock Joke 2"
    WALRUS_JOKE_3 =                             "Walrus Way Knock Knock Joke 3"
    WALRUS_JOKE_4 =                             "Walrus Way Knock Knock Joke 4"
    WALRUS_JOKE_5 =                             "Walrus Way Knock Knock Joke 5"
    WALRUS_JOKE_6 =                             "Walrus Way Knock Knock Joke 6"
    WALRUS_JOKE_7 =                             "Walrus Way Knock Knock Joke 7"
    WALRUS_JOKE_8 =                             "Walrus Way Knock Knock Joke 8"
    WALRUS_JOKE_9 =                             "Walrus Way Knock Knock Joke 9"
    WALRUS_JOKE_10 =                            "Walrus Way Knock Knock Joke 10"
    POLAR_JOKE_1 =                              "Polar Place Knock Knock Joke 1"
    POLAR_JOKE_2 =                              "Polar Place Knock Knock Joke 2"
    POLAR_JOKE_3 =                              "Polar Place Knock Knock Joke 3"
    POLAR_JOKE_4 =                              "Polar Place Knock Knock Joke 4"
    POLAR_JOKE_5 =                              "Polar Place Knock Knock Joke 5"
    POLAR_JOKE_6 =                              "Polar Place Knock Knock Joke 6"
    POLAR_JOKE_7 =                              "Polar Place Knock Knock Joke 7"
    POLAR_JOKE_8 =                              "Polar Place Knock Knock Joke 8"
    POLAR_JOKE_9 =                              "Polar Place Knock Knock Joke 9"
    POLAR_JOKE_10 =                             "Polar Place Knock Knock Joke 10"
    LULLABY_JOKE_1 =                            "Lullaby Lane Knock Knock Joke 1"
    LULLABY_JOKE_2 =                            "Lullaby Lane Knock Knock Joke 2"
    LULLABY_JOKE_3 =                            "Lullaby Lane Knock Knock Joke 3"
    LULLABY_JOKE_4 =                            "Lullaby Lane Knock Knock Joke 4"
    LULLABY_JOKE_5 =                            "Lullaby Lane Knock Knock Joke 5"
    LULLABY_JOKE_6 =                            "Lullaby Lane Knock Knock Joke 6"
    LULLABY_JOKE_7 =                            "Lullaby Lane Knock Knock Joke 7"
    LULLABY_JOKE_8 =                            "Lullaby Lane Knock Knock Joke 8"
    LULLABY_JOKE_9 =                            "Lullaby Lane Knock Knock Joke 9"
    LULLABY_JOKE_10 =                           "Lullaby Lane Knock Knock Joke 10"
    PAJAMA_JOKE_1 =                             "Pajama Place Knock Knock Joke 1"
    PAJAMA_JOKE_2 =                             "Pajama Place Knock Knock Joke 2"
    PAJAMA_JOKE_3 =                             "Pajama Place Knock Knock Joke 3"
    PAJAMA_JOKE_4 =                             "Pajama Place Knock Knock Joke 4"
    PAJAMA_JOKE_5 =                             "Pajama Place Knock Knock Joke 5"
    PAJAMA_JOKE_6 =                             "Pajama Place Knock Knock Joke 6"
    PAJAMA_JOKE_7 =                             "Pajama Place Knock Knock Joke 7"
    PAJAMA_JOKE_8 =                             "Pajama Place Knock Knock Joke 8"
    PAJAMA_JOKE_9 =                             "Pajama Place Knock Knock Joke 9"
    PAJAMA_JOKE_10 =                            "Pajama Place Knock Knock Joke 10"
    FRONT_FACTORY_BARREL_1 =                    "Front Factory West Silo Barrel"
    FRONT_FACTORY_BARREL_2 =                    "Front Factory East Silo Barrel"
    FRONT_FACTORY_BARREL_3 =                    "Front Factory Warehouse Barrel"
    FRONT_FACTORY_BARREL_4 =                    "Front Factory Paint Mixer Barrel"
    CLEAR_FRONT_FACTORY =                       "Front Factory Cleared"
    SIDE_FACTORY_BARREL_1 =                     "Side Factory West Silo Barrel"
    SIDE_FACTORY_BARREL_2 =                     "Side Factory East Silo Barrel"
    SIDE_FACTORY_BARREL_3 =                     "Side Factory Warehouse Barrel"
    SIDE_FACTORY_BARREL_4 =                     "Side Factory Lava Conveyor Barrel"
    CLEAR_SIDE_FACTORY =                        "Side Factory Cleared"
    COIN_MINT_BARREL_1 =                        "Coin Mint Parkour Barrel"
    COIN_MINT_BARREL_2 =                        "Coin Mint Stomper Barrel"
    COIN_MINT_BARREL_3 =                        "Coin Mint Paint Mixer Barrel"
    COIN_MINT_BARREL_4 =                        "Coin Mint Pusher Hall Barrel"
    CLEAR_COIN_MINT =                           "Coin Mint Cleared"
    DOLLAR_MINT_BARREL_1 =                      "Dollar Mint Parkour Barrel"
    DOLLAR_MINT_BARREL_2 =                      "Dollar Mint Stomper Barrel"
    DOLLAR_MINT_BARREL_3 =                      "Dollar Mint Paint Mixer Barrel"
    DOLLAR_MINT_BARREL_4 =                      "Dollar Mint Gear Tower Barrel"
    CLEAR_DOLLAR_MINT =                         "Dollar Mint Cleared"
    BULLION_MINT_BARREL_1 =                     "Bullion Mint Parkour Barrel"
    BULLION_MINT_BARREL_2 =                     "Bullion Mint Stomper Barrel"
    BULLION_MINT_BARREL_3 =                     "Bullion Mint Paint Mixer Barrel"
    BULLION_MINT_BARREL_4 =                     "Bullion Mint Diamond Goon Room Barrel"
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
    FIGHT_VP =                                  "Sellbot VP"
    SELLBOT_PROOF_1 =                           "Sellbot Proof Bundle 1"
    SELLBOT_PROOF_2 =                           "Sellbot Proof Bundle 2"
    SELLBOT_PROOF_3 =                           "Sellbot Proof Bundle 3"
    SELLBOT_PROOF_4 =                           "Sellbot Proof Bundle 4"
    SELLBOT_PROOF_5 =                           "Sellbot Proof Bundle 5"
    FIGHT_CFO =                                 "Cashbot CFO"
    CASHBOT_PROOF_1 =                           "Cashbot Proof Bundle 1"
    CASHBOT_PROOF_2 =                           "Cashbot Proof Bundle 2"
    CASHBOT_PROOF_3 =                           "Cashbot Proof Bundle 3"
    CASHBOT_PROOF_4 =                           "Cashbot Proof Bundle 4"
    CASHBOT_PROOF_5 =                           "Cashbot Proof Bundle 5"
    FIGHT_CJ =                                  "Lawbot CJ"
    LAWBOT_PROOF_1 =                            "Lawbot Proof Bundle 1"
    LAWBOT_PROOF_2 =                            "Lawbot Proof Bundle 2"
    LAWBOT_PROOF_3 =                            "Lawbot Proof Bundle 3"
    LAWBOT_PROOF_4 =                            "Lawbot Proof Bundle 4"
    LAWBOT_PROOF_5 =                            "Lawbot Proof Bundle 5"
    FIGHT_CEO =                                 "Bossbot CEO"
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
    COG_LEVELS      = auto()  # Locations related to cogs generally
    FACILITIES      = auto()  # Locations for clearing facilities
    BUILDINGS       = auto()  # Locations for clearing cog buildings
    BOSS_META       = auto()  # Locations for clearing bosses
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
    SUPPORT_GAG_TRAINING    = auto()  # Locations for training support gags
    TRAP_GAG_TRAINING       = auto()  # Locations for training trap gags
    SOUND_GAG_TRAINING      = auto()  # Locations for training sound gags
    THROW_GAG_TRAINING      = auto()  # Locations for training throw gags
    SQUIRT_GAG_TRAINING     = auto()  # Locations for training squirt gags
    DROP_GAG_TRAINING       = auto()  # Locations for training drop gags
    PET_SHOP        = auto()  # Locations for purchasing checks from pet shop clerks
    TTC_TASKS       = auto()  # Locations for TTC tasks
    DD_TASKS        = auto()  # Locations for DD tasks
    DG_TASKS        = auto()  # Locations for DG tasks
    MML_TASKS       = auto()  # Locations for MML tasks
    TB_TASKS        = auto()  # Locations for TB tasks
    DDL_TASKS       = auto()  # Locations for DDL tasks
    JOKE_1          = auto()  # Locations for knock knock jokes
    JOKE_2          = auto()  # Locations for knock knock jokes
    JOKE_3          = auto()  # Locations for knock knock jokes
    JOKE_4          = auto()  # Locations for knock knock jokes
    JOKE_5          = auto()  # Locations for knock knock jokes
    JOKE_6          = auto()  # Locations for knock knock jokes
    JOKE_7          = auto()  # Locations for knock knock jokes
    JOKE_8          = auto()  # Locations for knock knock jokes
    JOKE_9          = auto()  # Locations for knock knock jokes
    JOKE_10          = auto()  # Locations for knock knock jokes

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

REGION_TO_TREASURE_RULES: dict[ToontownRegionName, list[list]] = {
    ToontownRegionName.TTC:  [[Rule.CanReachTTC], [Rule.CanReachTTC], [Rule.CanReachTTC], [Rule.CanReachTTC], [Rule.CanReachTTC], [Rule.CanReachTTC]],
    ToontownRegionName.DD:   [[Rule.CanReachDD], [Rule.CanReachDD], [Rule.CanReachDD], [Rule.CanReachDD], [Rule.CanReachDD], [Rule.CanReachDD]],
    ToontownRegionName.DG:   [[Rule.CanReachDG], [Rule.CanReachDG], [Rule.CanReachDG], [Rule.CanReachDG], [Rule.CanReachDG], [Rule.CanReachDG]],
    ToontownRegionName.MML:  [[Rule.CanReachMML], [Rule.CanReachMML], [Rule.CanReachMML], [Rule.CanReachMML], [Rule.CanReachMML], [Rule.CanReachMML]],
    ToontownRegionName.TB:   [[Rule.CanReachTB], [Rule.CanReachTB], [Rule.CanReachTB], [Rule.CanReachTB], [Rule.CanReachTB], [Rule.CanReachTB]],
    ToontownRegionName.DDL:  [[Rule.CanReachDDL], [Rule.CanReachDDL], [Rule.CanReachDDL], [Rule.CanReachDDL], [Rule.CanReachDDL], [Rule.CanReachDDL]],
    ToontownRegionName.GS:   [[Rule.CanReachGS], [Rule.CanReachGS], [Rule.CanReachGS], [Rule.CanReachGS], [Rule.CanReachGS], [Rule.CanReachGS]],
    ToontownRegionName.AA:   [[Rule.CanReachAA], [Rule.CanReachAA], [Rule.CanReachAA], [Rule.CanReachAA], [Rule.CanReachAA], [Rule.CanReachAA]],
    ToontownRegionName.SBHQ: [[Rule.CanReachSBHQ], [Rule.CanReachSBHQ], [Rule.CanReachSBHQ], [Rule.CanReachSBHQ], [Rule.CanReachSBHQ], [Rule.CanReachSBHQ]],
    ToontownRegionName.CBHQ: [[Rule.CanReachCBHQ], [Rule.CanReachCBHQ], [Rule.CanReachCBHQ], [Rule.CanReachCBHQ], [Rule.CanReachCBHQ], [Rule.CanReachCBHQ]],
    ToontownRegionName.LBHQ: [[Rule.CanReachLBHQ], [Rule.CanReachLBHQ], [Rule.CanReachLBHQ], [Rule.CanReachLBHQ], [Rule.CanReachLBHQ], [Rule.CanReachLBHQ]],
    ToontownRegionName.BBHQ: [[Rule.CanReachBBHQ], [Rule.CanReachBBHQ], [Rule.CanReachBBHQ], [Rule.CanReachBBHQ], [Rule.CanReachBBHQ], [Rule.CanReachBBHQ]]
}

TREASURE_LOCATION_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(location_name,  location_type, region_name, rule_set)
    for region_name in REGION_TO_TREASURE_LOCATIONS.keys()
    for location_name, location_type, rule_set in zip(
        REGION_TO_TREASURE_LOCATIONS.get(region_name), TREASURE_LOCATION_TYPES, REGION_TO_TREASURE_RULES.get(region_name)
    )
]
# endregion
# region Knock Knock Location Definitions
REGION_TO_KNOCK_KNOCK_LOCATIONS = {
    ToontownRegionName.TTC: [
        [ToontownLocationName.LOOPY_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.LOOPY_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.LOOPY_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.LOOPY_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.LOOPY_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.LOOPY_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.LOOPY_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.LOOPY_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.LOOPY_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.LOOPY_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.PUNCHLINE_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.PUNCHLINE_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.PUNCHLINE_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.PUNCHLINE_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.PUNCHLINE_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.PUNCHLINE_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.PUNCHLINE_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.PUNCHLINE_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.PUNCHLINE_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.PUNCHLINE_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.SILLY_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.SILLY_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.SILLY_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.SILLY_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.SILLY_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.SILLY_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.SILLY_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.SILLY_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.SILLY_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.SILLY_JOKE_10, ToontownLocationType.JOKE_10],
    ],
    ToontownRegionName.DD:   [
        [ToontownLocationName.BARNACLE_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.BARNACLE_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.BARNACLE_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.BARNACLE_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.BARNACLE_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.BARNACLE_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.BARNACLE_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.BARNACLE_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.BARNACLE_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.BARNACLE_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.SEAWEED_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.SEAWEED_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.SEAWEED_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.SEAWEED_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.SEAWEED_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.SEAWEED_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.SEAWEED_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.SEAWEED_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.SEAWEED_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.SEAWEED_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.LIGHTHOUSE_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.LIGHTHOUSE_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.LIGHTHOUSE_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.LIGHTHOUSE_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.LIGHTHOUSE_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.LIGHTHOUSE_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.LIGHTHOUSE_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.LIGHTHOUSE_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.LIGHTHOUSE_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.LIGHTHOUSE_JOKE_10, ToontownLocationType.JOKE_10],
    ],
    ToontownRegionName.DG:   [
        [ToontownLocationName.ELM_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.ELM_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.ELM_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.ELM_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.ELM_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.ELM_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.ELM_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.ELM_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.ELM_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.ELM_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.MAPLE_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.MAPLE_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.MAPLE_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.MAPLE_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.MAPLE_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.MAPLE_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.MAPLE_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.MAPLE_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.MAPLE_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.MAPLE_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.OAK_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.OAK_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.OAK_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.OAK_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.OAK_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.OAK_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.OAK_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.OAK_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.OAK_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.OAK_JOKE_10, ToontownLocationType.JOKE_10],
    ],
    ToontownRegionName.MML:  [
        [ToontownLocationName.ALTO_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.ALTO_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.ALTO_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.ALTO_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.ALTO_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.ALTO_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.ALTO_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.ALTO_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.ALTO_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.ALTO_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.BARITONE_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.BARITONE_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.BARITONE_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.BARITONE_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.BARITONE_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.BARITONE_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.BARITONE_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.BARITONE_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.BARITONE_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.BARITONE_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.TENOR_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.TENOR_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.TENOR_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.TENOR_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.TENOR_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.TENOR_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.TENOR_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.TENOR_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.TENOR_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.TENOR_JOKE_10, ToontownLocationType.JOKE_10],
    ],
    ToontownRegionName.TB:   [
        [ToontownLocationName.SLEET_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.SLEET_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.SLEET_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.SLEET_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.SLEET_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.SLEET_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.SLEET_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.SLEET_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.SLEET_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.SLEET_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.WALRUS_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.WALRUS_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.WALRUS_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.WALRUS_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.WALRUS_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.WALRUS_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.WALRUS_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.WALRUS_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.WALRUS_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.WALRUS_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.POLAR_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.POLAR_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.POLAR_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.POLAR_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.POLAR_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.POLAR_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.POLAR_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.POLAR_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.POLAR_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.POLAR_JOKE_10, ToontownLocationType.JOKE_10],
    ],
    ToontownRegionName.DDL:  [
        [ToontownLocationName.LULLABY_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.LULLABY_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.LULLABY_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.LULLABY_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.LULLABY_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.LULLABY_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.LULLABY_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.LULLABY_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.LULLABY_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.LULLABY_JOKE_10, ToontownLocationType.JOKE_10],
        [ToontownLocationName.PAJAMA_JOKE_1,  ToontownLocationType.JOKE_1],
        [ToontownLocationName.PAJAMA_JOKE_2,  ToontownLocationType.JOKE_2],
        [ToontownLocationName.PAJAMA_JOKE_3,  ToontownLocationType.JOKE_3],
        [ToontownLocationName.PAJAMA_JOKE_4,  ToontownLocationType.JOKE_4],
        [ToontownLocationName.PAJAMA_JOKE_5,  ToontownLocationType.JOKE_5],
        [ToontownLocationName.PAJAMA_JOKE_6,  ToontownLocationType.JOKE_6],
        [ToontownLocationName.PAJAMA_JOKE_7,  ToontownLocationType.JOKE_7],
        [ToontownLocationName.PAJAMA_JOKE_8,  ToontownLocationType.JOKE_8],
        [ToontownLocationName.PAJAMA_JOKE_9,  ToontownLocationType.JOKE_9],
        [ToontownLocationName.PAJAMA_JOKE_10, ToontownLocationType.JOKE_10],
    ],
}

KNOCK_KNOCK_LOCATION_TYPES: list[ToontownLocationType] = [
    ToontownLocationType.JOKE_1,
    ToontownLocationType.JOKE_2,
    ToontownLocationType.JOKE_3,
    ToontownLocationType.JOKE_4,
    ToontownLocationType.JOKE_5,
    ToontownLocationType.JOKE_6,
    ToontownLocationType.JOKE_7,
    ToontownLocationType.JOKE_8,
    ToontownLocationType.JOKE_9,
    ToontownLocationType.JOKE_10,
]

REGION_TO_KNOCK_KNOCK_RULES: dict[ToontownRegionName, list] = {
    ToontownRegionName.TTC:  [Rule.CanReachTTC, Rule.HasTTCBook],
    ToontownRegionName.DD:   [Rule.CanReachDD, Rule.HasDDBook],
    ToontownRegionName.DG:   [Rule.CanReachDG, Rule.HasDGBook],
    ToontownRegionName.MML:  [Rule.CanReachMML, Rule.HasMMLBook],
    ToontownRegionName.TB:   [Rule.CanReachTB, Rule.HasTBBook],
    ToontownRegionName.DDL:  [Rule.CanReachDDL, Rule.HasDDLBook]
}

KNOCK_KNOCK_LOCATION_DEFINITIONS: List[ToontownLocationDefinition] = []
for region_name in REGION_TO_KNOCK_KNOCK_LOCATIONS.keys():
    for location_info in REGION_TO_KNOCK_KNOCK_LOCATIONS[region_name]:
        location = ToontownLocationDefinition(location_info[0],  location_info[1], region_name, REGION_TO_KNOCK_KNOCK_RULES.get(region_name))
        KNOCK_KNOCK_LOCATION_DEFINITIONS.append(location)
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

REGION_TO_BOSS_EVENTS: dict[ToontownRegionName, list[ToontownLocationName]] = {
    ToontownRegionName.SBHQ: ToontownLocationName.FIGHT_VP,
    ToontownRegionName.CBHQ: ToontownLocationName.FIGHT_CFO,
    ToontownRegionName.LBHQ: ToontownLocationName.FIGHT_CJ,
    ToontownRegionName.BBHQ: ToontownLocationName.FIGHT_CEO,
}

BOSS_LOCATION_TYPES: list[ToontownLocationType] = [
    ToontownLocationType.BOSSES_1,
    ToontownLocationType.BOSSES_2,
    ToontownLocationType.BOSSES_3,
    ToontownLocationType.BOSSES_4,
    ToontownLocationType.BOSSES_5,
]

REGION_TO_BOSS_RULES: dict[ToontownRegionName, list[list]] = {
    ToontownRegionName.SBHQ: [Rule.CanFightVP],
    ToontownRegionName.CBHQ: [Rule.CanFightCFO],
    ToontownRegionName.LBHQ: [Rule.CanFightCJ],
    ToontownRegionName.BBHQ: [Rule.CanFightCEO],
}

BOSS_LOCATION_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(location_name,  location_type, region_name, rule_set, [ItemRule.RestrictDisguises])
    for region_name, locations in REGION_TO_BOSS_LOCATIONS.items()
    for location_name, location_type, rule_set in zip(
        locations, BOSS_LOCATION_TYPES, [REGION_TO_BOSS_RULES.get(region_name)] * len(BOSS_LOCATION_TYPES)
    )
]

BOSS_EVENT_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(location_name,  ToontownLocationType.BOSS_META, region_name, REGION_TO_BOSS_RULES.get(region_name), [ItemRule.RestrictDisguises])
    for region_name, location_name in REGION_TO_BOSS_EVENTS.items()
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
    ToontownLocationDefinition(ToontownLocationName.GLAD_HANDER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourSellbot]),
    ToontownLocationDefinition(ToontownLocationName.BEAN_COUNTER_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourCashbot]),
    ToontownLocationDefinition(ToontownLocationName.AMBULANCE_CHASER_DEFEATED,  ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourLawbot]),
    ToontownLocationDefinition(ToontownLocationName.MICROMANAGER_DEFEATED,      ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFourBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MOVER_AND_SHAKER_DEFEATED,  ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveSellbot]),
    ToontownLocationDefinition(ToontownLocationName.NUMBER_CRUNCHER_DEFEATED,   ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveCashbot]),
    ToontownLocationDefinition(ToontownLocationName.BACKSTABBER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveLawbot]),
    ToontownLocationDefinition(ToontownLocationName.DOWNSIZER_DEFEATED,         ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierFiveBossbot]),
    ToontownLocationDefinition(ToontownLocationName.TWO_FACE_DEFEATED,          ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixSellbot]),
    ToontownLocationDefinition(ToontownLocationName.MONEY_BAGS_DEFEATED,        ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixCashbot]),
    ToontownLocationDefinition(ToontownLocationName.SPIN_DOCTOR_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixLawbot]),
    ToontownLocationDefinition(ToontownLocationName.HEAD_HUNTER_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSixBossbot]),
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
    ToontownLocationDefinition(ToontownLocationName.COLD_CALLER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierOneSellbot, Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.SHORT_CHANGE_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierOneCashbot, Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.BOTTOM_FEEDER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierOneLawbot,  Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.FLUNKY_MAXED,               ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierOneBossbot, Rule.TierOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.TELEMARKETER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierTwoSellbot, Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.PENNY_PINCHER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierTwoCashbot, Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.BLOODSUCKER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierTwoLawbot,  Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.PENCIL_PUSHER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierTwoBossbot, Rule.TierTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.NAME_DROPPER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierThreeSellbot, Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.TIGHTWAD_MAXED,             ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierThreeCashbot, Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.DOUBLE_TALKER_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierThreeLawbot,  Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.YESMAN_MAXED,               ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierThreeBossbot, Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.GLAD_HANDER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFourSellbot, Rule.TierFourSellbot]),
    ToontownLocationDefinition(ToontownLocationName.BEAN_COUNTER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFourCashbot, Rule.TierFourCashbot]),
    ToontownLocationDefinition(ToontownLocationName.AMBULANCE_CHASER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFourLawbot,  Rule.TierFourLawbot]),
    ToontownLocationDefinition(ToontownLocationName.MICROMANAGER_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFourBossbot, Rule.TierFourBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MOVER_AND_SHAKER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFiveSellbot, Rule.TierFiveSellbot]),
    ToontownLocationDefinition(ToontownLocationName.NUMBER_CRUNCHER_MAXED,      ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFiveCashbot, Rule.TierFiveCashbot]),
    ToontownLocationDefinition(ToontownLocationName.BACKSTABBER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFiveLawbot,  Rule.TierFiveLawbot]),
    ToontownLocationDefinition(ToontownLocationName.DOWNSIZER_MAXED,            ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierFiveBossbot, Rule.TierFiveBossbot]),
    ToontownLocationDefinition(ToontownLocationName.TWO_FACE_MAXED,             ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierSixSellbot, Rule.TierSixSellbot]),
    ToontownLocationDefinition(ToontownLocationName.MONEY_BAGS_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierSixCashbot, Rule.TierSixCashbot]),
    ToontownLocationDefinition(ToontownLocationName.SPIN_DOCTOR_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierSixLawbot,  Rule.TierSixLawbot]),
    ToontownLocationDefinition(ToontownLocationName.HEAD_HUNTER_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierSixBossbot, Rule.TierSixBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MINGLER_MAXED,              ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightSellbot, Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.LOAN_SHARK_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightCashbot, Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.LEGAL_EAGLE_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightLawbot,  Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.CORPORATE_RAIDER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightBossbot, Rule.TierEightBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MR_HOLLYWOOD_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightSellbot, Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.ROBBER_BARRON_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightCashbot, Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_WIG_MAXED,              ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightLawbot,  Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_CHEESE_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.CanMaxTierEightBossbot, Rule.TierEightBossbot]),
    # endregion
    # region Cog Levels
    ToontownLocationDefinition(ToontownLocationName.LEVEL_ONE_COG_DEFEATED,      ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelOneCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_TWO_COG_DEFEATED,      ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelTwoCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_THREE_COG_DEFEATED,    ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_FOUR_COG_DEFEATED,     ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelFourCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_FIVE_COG_DEFEATED,     ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_SIX_COG_DEFEATED,      ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelSixCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_SEVEN_COG_DEFEATED,    ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_EIGHT_COG_DEFEATED,    ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelEightCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_NINE_COG_DEFEATED,     ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelNineCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_TEN_COG_DEFEATED,      ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelTenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_ELEVEN_COG_DEFEATED,   ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelElevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_TWELVE_COG_DEFEATED,   ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelTwelveCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_THIRTEEN_COG_DEFEATED, ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelThirteenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEVEL_FOURTEEN_COG_DEFEATED, ToontownLocationType.COG_LEVELS, ToontownRegionName.GALLERY, [Rule.LevelFourteenCogs]),
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
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_1,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_2,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_3,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_4,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_5,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_6,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_7,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_8,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_9,    ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_10,   ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_11,   ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_TASK_12,   ToontownLocationType.TTC_TASKS, ToontownRegionName.TTC, [Rule.HasTTCHQAccess, Rule.TierThreeCogs]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_1,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_2,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_3,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.OneStory, Rule.TierFiveCogs]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_4,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_5,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_6,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_7,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_8,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_9,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFiveOffenseGag, Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_10,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_11,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_12,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_1,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_2,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_3,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_4,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_5,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_6,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.TierFiveCogs, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_7,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_8,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_9,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.TierEightSellbot, Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_10,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_11,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_12,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag, Rule.Has20PercentMax, Rule.ThreeStory]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_1,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_2,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_3,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.TierEightSellbot, Rule.TierEightCashbot, Rule.TierEightLawbot, Rule.TierEightBossbot]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_4,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_5,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_6,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_7,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_8,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_9,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_10, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_11, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_12, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag, Rule.Has20PercentMax, Rule.CanAnyFacility]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_1,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_2,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_3,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_4,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_5,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_6,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.TierEightSellbot, Rule.TierEightCashbot, Rule.TierEightLawbot, Rule.TierEightBossbot, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_7,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_8,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_9,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_10,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_11,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_12,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelSevenOffenseGag, Rule.FiveStory, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_1,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax, Rule.FourStory]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_2,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_3,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_4,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_5,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_6,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.TierEightSellbot, Rule.TierEightCashbot, Rule.TierEightLawbot, Rule.TierEightBossbot, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_7,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_8,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax, Rule.CanAnyFacility]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_9,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.CanReachBBHQ, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_10,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_11,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_12,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelSixOffenseGag, Rule.Has40PercentMax]),
    # endregion
    # region Buildings
    ToontownLocationDefinition(ToontownLocationName.ONE_STORY_FIRST_FLOOR,      ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelThreeOffenseGag, Rule.OneStory]),
    ToontownLocationDefinition(ToontownLocationName.TWO_STORY_FIRST_FLOOR,      ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.TWO_STORY_SECOND_FLOOR,     ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.THREE_STORY_FIRST_FLOOR,    ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFiveOffenseGag,  Rule.ThreeStory]),
    ToontownLocationDefinition(ToontownLocationName.THREE_STORY_SECOND_FLOOR,   ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFiveOffenseGag,  Rule.ThreeStory]),
    ToontownLocationDefinition(ToontownLocationName.THREE_STORY_THIRD_FLOOR,    ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFiveOffenseGag,  Rule.ThreeStory]),
    ToontownLocationDefinition(ToontownLocationName.FOUR_STORY_FIRST_FLOOR,     ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSixOffenseGag,   Rule.FourStory]),
    ToontownLocationDefinition(ToontownLocationName.FOUR_STORY_SECOND_FLOOR,    ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSixOffenseGag,   Rule.FourStory]),
    ToontownLocationDefinition(ToontownLocationName.FOUR_STORY_THIRD_FLOOR,     ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSixOffenseGag,   Rule.FourStory]),
    ToontownLocationDefinition(ToontownLocationName.FOUR_STORY_FOURTH_FLOOR,    ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSixOffenseGag,   Rule.FourStory]),
    ToontownLocationDefinition(ToontownLocationName.FIVE_STORY_FIRST_FLOOR,     ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSevenOffenseGag, Rule.FiveStory]),
    ToontownLocationDefinition(ToontownLocationName.FIVE_STORY_SECOND_FLOOR,    ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSevenOffenseGag, Rule.FiveStory]),
    ToontownLocationDefinition(ToontownLocationName.FIVE_STORY_THIRD_FLOOR,     ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSevenOffenseGag, Rule.FiveStory]),
    ToontownLocationDefinition(ToontownLocationName.FIVE_STORY_FOURTH_FLOOR,    ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSevenOffenseGag, Rule.FiveStory]),
    ToontownLocationDefinition(ToontownLocationName.FIVE_STORY_FIFTH_FLOOR,     ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelSevenOffenseGag, Rule.FiveStory]),
    ToontownLocationDefinition(ToontownLocationName.TOONTOWN_CENTRAL_BUILDING,  ToontownLocationType.BUILDINGS, ToontownRegionName.TTC,       [Rule.HasLevelThreeOffenseGag, Rule.OneStory,   Rule.CanReachTTC]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_BUILDING,      ToontownLocationType.BUILDINGS, ToontownRegionName.DD,        [Rule.HasLevelFourOffenseGag,  Rule.TwoStory,   Rule.CanReachDD]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_BUILDING,    ToontownLocationType.BUILDINGS, ToontownRegionName.DG,        [Rule.HasLevelFourOffenseGag,  Rule.TwoStory,   Rule.CanReachDG]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_BUILDING,ToontownLocationType.BUILDINGS, ToontownRegionName.MML,       [Rule.HasLevelFiveOffenseGag,  Rule.ThreeStory, Rule.CanReachMML]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_BUILDING,        ToontownLocationType.BUILDINGS, ToontownRegionName.TB,        [Rule.HasLevelFiveOffenseGag,  Rule.ThreeStory, Rule.CanReachTB]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_BUILDING, ToontownLocationType.BUILDINGS, ToontownRegionName.DDL,       [Rule.HasLevelSixOffenseGag,   Rule.FourStory,  Rule.CanReachDDL]),
    ToontownLocationDefinition(ToontownLocationName.BOSSBOT_BUILDING,           ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.LAWBOT_BUILDING,            ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.CASHBOT_BUILDING,           ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    ToontownLocationDefinition(ToontownLocationName.SELLBOT_BUILDING,           ToontownLocationType.BUILDINGS, ToontownRegionName.BUILDINGS, [Rule.HasLevelFourOffenseGag,  Rule.TwoStory]),
    # endregion
] + TREASURE_LOCATION_DEFINITIONS + KNOCK_KNOCK_LOCATION_DEFINITIONS + [
    # region Facilities
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_1, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_2, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_3, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_FACTORY_BARREL_4, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_FRONT_FACTORY,    ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_1,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_2,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_3,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.SIDE_FACTORY_BARREL_4,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_SIDE_FACTORY,     ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_1,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_2,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_3,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.COIN_MINT_BARREL_4,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_COIN_MINT,        ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_1,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_2,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_3,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.DOLLAR_MINT_BARREL_4,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_DOLLAR_MINT,      ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_1,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_2,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_3,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BULLION_MINT_BARREL_4,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_BULLION_MINT,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.A_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_A_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelFourOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.B_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_B_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.C_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_C_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_1,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_2,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_3,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.D_OFFICE_BARREL_4,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_D_OFFICE,         ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_ONE_BARREL_1,     ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.FRONT_ONE_BARREL_2,     ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_FRONT_ONE,        ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelFiveOffenseGag, Rule.Has40PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_1,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_2,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_3,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.MIDDLE_TWO_BARREL_4,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_MIDDLE_TWO,       ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag,  Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_1,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_2,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_3,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_4,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_5,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.BACK_THREE_BARREL_6,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_BACK_THREE,       ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag, Rule.Has60PercentMax]),
    # endregion
    # region Gag Unlocks
    ToontownLocationDefinition(ToontownLocationName.TOONUP_FEATHER_UNLOCKED,      ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpOne, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_MEGAPHONE_UNLOCKED,    ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpTwo, Rule.HasLevelOneOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_LIPSTICK_UNLOCKED,     ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpThree, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_CANE_UNLOCKED,         ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpFour, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_PIXIE_UNLOCKED,        ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpFive, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_JUGGLING_UNLOCKED,     ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpSix, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TOONUP_HIGHDIVE_UNLOCKED,     ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ToonUpSeven, Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_BANANA_UNLOCKED,         ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapOne]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_RAKE_UNLOCKED,           ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapTwo]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_MARBLES_UNLOCKED,        ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapThree]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_QUICKSAND_UNLOCKED,      ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapFour]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_TRAPDOOR_UNLOCKED,       ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapFive]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_TNT_UNLOCKED,            ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapSix]),
    ToontownLocationDefinition(ToontownLocationName.TRAP_TRAIN_UNLOCKED,          ToontownLocationType.TRAP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.TrapSeven]),
    ToontownLocationDefinition(ToontownLocationName.LURE_ONEBILL_UNLOCKED,        ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureOne]),
    ToontownLocationDefinition(ToontownLocationName.LURE_SMALLMAGNET_UNLOCKED,    ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureTwo]),
    ToontownLocationDefinition(ToontownLocationName.LURE_FIVEBILL_UNLOCKED,       ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureThree]),
    ToontownLocationDefinition(ToontownLocationName.LURE_BIGMAGNET_UNLOCKED,      ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureFour]),
    ToontownLocationDefinition(ToontownLocationName.LURE_TENBILL_UNLOCKED,        ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureFive]),
    ToontownLocationDefinition(ToontownLocationName.LURE_HYPNO_UNLOCKED,          ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureSix]),
    ToontownLocationDefinition(ToontownLocationName.LURE_PRESENTATION_UNLOCKED,   ToontownLocationType.SUPPORT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.LureSeven]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_BIKEHORN_UNLOCKED,      ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundOne]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_WHISTLE_UNLOCKED,       ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundTwo]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_BUGLE_UNLOCKED,         ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundThree]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_AOOGAH_UNLOCKED,        ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundFour]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_TRUNK_UNLOCKED,         ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundFive]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_FOG_UNLOCKED,           ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundSix]),
    ToontownLocationDefinition(ToontownLocationName.SOUND_OPERA_UNLOCKED,         ToontownLocationType.SOUND_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SoundSeven]),
    ToontownLocationDefinition(ToontownLocationName.THROW_CUPCAKE_UNLOCKED,       ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowOne]),
    ToontownLocationDefinition(ToontownLocationName.THROW_FRUITPIESLICE_UNLOCKED, ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowTwo]),
    ToontownLocationDefinition(ToontownLocationName.THROW_CREAMPIESLICE_UNLOCKED, ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowThree]),
    ToontownLocationDefinition(ToontownLocationName.THROW_WHOLEFRUIT_UNLOCKED,    ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowFour]),
    ToontownLocationDefinition(ToontownLocationName.THROW_WHOLECREAM_UNLOCKED,    ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowFive]),
    ToontownLocationDefinition(ToontownLocationName.THROW_CAKE_UNLOCKED,          ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowSix]),
    ToontownLocationDefinition(ToontownLocationName.THROW_WEDDING_UNLOCKED,       ToontownLocationType.THROW_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.ThrowSeven]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_SQUIRTFLOWER_UNLOCKED, ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtOne]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_GLASS_UNLOCKED,        ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtTwo]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_SQUIRTGUN_UNLOCKED,    ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtThree]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_SELTZER_UNLOCKED,      ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtFour]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_HOSE_UNLOCKED,         ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtFive]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_CLOUD_UNLOCKED,        ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtSix]),
    ToontownLocationDefinition(ToontownLocationName.SQUIRT_GEYSER_UNLOCKED,       ToontownLocationType.SQUIRT_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.SquirtSeven]),
    ToontownLocationDefinition(ToontownLocationName.DROP_FLOWERPOT_UNLOCKED,      ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropOne]),
    ToontownLocationDefinition(ToontownLocationName.DROP_SANDBAG_UNLOCKED,        ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropTwo]),
    ToontownLocationDefinition(ToontownLocationName.DROP_ANVIL_UNLOCKED,          ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropThree]),
    ToontownLocationDefinition(ToontownLocationName.DROP_BIGWEIGHT_UNLOCKED,      ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropFour]),
    ToontownLocationDefinition(ToontownLocationName.DROP_SAFE_UNLOCKED,           ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropFive]),
    ToontownLocationDefinition(ToontownLocationName.DROP_PIANO_UNLOCKED,          ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropSix]),
    ToontownLocationDefinition(ToontownLocationName.DROP_BOAT_UNLOCKED,           ToontownLocationType.DROP_GAG_TRAINING, ToontownRegionName.TRAINING, [Rule.DropSeven]),
    # endregion
    ] + BOSS_LOCATION_DEFINITIONS + BOSS_EVENT_DEFINITIONS

LOCATION_NAME_TO_DEFINITION: dict[ToontownLocationName, ToontownLocationDefinition] = {
    locdef.name: locdef for locdef in LOCATION_DEFINITIONS
}

EVENT_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(ToontownLocationName.SAVED_TOONTOWN, ToontownLocationType.MISC, ToontownRegionName.TTC, [Rule.CanWinGame]),
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
TASK_LOCATION_TYPES = [
    ToontownLocationType.TTC_TASKS, ToontownLocationType.DD_TASKS, ToontownLocationType.DG_TASKS,
    ToontownLocationType.MML_TASKS, ToontownLocationType.TB_TASKS, ToontownLocationType.DDL_TASKS
]

SCOUTING_REQUIRED_LOCATIONS = ALL_TASK_LOCATIONS.copy() + SHOP_LOCATIONS.copy()

LOCATION_NAME_TO_ID = {location.name.value: i + consts.BASE_ID for i, location in enumerate(LOCATION_DEFINITIONS)}
LOCATION_ID_TO_NAME = {i + consts.BASE_ID: location.name.value for i, location in enumerate(LOCATION_DEFINITIONS)}

# Remember to update BountiesRequired and TotalBounties options when more bounties get added
BOUNTY_LOCATIONS = [
    ToontownLocationName.SELLBOT_PROOF_1, ToontownLocationName.CASHBOT_PROOF_1, ToontownLocationName.LAWBOT_PROOF_1, ToontownLocationName.BOSSBOT_PROOF_1,  # Boss bounty locations
    ToontownLocationName.URBAN_2_QUALIFY, ToontownLocationName.HARD_GOLF_9, ToontownLocationName.FISHING_COMPLETE_ALBUM, ToontownLocationName.DOG_FISH_1,  # Activity bounty locations
    ToontownLocationName.TOONTOWN_CENTRAL_TASK_12, ToontownLocationName.DONALDS_DOCK_TASK_12, ToontownLocationName.DAISYS_GARDENS_TASK_12,  # Task bounty locations (1)
    ToontownLocationName.MINNIES_MELODYLAND_TASK_12, ToontownLocationName.THE_BRRRGH_TASK_12, ToontownLocationName.DONALDS_DREAMLAND_TASK_12,  # Task bounty locations (2)
    ToontownLocationName.CLEAR_FRONT_FACTORY, ToontownLocationName.CLEAR_SIDE_FACTORY, ToontownLocationName.CLEAR_COIN_MINT, ToontownLocationName.CLEAR_DOLLAR_MINT,  # Facility bounty locations (1)
    ToontownLocationName.CLEAR_BULLION_MINT, ToontownLocationName.CLEAR_A_OFFICE, ToontownLocationName.CLEAR_B_OFFICE, ToontownLocationName.CLEAR_C_OFFICE,  # Facility bounty locations (2)
    ToontownLocationName.CLEAR_D_OFFICE, ToontownLocationName.CLEAR_FRONT_ONE, ToontownLocationName.CLEAR_MIDDLE_TWO, ToontownLocationName.CLEAR_BACK_THREE,  # Facility bounty locations (3)
    ToontownLocationName.TOONUP_HIGHDIVE_UNLOCKED, ToontownLocationName.TRAP_TRAIN_UNLOCKED, ToontownLocationName.LURE_PRESENTATION_UNLOCKED, ToontownLocationName.SOUND_OPERA_UNLOCKED,  # Gag bounty locations (1)
    ToontownLocationName.THROW_WEDDING_UNLOCKED, ToontownLocationName.SQUIRT_GEYSER_UNLOCKED, ToontownLocationName.DROP_BOAT_UNLOCKED,  # Gag bounty locations (2)
    ToontownLocationName.LEVEL_TWELVE_COG_DEFEATED,  # Cog tier bounty locations
    ToontownLocationName.FIVE_STORY_FIFTH_FLOOR,  # Building bounty locations
]

BOSS_BOUNTIES = [ToontownLocationName.SELLBOT_PROOF_1, ToontownLocationName.CASHBOT_PROOF_1, ToontownLocationName.LAWBOT_PROOF_1, ToontownLocationName.BOSSBOT_PROOF_1]
RACE_BOUNTIES = [ToontownLocationName.URBAN_2_QUALIFY]
GOLF_BOUNTIES = [ToontownLocationName.HARD_GOLF_9]
FISH_SPECIES_BOUNTIES = [ToontownLocationName.DOG_FISH_1]
FISH_ALBUM_BOUNTIES = [ToontownLocationName.FISHING_COMPLETE_ALBUM]
ALL_FISH_BOUNTIES = [ToontownLocationName.DOG_FISH_1, ToontownLocationName.FISHING_COMPLETE_ALBUM]
GAG_BOUNTIES = [ToontownLocationName.TOONUP_HIGHDIVE_UNLOCKED, ToontownLocationName.TRAP_TRAIN_UNLOCKED, ToontownLocationName.LURE_PRESENTATION_UNLOCKED, ToontownLocationName.SOUND_OPERA_UNLOCKED,
                ToontownLocationName.THROW_WEDDING_UNLOCKED, ToontownLocationName.SQUIRT_GEYSER_UNLOCKED, ToontownLocationName.DROP_BOAT_UNLOCKED]

def get_location_def_from_name(name: ToontownLocationName) -> ToontownLocationDefinition:
    return LOCATION_NAME_TO_DEFINITION[name]

def get_location_groups():
    return {
    "All Tasks": [name.value for name in ALL_TASK_LOCATIONS],
    "Fishing": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.FISHING],
    "Pet Shops": [name.value for name in SHOP_LOCATIONS],
    "Gag Training": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.TRAINING],
    "Cog Discovery": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.GALLERY],
    "Cog Gallery": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.GALLERY and loc_def.type != ToontownLocationType.COG_LEVELS],
    "Max Gallery": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.GALLERY_MAX],
    "Cog Levels": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.COG_LEVELS],
    "Treasures": [loc_def.name.value for loc_def in TREASURE_LOCATION_DEFINITIONS],
    "Boss Clears": [loc_def.name.value for loc_def in BOSS_LOCATION_DEFINITIONS],
    "Toontown Central": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.TTC],
    "Donald's Dock": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.DD],
    "Daisy Gardens": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.DG],
    "Minnie's Melodyland": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.MML],
    "The Brrrgh": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.TB],
    "Donald's Dreamland": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.DDL],
    "Goofy Speedway": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.GS],
    "Acorn Acres": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.AA],
    "Sellbot HQ": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.SBHQ and loc_def.type != ToontownLocationType.BOSS_META],
    "SBHQ Facilities": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.FACILITIES and loc_def.region == ToontownRegionName.SBHQ],
    "Cashbot HQ": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.CBHQ and loc_def.type != ToontownLocationType.BOSS_META],
    "CBHQ Facilities": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.FACILITIES and loc_def.region == ToontownRegionName.CBHQ],
    "Lawbot HQ": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.LBHQ and loc_def.type != ToontownLocationType.BOSS_META],
    "LBHQ Facilities": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.FACILITIES and loc_def.region == ToontownRegionName.LBHQ],
    "Bossbot HQ": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.region == ToontownRegionName.BBHQ and loc_def.type != ToontownLocationType.BOSS_META],
    "BBHQ Facilities": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.FACILITIES and loc_def.region == ToontownRegionName.BBHQ],
    "Buildings": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.BUILDINGS],
    "Golfing": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.GOLF],
    "Racing": [loc_def.name.value for loc_def in LOCATION_DEFINITIONS if loc_def.type == ToontownLocationType.RACING],
    "Bounty": [location.value for location in BOUNTY_LOCATIONS]
    }
