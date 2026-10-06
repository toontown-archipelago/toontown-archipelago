import math
import random

from panda3d.core import Point3
from panda3d_crowdcontrol import CrowdControlEffect

from toontown.hood import ZoneUtil


def get_free_place(avatar):
    place = base.cr.playGame.getPlace()
    if place is None or avatar.getHp() <= 0:
        return None
    fsm = getattr(place, 'fsm', None)
    if fsm is None:
        return None
    state = fsm.getCurrentState()
    if state is None or state.getName() != 'walk':
        return None
    if avatar.getTeleporting() or not avatar.controlManager.isEnabled:
        return None
    if not avatar.allowControls:
        return None
    if avatar.emote is not None and avatar.emote.isPlaying():
        return None
    return place


def get_free_outdoor_place(avatar):
    from toontown.safezone.Playground import Playground
    from toontown.town.Street import Street
    from toontown.coghq.CogHQExterior import CogHQExterior
    from toontown.coghq.FactoryExterior import FactoryExterior

    place = get_free_place(avatar)
    if not isinstance(place, (Playground, Street, CogHQExterior, FactoryExterior)):
        return None
    if place.loader.geom.isEmpty() or not render.isAncestorOf(place.loader.geom):
        return None
    return place


def get_teleport_candidates(place):
    from toontown.town.Street import Street
    from toontown.coghq.CogHQExterior import CogHQExterior
    from toontown.coghq.FactoryExterior import FactoryExterior

    if isinstance(place, (CogHQExterior, FactoryExterior)):
        pos = base.localAvatar.getPos(place.loader.geom)
        candidates = []
        for radius in (12, 20, 32):
            for step in range(8):
                angle = step * math.pi / 4
                candidates.append(pos + Point3(math.cos(angle) * radius, math.sin(angle) * radius, 0))
        return candidates

    if isinstance(place, Street):
        planner = getattr(base.cr, 'currSuitPlanner', None)
        branch = place.loader.zoneId
        if planner is None:
            return []
        if ZoneUtil.getCanonicalBranchZone(planner.getZoneId()) != ZoneUtil.getCanonicalBranchZone(branch):
            return []
        candidates = []
        for zoneId, pos in planner.battlePosDict.items():
            zoneId = ZoneUtil.getTrueZoneId(zoneId, branch)
            node = place.loader.zoneDict.get(zoneId)
            if node is not None and not node.isEmpty() and not node.isHidden() and not node.isStashed():
                candidates.append(Point3(pos))
        return candidates

    cached = getattr(place.loader, 'crowdControlTeleportCandidates', None)
    if cached is not None:
        return list(cached)
    return get_playground_teleport_candidates(place.loader.geom)


def get_playground_teleport_candidates(geom, include_hidden=False):
    candidates = []
    for pattern in ('**/npc_origin_*', '**/prop_*tree*_DNARoot',
                    '**/prop_*bench*_DNARoot', '**/prop_*post*_DNARoot',
                    '**/prop_*mailbox*_DNARoot', '**/prop_*lamp*_DNARoot'):
        for node in geom.findAllMatches(pattern):
            if (not include_hidden and node.isHidden()) or node.isStashed():
                continue
            pos = node.getPos(geom)
            for x, y in ((8, 0), (-8, 0), (0, 8), (0, -8),
                         (8, 8), (-8, 8), (8, -8), (-8, -8)):
                candidates.append(pos + Point3(x, y, 0))
    return candidates


def find_teleport_destination(avatar, place):
    candidates = get_teleport_candidates(place)
    random.shuffle(candidates)
    anchor = place.loader.geom.attachNewNode('cc-teleport-probe')
    try:
        for candidate in candidates:
            anchor.setPos(candidate - Point3(1, 0, 0))
            if (anchor.getPos(render) - avatar.getPos(render)).lengthSquared() < 100:
                continue
            offset = avatar.positionExaminer.consider(anchor, Point3(1, 0, 0), 3)
            if offset is not None:
                return render.getRelativePoint(anchor, offset)
    finally:
        anchor.removeNode()
    return None


class QueuedOutdoorEffect(CrowdControlEffect):
    label = ''
    queueHint = 'you can move freely outdoors'

    def on_start(self, viewer, parameters):
        self.avatar = getattr(base, 'localAvatar', None)
        if self.avatar is None:
            return False
        pending = getattr(self.avatar, '_crowdControlQueuedEffects', None)
        if pending is None:
            pending = self.avatar._crowdControlQueuedEffects = {}
        if self.code in pending:
            return False
        self.viewer = viewer
        self.taskName = self.avatar.uniqueName(f'cc-queued-{self.code}')
        pending[self.code] = self
        try:
            if self._tryApply():
                self.cancel()
                return True
            taskMgr.doMethodLater(0.5, self._poll, self.taskName)
            self.avatar.setSystemMessage(0, f"[Crowd Control] {viewer}'s {self.label} is queued until {self.queueHint}.")
            return True
        except Exception as error:
            self.cancel()
            print(f"[CrowdControl] Failed to start {self.code}: {error}")
            return False

    def _tryApply(self):
        place = get_free_outdoor_place(self.avatar)
        return place is not None and self.applyInPlace(place)

    def _poll(self, task):
        if getattr(base, 'localAvatar', None) is not self.avatar:
            self.cancel()
            return task.done
        try:
            if self._tryApply():
                self.cancel()
                return task.done
        except Exception as error:
            self.cancel()
            self.avatar.setSystemMessage(0, f"[Crowd Control] Queued {self.label} could not be applied.")
            print(f"[CrowdControl] Failed to apply {self.code}: {error}")
            return task.done
        return task.again

    def cancel(self):
        taskMgr.remove(self.taskName)
        pending = getattr(self.avatar, '_crowdControlQueuedEffects', {})
        if pending.get(self.code) is self:
            pending.pop(self.code)


class RandomTeleportEffect(QueuedOutdoorEffect):
    label = 'Random Teleport'

    def __init__(self):
        super().__init__('random_teleport')

    def applyInPlace(self, place):
        destination = find_teleport_destination(self.avatar, place)
        if destination is None:
            return False
        self.avatar.setPos(render, destination)
        self.avatar.setHpr(render, random.uniform(0, 360), 0, 0)
        self.avatar.controlManager.currentControls.oneTimeCollide()
        self.avatar.d_broadcastPositionNow()
        self.avatar.setSystemMessage(0, f"[Crowd Control] {self.viewer} teleported you to a random spot!")
        return True


class ForcedDanceEffect(QueuedOutdoorEffect):
    label = 'Forced Dance'
    queueHint = 'you can move freely'

    def __init__(self):
        super().__init__('forced_dance')

    def _tryApply(self):
        place = get_free_place(self.avatar)
        return place is not None and self.applyInPlace(place)

    def applyInPlace(self, place):
        self.avatar.sendUpdate('requestApplyCrowdControl', [self.code, self.viewer])
        return True
