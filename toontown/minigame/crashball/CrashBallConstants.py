from toontown.toonbase import ToontownGlobals

CrashBallNPCChoices = {
    ToontownGlobals.ToontownCentral: ["f", "bf", "sc", "cc"],
    ToontownGlobals.DonaldsDock: ["f", "bf", "sc", "cc", "ym", "dt", "pp", "nd"],
    ToontownGlobals.DaisyGardens: ["f", "bf", "sc", "cc", "ym", "dt", "pp", "nd", "mm", "ac", "tw", "gh"],
    ToontownGlobals.MinniesMelodyland: ["f", "bf", "sc", "cc", "mm", "ac", "tw", "gh", "hh", "bs", "nc", "tf"],
    ToontownGlobals.TheBrrrgh: ["f", "bf", "sc", "cc", "hh", "bs", "nc", "tf", "cr", "le", "mb", "m"],
    ToontownGlobals.DonaldsDreamland: ["f", "bf", "sc", "hh", "bs", "nc", "tf", "cc", "cr", "le", "mb", "m"],
}

CrashBallSkyFiles = {
    ToontownGlobals.ToontownCentral: "phase_3.5/models/props/TT_sky",
    ToontownGlobals.DonaldsDock: "phase_3.5/models/props/BR_sky",
    ToontownGlobals.DaisyGardens: "phase_3.5/models/props/TT_sky",
    ToontownGlobals.MinniesMelodyland: "phase_6/models/props/MM_sky",
    ToontownGlobals.TheBrrrgh: "phase_3.5/models/props/BR_sky",
    ToontownGlobals.DonaldsDreamland: "phase_8/models/props/DL_sky",
}

InitialScore = 15
GolfBallRadius = 0.5  # the radius in feet of our golf ball
GolfBallVolume = 4.0 / 3.0 * 3.14159 * (GolfBallRadius ** 3)  # in cubic feet
GolfBallMass = 4.0 # in pounds
GolfBallDensity = GolfBallMass / GolfBallVolume

# multiply a meters value by this constant to get feet
MetersToFeet = 3.2808399
# multiply a feet value by this constant to get meters
FeetToMeters = 1.0 / MetersToFeet

# How much force should the golf ball initiate with? (percentage out of 100)
GolfBallInitialForce = 15
