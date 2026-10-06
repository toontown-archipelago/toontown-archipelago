import time
from typing import List, Any
from panda3d_crowdcontrol import (
    Panda3DCrowdControlManager,
    CrowdControlEffect,
    TimedCrowdControlEffect
)
from toontown.archipelago.crowdcontrol.constants import GO_SAD_CD_SCNDS
from toontown.archipelago.crowdcontrol.QueuedEffects import RandomTeleportEffect, ForcedDanceEffect


class ToontownCrowdControlManager(Panda3DCrowdControlManager):
    def stop(self):
        avatar = getattr(base, 'localAvatar', None)
        if avatar is not None:
            for effect in list(getattr(avatar, '_crowdControlQueuedEffects', {}).values()):
                effect.cancel()
        for _, effect in list(self.active_timed_effects.values()):
            effect.on_stop()
        super().stop()


class ServerDelegateEffect(CrowdControlEffect):
    def __init__(self, code: str):
        super().__init__(code)

    def on_start(self, viewer: str, parameters: List[Any]) -> bool:
        if not hasattr(base, 'localAvatar') or base.localAvatar is None:
            return False

        try:
            base.localAvatar.sendUpdate("requestApplyCrowdControl", [self.code, viewer])
            return True
        except Exception as e:
            print(f"[CrowdControl] Error dispatching server effect '{self.code}': {e}")
            return False


class GoSadEffect(ServerDelegateEffect):
    def __init__(self):
        super().__init__("go_sad")

    def on_start(self, viewer: str, parameters: List[Any]) -> bool:
        avatar = getattr(base, 'localAvatar', None)
        if avatar is None or avatar.getHp() <= 0:
            return False
        now = time.monotonic()
        if now < getattr(avatar, '_crowdControlGoSadReadyAt', 0):
            return False
        if not super().on_start(viewer, parameters):
            return False
        avatar._crowdControlGoSadReadyAt = now + GO_SAD_CD_SCNDS
        return True


# Client-side Timed Effects

class SpeedBoostEffect(TimedCrowdControlEffect):
    def __init__(self):
        super().__init__("speed_boost", duration=15.0)

    def on_timed_start(self, viewer: str, parameters: List[Any]) -> bool:
        if not hasattr(base, 'localAvatar') or base.localAvatar is None:
            return False

        base.localAvatar.controlManager.setCrowdControlModifier(self.code, movement=2.0)
        base.localAvatar.setSystemMessage(0, f"[Crowd Control] {viewer} gave you Speed Boost!")
        return True

    def on_timed_stop(self) -> bool:
        if hasattr(base, 'localAvatar') and base.localAvatar:
            base.localAvatar.controlManager.clearCrowdControlModifier(self.code)
            base.localAvatar.setSystemMessage(0, "[Crowd Control] Speed Boost ended.")
        return True


class SlowDownEffect(TimedCrowdControlEffect):
    def __init__(self):
        super().__init__("slow_down", duration=15.0)

    def on_timed_start(self, viewer: str, parameters: List[Any]) -> bool:
        if not hasattr(base, 'localAvatar') or base.localAvatar is None:
            return False

        base.localAvatar.controlManager.setCrowdControlModifier(self.code, movement=0.4, rotation=0.5)
        base.localAvatar.setSystemMessage(0, f"[Crowd Control] {viewer} slowed you down!")
        return True

    def on_timed_stop(self) -> bool:
        if hasattr(base, 'localAvatar') and base.localAvatar:
            base.localAvatar.controlManager.clearCrowdControlModifier(self.code)
            base.localAvatar.setSystemMessage(0, "[Crowd Control] Slow Down ended.")
        return True


class LowGravityEffect(TimedCrowdControlEffect):
    def __init__(self):
        super().__init__("low_gravity", duration=15.0)

    def on_timed_start(self, viewer: str, parameters: List[Any]) -> bool:
        if not hasattr(base, 'localAvatar') or base.localAvatar is None:
            return False

        base.localAvatar.controlManager.setCrowdControlModifier(self.code, jump=2.5)
        base.localAvatar.setSystemMessage(0, f"[Crowd Control] {viewer} enabled Low Gravity!")
        return True

    def on_timed_stop(self) -> bool:
        if hasattr(base, 'localAvatar') and base.localAvatar:
            base.localAvatar.controlManager.clearCrowdControlModifier(self.code)
            base.localAvatar.setSystemMessage(0, "[Crowd Control] Low Gravity ended.")
        return True


