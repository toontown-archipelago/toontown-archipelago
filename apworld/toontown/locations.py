from dataclasses import dataclass, field
from enum import IntEnum, Enum, auto
from typing import List, Dict

from BaseClasses import LocationProgressType
from . import consts
from .regions import ToontownRegionName
from .rules import Rule


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
    TOONUP_FEATHER_UNLOCKED =                   "Feather Unlocked (Toon-up Training)"
    TOONUP_MEGAPHONE_UNLOCKED =                 "Megaphone Unlocked (Toon-up Training)"
    TOONUP_LIPSTICK_UNLOCKED =                  "Lipstick Unlocked (Toon-up Training)"
    TOONUP_CANE_UNLOCKED =                      "Bamboo Cane Unlocked (Toon-up Training)"
    TOONUP_PIXIE_UNLOCKED =                     "Pixie Dust Unlocked (Toon-up Training)"
    TOONUP_JUGGLING_UNLOCKED =                  "Juggling Cubes Unlocked (Toon-up Training)"
    TOONUP_HIGHDIVE_UNLOCKED =                  "High Dive Unlocked (MAXED Toon-up)"
    TRAP_BANANA_UNLOCKED =                      "Banana Peel Unlocked (Trap Training)"
    TRAP_RAKE_UNLOCKED =                        "Rake Unlocked (Trap Training)"
    TRAP_MARBLES_UNLOCKED =                     "Marbles Unlocked (Trap Training)"
    TRAP_QUICKSAND_UNLOCKED =                   "Quicksand Unlocked (Trap Training)"
    TRAP_TRAPDOOR_UNLOCKED =                    "Trapdoor Unlocked (Trap Training)"
    TRAP_TNT_UNLOCKED =                         "TNT Unlocked (Trap Training)"
    TRAP_TRAIN_UNLOCKED =                       "Railroad Unlocked (MAXED Trap)"
    LURE_ONEBILL_UNLOCKED =                     "$1 Bill Unlocked (Lure Training)"
    LURE_SMALLMAGNET_UNLOCKED =                 "Small Magnet Unlocked (Lure Training)"
    LURE_FIVEBILL_UNLOCKED =                    "$5 Bill Unlocked (Lure Training)"
    LURE_BIGMAGNET_UNLOCKED =                   "Big Magnet Unlocked (Lure Training)"
    LURE_TENBILL_UNLOCKED =                     "$10 Bill Unlocked (Lure Training)"
    LURE_HYPNO_UNLOCKED =                       "Hypno-Goggles Unlocked (Lure Training)"
    LURE_PRESENTATION_UNLOCKED =                "Presentation Unlocked (MAXED Lure)"
    SOUND_BIKEHORN_UNLOCKED =                   "Bike Horn Unlocked (Sound Training)"
    SOUND_WHISTLE_UNLOCKED =                    "Whistle Unlocked (Sound Training)"
    SOUND_BUGLE_UNLOCKED =                      "Bugle Unlocked (Sound Training)"
    SOUND_AOOGAH_UNLOCKED =                     "Aoogah Unlocked (Sound Training)"
    SOUND_TRUNK_UNLOCKED =                      "Elephant Trunk Unlocked (Sound Training)"
    SOUND_FOG_UNLOCKED =                        "Foghorn Unlocked (Sound Training)"
    SOUND_OPERA_UNLOCKED =                      "Opera Singer Unlocked (MAXED Sound)"
    THROW_CUPCAKE_UNLOCKED =                    "Cupcake Unlocked (Throw Training)"
    THROW_FRUITPIESLICE_UNLOCKED =              "Fruit Pie Slice Unlocked (Throw Training)"
    THROW_CREAMPIESLICE_UNLOCKED =              "Cream Pie Slice Unlocked (Throw Training)"
    THROW_WHOLEFRUIT_UNLOCKED =                 "Whole Fruit Pie Unlocked (Throw Training)"
    THROW_WHOLECREAM_UNLOCKED =                 "Whole Cream Pie Unlocked (Throw Training)"
    THROW_CAKE_UNLOCKED =                       "Birthday Cake Unlocked (Throw Training)"
    THROW_WEDDING_UNLOCKED =                    "Wedding Cake Unlocked (MAXED Throw)"
    SQUIRT_SQUIRTFLOWER_UNLOCKED =              "Squirting Flower Unlocked (Squirt Training)"
    SQUIRT_GLASS_UNLOCKED =                     "Glass of Water Unlocked (Squirt Training)"
    SQUIRT_SQUIRTGUN_UNLOCKED =                 "Squirt Gun Unlocked (Squirt Training)"
    SQUIRT_SELTZER_UNLOCKED =                   "Seltzer Bottle Unlocked (Squirt Training)"
    SQUIRT_HOSE_UNLOCKED =                      "Firehose Unlocked (Squirt Training)"
    SQUIRT_CLOUD_UNLOCKED =                     "Stormcloud Unlocked (Squirt Training)"
    SQUIRT_GEYSER_UNLOCKED =                    "Geyser Unlocked (MAXED Squirt)"
    DROP_FLOWERPOT_UNLOCKED =                   "Flowerpot Unlocked (Drop Training)"
    DROP_SANDBAG_UNLOCKED =                     "Sandbag Unlocked (Drop Training)"
    DROP_ANVIL_UNLOCKED =                       "Anvil Unlocked (Drop Training)"
    DROP_BIGWEIGHT_UNLOCKED =                   "Big Weight Unlocked (Drop Training)"
    DROP_SAFE_UNLOCKED =                        "Safe Unlocked (Drop Training)"
    DROP_PIANO_UNLOCKED =                       "Piano Unlocked (Drop Training)"
    DROP_BOAT_UNLOCKED =                        "Toontanic Unlocked (MAXED Drop)"
    FISHING_10_SPECIES =                        "(Fishing) 10 Species Caught Trophy"
    FISHING_20_SPECIES =                        "(Fishing) 20 Species Caught Trophy"
    FISHING_30_SPECIES =                        "(Fishing) 30 Species Caught Trophy"
    FISHING_40_SPECIES =                        "(Fishing) 40 Species Caught Trophy"
    FISHING_50_SPECIES =                        "(Fishing) 50 Species Caught Trophy"
    FISHING_60_SPECIES =                        "(Fishing) 60 Species Caught Trophy"
    FISHING_COMPLETE_ALBUM =                    "(Fishing) All 70 Species Caught Trophy"
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
    DISCOVER_TTC =                              "Discover Toontown Central"
    DISCOVER_DD =                               "Discover Donald's Dock"
    DISCOVER_DG =                               "Discover Daisy Gardens"
    DISCOVER_MML =                              "Discover Minnie's Melodyland"
    DISCOVER_TB =                               "Discover The Brrrgh"
    DISCOVER_DDL =                              "Discover Donald's Dreamland"
    DISCOVER_GS =                               "Discover Goofy Speedway"
    DISCOVER_AA =                               "Discover Acorn Acres"
    DISCOVER_SBHQ =                             "Discover Sellbot HQ"
    DISCOVER_CBHQ =                             "Discover Cashbot HQ"
    DISCOVER_LBHQ =                             "Discover Lawbot HQ"
    DISCOVER_BBHQ =                             "Discover Bossbot HQ"
    CLEAR_FRONT_FACTORY =                       "Front Factory Cleared"
    CLEAR_SIDE_FACTORY =                        "Side Factory Cleared"
    CLEAR_COIN_MINT =                           "Coin Mint Cleared"
    CLEAR_DOLLAR_MINT =                         "Dollar Mint Cleared"
    CLEAR_BULLION_MINT =                        "Bullion Mint Cleared"
    CLEAR_A_OFFICE =                            "A Office Cleared"
    CLEAR_B_OFFICE =                            "B Office Cleared"
    CLEAR_C_OFFICE =                            "C Office Cleared"
    CLEAR_D_OFFICE =                            "D Office Cleared"
    CLEAR_FRONT_ONE =                         "Front One Cleared"
    CLEAR_MIDDLE_TWO =                        "Middle Two Cleared"
    CLEAR_BACK_THREE =                          "Back Three Cleared"
    SELLBOT_PROOF =                             "Sellbot Proof"
    CASHBOT_PROOF =                             "Cashbot Proof"
    LAWBOT_PROOF =                              "Lawbot Proof"
    BOSSBOT_PROOF =                             "Bossbot Proof"
    SAVED_TOONTOWN =                            "Save Toontown"


