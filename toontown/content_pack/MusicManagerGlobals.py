from toontown.toonbase.ToontownGlobals import *
GLOBALS = {
    SellbotHQ: {
        'music': 'sellbot-courtyard',
        'battleMusic': 'sellbot-courtyard-battle',
    },
    SellbotLobby: {
        'music': 'sellbot-lobby',
        'battleMusic': 'sellbot-lobby',
    },
    SellbotFactoryExt: {
        'music': 'sellbot-factory-exterior',
        'battleMusic': 'sellbot-factory-exterior-battle',
    },
    SellbotFactoryInt: {
        'music': 'sellbot-f-factory-interior',
        'battleMusic': 'sellbot-f-factory-interior-battle',
    },
    SellbotFactoryIntS: {
        'music': 'sellbot-s-factory-interior',
        'battleMusic': 'sellbot-s-factory-interior-battle',
    },
    CashbotHQ: {
        'music': 'cashbot-courtyard',
        'battleMusic': 'cashbot-courtyard-battle',
    },
    CashbotMintIntA: {
        'music': 'cashbot-coin-mint',
        'battleMusic': 'cashbot-coin-mint-battle',
    },
    CashbotMintIntB: {
        'music': 'cashbot-dollar-mint',
        'battleMusic': 'cashbot-dollar-mint-battle',
    },
    CashbotLobby: {
        'music': 'cashbot-lobby',
        'battleMusic': 'cashbot-lobby',
    },
    CashbotMintIntC: {
        'music': 'cashbot-bullion-mint',
        'battleMusic': 'cashbot-bullion-mint-battle',
    },
    LawbotHQ: {
        'music': 'lawbot-courtyard',
        'battleMusic': 'lawbot-courtyard-battle',
    },
    LawbotLobby: {
        'music': 'lawbot-lobby',
        'battleMusic': 'lawbot-lobby',
    },
    LawbotOfficeExt: {
        'music': 'lawbot-district-attorney-office-lobby',
        'battleMusic': 'lawbot-district-attorney-office-lobby-battle',
    },
    LawbotStageIntA: {
        'music': 'lawbot-office-a',
        'battleMusic': 'lawbot-office-a-battle',
    },
    LawbotStageIntB: {
        'music': 'lawbot-office-b',
        'battleMusic': 'lawbot-office-b-battle',
    },
    LawbotStageIntC: {
        'music': 'lawbot-office-c',
        'battleMusic': 'lawbot-office-c-battle',
    },
    LawbotStageIntD: {
        'music': 'lawbot-office-d',
        'battleMusic': 'lawbot-office-d-battle',
    },
    BossbotHQ: {
        'music': 'bossbot-courtyard',
        'battleMusic': 'bossbot-courtyard-battle',
    },
    BossbotLobby: {
        'music': 'bossbot-lobby',
        'battleMusic': 'bossbot-lobby',
    },
    BossbotCountryClubIntA: {
        'music': 'front-one',
        'battleMusic': 'front-one-battle',
    },
    BossbotCountryClubIntB: {
        'music': 'middle-two',
        'battleMusic': 'middle-two-battle',
    },
    BossbotCountryClubIntC: {
        'music': 'back-three',
        'battleMusic': 'back-three-battle',
    },
}

safeZones = [ToontownCentral,
             DonaldsDock,
             DaisyGardens,
             MinniesMelodyland,
             TheBrrrgh,
             DonaldsDreamland,
             GoofySpeedway,
             GolfZone,
             OutdoorZone]

safeZonetoAlis = {
    ToontownCentral: 'tt',
    DonaldsDock: 'dd',
    DaisyGardens: 'dg',
    MinniesMelodyland: 'mm',
    TheBrrrgh: 'br',
    DonaldsDreamland: 'dl',
    GoofySpeedway: 'gs',
    OutdoorZone: 'oz',
    GolfZone: 'gz',
}

for safeZone in safeZones:
    GLOBALS[safeZone] = {
        'music': safeZonetoAlis[safeZone] + '-sz',
        'battleMusic': safeZonetoAlis[safeZone] + '-sz-battle',
        'activityMusic': safeZonetoAlis[safeZone] + '-sz-activity'
    }
    if safeZone not in [GolfZone,
                        OutdoorZone]:
        safeHierarchy = HoodHierarchyMusicManager[safeZone]
        for hood in safeHierarchy:
            GLOBALS[safeZonetoAlis[safeZone] + '-' + str(hood)] = {
                'music': safeZonetoAlis[safeZone] + '-' + str(hood),
                'battleMusic': safeZonetoAlis[safeZone] + '-' + str(hood) + '-battle',
                'activityMusic': safeZonetoAlis[safeZone] + '-' + str(hood) + '-activity'
            }