from panda3d.core import Vec4
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.FunctionInterval import Wait, Func

PULSE_GUI_DURATION = 0.2
PULSE_GUI_CHANGE = 0.5


def cleanup(name):
    taskMgr.remove(name)


def start(ival):
    cleanup(ival.getName())
    ival.start()
    return ival


def loop(ival):
    cleanup(ival.getName())
    ival.loop()
    return ival


def getPulseLargerIval(np, name, duration=PULSE_GUI_DURATION, scale=1):
    return Parallel(
        getPulseIval(np.container, name, 1 + PULSE_GUI_CHANGE, duration=duration, scale=scale),
        Sequence(
            np.colorScaleInterval(PULSE_GUI_DURATION, Vec4(0, 1.0, 0, 1), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0),
                                  blendType='easeOut', name=name),
            np.colorScaleInterval(PULSE_GUI_DURATION, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=Vec4(0, 1.0, 0, 1),
                                  blendType='easeIn', name=name)
        )
    )


def getPulseSmallerIval(np, name, duration=PULSE_GUI_DURATION, scale=1):
    return Parallel(
        getPulseIval(np.container, name, 1 - PULSE_GUI_CHANGE, duration=duration, scale=scale),
        Sequence(
            np.colorScaleInterval(PULSE_GUI_DURATION, Vec4(1.0, 0, 0, 1), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0),
                                  blendType='easeOut', name=name),
            np.colorScaleInterval(PULSE_GUI_DURATION, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=Vec4(1.0, 0, 0, 1),
                                  blendType='easeIn', name=name)
        )
    )


def getPulseIval(np, name, change, duration=PULSE_GUI_CHANGE, scale=1):
    return Sequence(np.scaleInterval(duration, scale * change, blendType='easeOut'),
                    np.scaleInterval(duration, scale, blendType='easeIn'), name=name, autoFinish=1)


def getPresentGuiIval(np, name, waitDuration=0.5, moveDuration=1.0, parent=aspect2d, startPos=(0, 0, 0)):
    endPos = np.getPos()
    np.setPos(parent, startPos[0], startPos[1], startPos[2])
    return Sequence(Func(np.show), getPulseLargerIval(np, '', scale=np.getScale()), Wait(waitDuration),
                    np.posInterval(moveDuration, endPos, blendType='easeInOut'), name=name, autoFinish=1)


def getFlashIval(np, name, duration=PULSE_GUI_DURATION, color=Vec4(1, 0, 0, 1)):
    return Sequence(
        Wait(.5),
        np.colorScaleInterval(duration, color, startColorScale=Vec4(1.0, 1.0, 1.0, 1.0),
                              blendType='easeInOut', name=name),
        np.colorScaleInterval(duration, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=color,
                              blendType='easeInOut', name=name)

    )