class ToontownLocationType(IntEnum):
    STARTER      = auto()  # Location that is considered a "starting" check on login, typically we force checks here
    GALLERY      = auto()  # Locations for discovering cogs in the gallery
    GALLERY_MAX  = auto()  # Locations for maxing cogs in the gallery
    FACILITIES   = auto()  # Locations for clearing facilities
    BOSSES       = auto()  # Locations for clearing bosses
    FISHING      = auto()  # Locations for fishing trophies
    PLAYGROUND   = auto()  # Locations for discovering playgrounds
    GAG_TRAINING = auto()  # Locations for training gags

    TTC_TASKS    = auto()  # Locations for TTC tasks
    DD_TASKS     = auto()  # Locations for DD tasks
    DG_TASKS     = auto()  # Locations for DG tasks
    MML_TASKS    = auto()  # Locations for MML tasks
    TB_TASKS     = auto()  # Locations for TB tasks
    DDL_TASKS    = auto()  # Locations for DDL tasks

    MISC = auto()


@dataclass
class ToontownLocationDefinition:
    name: ToontownLocationName
    type: ToontownLocationType
    region: ToontownRegionName
    rules: List[Rule] = field(default_factory=list)
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    rule_logic_or: bool = False  # By default, rule logic ANDs values in the list
    unique_id: int = 0  # Set in post


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
    ToontownLocationDefinition(ToontownLocationName.MINGLER_DEFEATED,           ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LOAN_SHARK_DEFEATED,        ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEGAL_EAGLE_DEFEATED,       ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.CORPORATE_RAIDER_DEFEATED,  ToontownLocationType.GALLERY,     ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
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
    ToontownLocationDefinition(ToontownLocationName.MINGLER_MAXED,              ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LOAN_SHARK_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.LEGAL_EAGLE_MAXED,          ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.CORPORATE_RAIDER_MAXED,     ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierSevenCogs]),
    ToontownLocationDefinition(ToontownLocationName.MR_HOLLYWOOD_MAXED,         ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightSellbot]),
    ToontownLocationDefinition(ToontownLocationName.ROBBER_BARRON_MAXED,        ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightCashbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_WIG_MAXED,              ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightLawbot]),
    ToontownLocationDefinition(ToontownLocationName.BIG_CHEESE_MAXED,           ToontownLocationType.GALLERY_MAX, ToontownRegionName.GALLERY, [Rule.TierEightBossbot]),
    # endregion
    # region Fishing
    ToontownLocationDefinition(ToontownLocationName.FISHING_10_SPECIES,     ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.TwigRod,   Rule.OnePlaygroundAccessible]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_20_SPECIES,     ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.BambooRod, Rule.TwoPlaygroundsAccessible]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_30_SPECIES,     ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.WoodRod,   Rule.ThreePlaygroundsAccessible]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_40_SPECIES,     ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.SteelRod,  Rule.FourPlaygroundsAccessible]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_50_SPECIES,     ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.GoldRod,   Rule.FivePlaygroundsAccessible]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_60_SPECIES,     ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.GoldRod,   Rule.SixPlaygroundsAccessible]),
    ToontownLocationDefinition(ToontownLocationName.FISHING_COMPLETE_ALBUM, ToontownLocationType.FISHING, ToontownRegionName.FISHING, [Rule.GoldRod,   Rule.SixPlaygroundsAccessible]),
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
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_3,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_4,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_5,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_6,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_7,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_8,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_9,        ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_10,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_11,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelTwoOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DOCK_TASK_12,       ToontownLocationType.DD_TASKS, ToontownRegionName.DD, [Rule.HasDDHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_1,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_2,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_3,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_4,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_5,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_6,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_7,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_8,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_9,      ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_10,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_11,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DAISYS_GARDENS_TASK_12,     ToontownLocationType.DG_TASKS, ToontownRegionName.DG, [Rule.HasDGHQAccess, Rule.HasLevelThreeOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_1,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_2,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_3,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_4,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_5,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_6,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_7,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_8,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_9,  ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_10, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_11, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.MINNIES_MELODYLAND_TASK_12, ToontownLocationType.MML_TASKS, ToontownRegionName.MML, [Rule.HasMMLHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_1,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_2,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_3,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_4,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_5,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_6,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_7,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_8,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_9,          ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_10,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_11,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.THE_BRRRGH_TASK_12,         ToontownLocationType.TB_TASKS, ToontownRegionName.TB, [Rule.HasTBHQAccess, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_1,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_2,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_3,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_4,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_5,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_6,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_7,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_8,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_9,   ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_10,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_11,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.DONALDS_DREAMLAND_TASK_12,  ToontownLocationType.DDL_TASKS, ToontownRegionName.DDL, [Rule.HasDDLHQAccess, Rule.HasLevelFiveOffenseGag]),
    # endregion
    # region Area Discovery
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_TTC,  ToontownLocationType.PLAYGROUND, ToontownRegionName.TTC),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_DD,   ToontownLocationType.PLAYGROUND, ToontownRegionName.DD),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_DG,   ToontownLocationType.PLAYGROUND, ToontownRegionName.DG),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_MML,  ToontownLocationType.PLAYGROUND, ToontownRegionName.MML),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_TB,   ToontownLocationType.PLAYGROUND, ToontownRegionName.TB),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_DDL,  ToontownLocationType.PLAYGROUND, ToontownRegionName.DDL),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_GS,   ToontownLocationType.PLAYGROUND, ToontownRegionName.GS),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_AA,   ToontownLocationType.PLAYGROUND, ToontownRegionName.AA),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_SBHQ, ToontownLocationType.PLAYGROUND, ToontownRegionName.SBHQ),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_CBHQ, ToontownLocationType.PLAYGROUND, ToontownRegionName.CBHQ),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_LBHQ, ToontownLocationType.PLAYGROUND, ToontownRegionName.LBHQ),
    ToontownLocationDefinition(ToontownLocationName.DISCOVER_BBHQ, ToontownLocationType.PLAYGROUND, ToontownRegionName.BBHQ),
    # endregion
    # region Facilities
    ToontownLocationDefinition(ToontownLocationName.CLEAR_FRONT_FACTORY, ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.FrontFactoryKey, Rule.HasLevelFourOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_SIDE_FACTORY,  ToontownLocationType.FACILITIES, ToontownRegionName.SBHQ, [Rule.SideFactoryKey,  Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_COIN_MINT,     ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.CoinMintKey,     Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_DOLLAR_MINT,   ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.DollarMintKey,   Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_BULLION_MINT,  ToontownLocationType.FACILITIES, ToontownRegionName.CBHQ, [Rule.BullionMintKey,  Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_A_OFFICE,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeAKey,      Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_B_OFFICE,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeBKey,      Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_C_OFFICE,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeCKey,      Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_D_OFFICE,      ToontownLocationType.FACILITIES, ToontownRegionName.LBHQ, [Rule.OfficeDKey,      Rule.HasLevelSevenOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_FRONT_ONE,     ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.FrontOneKey,     Rule.HasLevelFiveOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_MIDDLE_TWO,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.MiddleTwoKey,    Rule.HasLevelSixOffenseGag]),
    ToontownLocationDefinition(ToontownLocationName.CLEAR_BACK_THREE,    ToontownLocationType.FACILITIES, ToontownRegionName.BBHQ, [Rule.BackThreeKey,    Rule.HasLevelSevenOffenseGag]),
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
    # region Bosses
    ToontownLocationDefinition(ToontownLocationName.SELLBOT_PROOF, ToontownLocationType.BOSSES, ToontownRegionName.SBHQ, [Rule.CanFightVP]),
    ToontownLocationDefinition(ToontownLocationName.CASHBOT_PROOF, ToontownLocationType.BOSSES, ToontownRegionName.CBHQ, [Rule.CanFightCFO]),
    ToontownLocationDefinition(ToontownLocationName.LAWBOT_PROOF,  ToontownLocationType.BOSSES, ToontownRegionName.LBHQ, [Rule.CanFightCJ]),
    ToontownLocationDefinition(ToontownLocationName.BOSSBOT_PROOF, ToontownLocationType.BOSSES, ToontownRegionName.BBHQ, [Rule.CanFightCEO]),
    # endregion
]


EVENT_DEFINITIONS: List[ToontownLocationDefinition] = [
    ToontownLocationDefinition(ToontownLocationName.SAVED_TOONTOWN, ToontownLocationType.MISC,   ToontownRegionName.TTC, [Rule.AllBossesDefeated]),
]


for i in range(len(LOCATION_DEFINITIONS)):
    LOCATION_DEFINITIONS[i].unique_id = i + consts.BASE_ID

LOCATION_DESCRIPTIONS: Dict[str, str] = {

}


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

SCOUTING_REQUIRED_LOCATIONS = ALL_TASK_LOCATIONS.copy()