class InvertedMovementEffect(TimedCrowdControlEffect):
    def __init__(self):
        super().__init__("inverted_movement", duration=20.0)

    def on_timed_start(self, viewer: str, parameters: List[Any]) -> bool:
        avatar = getattr(base, 'localAvatar', None)
        if avatar is None:
            return False
        avatar.controlManager.setCrowdControlModifier(self.code, movement=-1.0, rotation=-1.0)
        avatar.setSystemMessage(0, f"[Crowd Control] {viewer} inverted your movement!")
        return True

    def on_timed_stop(self) -> bool:
        avatar = getattr(base, 'localAvatar', None)
        if avatar is not None:
            avatar.controlManager.clearCrowdControlModifier(self.code)
            avatar.setSystemMessage(0, "[Crowd Control] Your movement is back to normal.")
        return True


class FreezeToonEffect(TimedCrowdControlEffect):
    def __init__(self):
        super().__init__("freeze_toon", duration=5.0)

    def on_timed_start(self, viewer: str, parameters: List[Any]) -> bool:
        if not hasattr(base, 'localAvatar') or base.localAvatar is None:
            return False

        base.localAvatar.disableControls()
        base.localAvatar.setSystemMessage(0, f"[Crowd Control] {viewer} froze your Toon!")
        return True

    def on_timed_stop(self) -> bool:
        if hasattr(base, 'localAvatar') and base.localAvatar:
            base.localAvatar.enableControls()
            base.localAvatar.setSystemMessage(0, "[Crowd Control] You are unfrozen!")
        return True


class ToonSizeEffect(TimedCrowdControlEffect):
    def __init__(self, code, scale, startMessage):
        super().__init__(code, duration=20.0)
        self.scale = scale
        self.startMessage = startMessage
        self.avatar = None

    def on_test(self, viewer: str, parameters: List[Any]) -> bool:
        avatar = getattr(base, 'localAvatar', None)
        return avatar is not None and getattr(avatar, '_crowdControlSizeEffect', None) is None

    def on_timed_start(self, viewer: str, parameters: List[Any]) -> bool:
        if not self.on_test(viewer, parameters):
            return False

        avatar = base.localAvatar
        self.avatar = avatar
        self.originalScale = avatar.getScale()
        avatar._crowdControlSizeEffect = self
        avatar.setScale(self.originalScale * self.scale)
        avatar.setSystemMessage(0, f"[Crowd Control] {viewer} {self.startMessage}!")
        return True

    def on_timed_stop(self) -> bool:
        avatar = self.avatar
        if avatar is not None and getattr(avatar, '_crowdControlSizeEffect', None) is self:
            avatar.setScale(self.originalScale)
            del avatar._crowdControlSizeEffect
            avatar.setSystemMessage(0, "[Crowd Control] You returned to normal size.")
        self.avatar = None
        return True


class GiantToonEffect(ToonSizeEffect):
    def __init__(self):
        super().__init__('giant_toon', 2.0, 'made you GIANT')


class TinyToonEffect(ToonSizeEffect):
    def __init__(self):
        super().__init__('tiny_toon', 0.5, 'made you TINY')


def _make_server_effect(code: str):
    class CustomServerEffect(ServerDelegateEffect):
        def __init__(self):
            super().__init__(code)
    return CustomServerEffect


def register_all_toontown_effects(manager: Panda3DCrowdControlManager):
    """Registers all positive, negative, and timed Crowd Control effects."""

    # Positive Server Rewards
    positive_codes = [
        "heal_toon",
        "minor_heal",
        "gag_restock",
        "jellybeans",
        "gag_xp",
        "unite_toonup",
        "unite_gag",
        "pink_slip",
        "sos_card",
        "cog_summon",
    ]

    # Negative Server Traps
    negative_codes = [
        "damage_15",
        "damage_25",
        "uber_trap",
        "bean_tax",
        "drip_trap",
        "gag_shuffle",
    ]

    for code in positive_codes + negative_codes:
        manager.register_effect(code, _make_server_effect(code))

    manager.register_effect("go_sad", GoSadEffect)
    manager.register_effect("random_teleport", RandomTeleportEffect)
    manager.register_effect("forced_dance", ForcedDanceEffect)

    # Timed Client Movement / Scale Effects
    manager.register_effect("speed_boost", SpeedBoostEffect)
    manager.register_effect("slow_down", SlowDownEffect)
    manager.register_effect("low_gravity", LowGravityEffect)
    manager.register_effect("freeze_toon", FreezeToonEffect)
    manager.register_effect("giant_toon", GiantToonEffect)
    manager.register_effect("tiny_toon", TinyToonEffect)
    manager.register_effect("inverted_movement", InvertedMovementEffect)
