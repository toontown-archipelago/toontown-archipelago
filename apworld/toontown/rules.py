from enum import Enum, auto


class Rule(Enum):
    ### Street Access ###

    SillyStreet    = auto()  # TTC => DG
    LoopyLane      = auto()  # TTC => MML
    PunchlinePlace = auto()  # TTC => DD
    BarnacleBoulevard = auto()  # DD => TTC
    SeaweedStreet     = auto()  # DD => DG
    LighthouseLane    = auto()  # DD => TB
    AATunnel = auto()  # DD => AA
    ElmStreet   = auto()  # DG => TTC
    MapleStreet = auto()  # DG => DD
    OakStreet   = auto()  # DG => SBHQ
    AltoAvenue        = auto()  # MML => TTC
    BaritoneBoulevard = auto()  # MML => TB
    TenorTerrace      = auto()  # MML => DDL
    WalrusWay   = auto()  # TB => DD
    SleetStreet = auto()  # TB => MML
    PolarPlace  = auto()  # TB => LBHQ
    LullabyLane = auto()  # DDL => MML
    PajamaPlace = auto()  # DDL => CBHQ

    TunnelCanBeUsed = auto()
    HasTeleportAccess = auto()

    ### Playground Accessibility ###

    # NOTE - avoid using these rules for region defs
    CanReachTTC  = auto()
    CanReachDD   = auto()
    CanReachDG   = auto()
    CanReachMML  = auto()
    CanReachTB   = auto()
    CanReachDDL  = auto()
    CanReachAA   = auto()
    CanReachGS   = auto()
    CanReachSBHQ = auto()
    CanReachCBHQ = auto()
    CanReachLBHQ = auto()
    CanReachBBHQ = auto()

    OnePlaygroundAccessible    = auto()
    TwoPlaygroundsAccessible   = auto()
    ThreePlaygroundsAccessible = auto()
    FourPlaygroundsAccessible  = auto()
    FivePlaygroundsAccessible  = auto()
    SixPlaygroundsAccessible   = auto()

    HasTTCHQAccess = auto()
    HasDDHQAccess  = auto()
    HasDGHQAccess  = auto()
    HasMMLHQAccess = auto()
    HasTBHQAccess  = auto()
    HasDDLHQAccess = auto()

    ### Joke Access ###

    HasTTCBook = auto()
    HasDDBook  = auto()
    HasDGBook  = auto()
    HasMMLBook = auto()
    HasTBBook  = auto()
    HasDDLBook = auto()

    ### Building Access ###

    OneStory      = auto()
    TwoStory      = auto()
    ThreeStory    = auto()
    FourStory     = auto()
    FiveStory     = auto()

    ### Cog Tier Access ###

    TierOneCogs   = auto()
    TierTwoCogs   = auto()
    TierThreeCogs = auto()

    TierFourSellbot  = auto()
    TierFourCashbot = auto()
    TierFourLawbot = auto()
    TierFourBossbot = auto()
    TierFourCogs = auto()

    TierFiveSellbot = auto()
    TierFiveCashbot = auto()
    TierFiveLawbot = auto()
    TierFiveBossbot = auto()
    TierFiveCogs = auto()

    TierSixSellbot = auto()
    TierSixCashbot = auto()
    TierSixLawbot = auto()
    TierSixBossbot = auto()
    TierSixCogs = auto()

    TierSevenCogs = auto()

    TierEightSellbot = auto()
    TierEightCashbot = auto()
    TierEightLawbot  = auto()
    TierEightBossbot = auto()
    TierEightCogs = auto()

    LevelOneCogs = auto()
    LevelTwoCogs = auto()
    LevelThreeCogs = auto()
    LevelFourCogs = auto()
    LevelFiveCogs = auto()
    LevelSixCogs = auto()
    LevelSevenCogs = auto()
    LevelEightCogs = auto()
    LevelNineCogs = auto()
    LevelTenCogs = auto()
    LevelElevenCogs = auto()
    LevelTwelveCogs = auto()
    LevelThirteenCogs = auto()
    LevelFourteenCogs = auto()

    CanMaxTierOneSellbot = auto()
    CanMaxTierOneCashbot = auto()
    CanMaxTierOneLawbot = auto()
    CanMaxTierOneBossbot = auto()

    CanMaxTierTwoSellbot = auto()
    CanMaxTierTwoCashbot = auto()
    CanMaxTierTwoLawbot = auto()
    CanMaxTierTwoBossbot = auto()

    CanMaxTierThreeSellbot = auto()
    CanMaxTierThreeCashbot = auto()
    CanMaxTierThreeLawbot = auto()
    CanMaxTierThreeBossbot = auto()

    CanMaxTierFourSellbot = auto()
    CanMaxTierFourCashbot = auto()
    CanMaxTierFourLawbot = auto()
    CanMaxTierFourBossbot = auto()

    CanMaxTierFiveSellbot = auto()
    CanMaxTierFiveCashbot = auto()
    CanMaxTierFiveLawbot = auto()
    CanMaxTierFiveBossbot = auto()

    CanMaxTierSixSellbot = auto()
    CanMaxTierSixCashbot = auto()
    CanMaxTierSixLawbot = auto()
    CanMaxTierSixBossbot = auto()

    CanMaxTierEightSellbot = auto()
    CanMaxTierEightCashbot = auto()
    CanMaxTierEightLawbot = auto()
    CanMaxTierEightBossbot = auto()

    ### Facility Keys ###

    FrontFactoryKey = auto()
    SideFactoryKey  = auto()

    CoinMintKey    = auto()
    DollarMintKey  = auto()
    BullionMintKey = auto()

    OfficeAKey = auto()
    OfficeBKey = auto()
    OfficeCKey = auto()
    OfficeDKey = auto()

    FrontOneKey  = auto()
    MiddleTwoKey = auto()
    BackThreeKey = auto()

    CanAnyFacility = auto()

    ### Laff Logic ###

    Has20PercentMax = auto()
    Has40PercentMax = auto()
    Has60PercentMax = auto()
    Has80PercentMax = auto()

    ### Activities ###

    Racing  = auto()
    Golfing = auto()

    ### Cog Disguises ###

    SellbotDisguise = auto()
    CashbotDisguise = auto()
    LawbotDisguise  = auto()
    BossbotDisguise = auto()

    ### Doodles ###

    CanBuyTTCDoodle = auto()
    CanBuyDDDoodle = auto()
    CanBuyDGDoodle = auto()
    CanBuyMMLDoodle = auto()
    CanBuyTBDoodle = auto()
    CanBuyDDLDoodle = auto()

    ### Gag Rules ###

    ToonUpOne   = auto()
    ToonUpTwo   = auto()
    ToonUpThree = auto()
    ToonUpFour  = auto()
    ToonUpFive  = auto()
    ToonUpSix   = auto()
    ToonUpSeven = auto()

    TrapOne   = auto()
    TrapTwo   = auto()
    TrapThree = auto()
    TrapFour  = auto()
    TrapFive  = auto()
    TrapSix   = auto()
    TrapSeven = auto()

    LureOne   = auto()
    LureTwo   = auto()
    LureThree = auto()
    LureFour  = auto()
    LureFive  = auto()
    LureSix   = auto()
    LureSeven = auto()

    SoundOne   = auto()
    SoundTwo   = auto()
    SoundThree = auto()
    SoundFour  = auto()
    SoundFive  = auto()
    SoundSix   = auto()
    SoundSeven = auto()

    ThrowOne   = auto()
    ThrowTwo   = auto()
    ThrowThree = auto()
    ThrowFour  = auto()
    ThrowFive  = auto()
    ThrowSix   = auto()
    ThrowSeven = auto()

    SquirtOne   = auto()
    SquirtTwo   = auto()
    SquirtThree = auto()
    SquirtFour  = auto()
    SquirtFive  = auto()
    SquirtSix   = auto()
    SquirtSeven = auto()

    DropOne   = auto()
    DropTwo   = auto()
    DropThree = auto()
    DropFour  = auto()
    DropFive  = auto()
    DropSix   = auto()
    DropSeven = auto()

    HasLevelOneOffenseGag = auto()
    HasLevelTwoOffenseGag = auto()
    HasLevelThreeOffenseGag = auto()
    HasLevelFourOffenseGag = auto()
    HasLevelFiveOffenseGag = auto()
    HasLevelSixOffenseGag = auto()
    HasLevelSevenOffenseGag = auto()
    HasLevelEightOffenseGag = auto()

    ### Fishing ###

    FishCatch   = auto()
    FishGenus  = auto()
    FishGallery = auto()

    ### General ###

    CanFightVP  = auto()
    CanFightCFO = auto()
    CanFightCJ  = auto()
    CanFightCEO = auto()

    ### WIN CONDITION ###

    AllBossesDefeated = auto()
    AllFishCaught = auto()
    TaskedAllHoods = auto()
    GainedEnoughLaff = auto()
    MaxedAllGags = auto()
    CanReachBounties = auto()

    CanWinGame = auto()


class ItemRule(Enum):
    RestrictDisguises = auto()
