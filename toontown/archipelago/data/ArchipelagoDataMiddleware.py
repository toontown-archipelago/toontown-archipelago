import dataclasses
from collections import defaultdict
from typing import TYPE_CHECKING

from toontown.archipelago.apclient.archipelago_client import ArchipelagoClient
from toontown.archipelago.util.net_utils import NetworkItem

if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


@dataclasses.dataclass
class ArchipelagoDataMiddleware:
    """
    Created on the AI server. Processes data such as hints relevant to one toon.
    """

    toon: "DistributedToonAI"
    client: ArchipelagoClient
    hints: dict[int, list[tuple[int, int]]] = dataclasses.field(default_factory=lambda: defaultdict(list))
    foundItems: dict[int, set[tuple[int, int]]] = dataclasses.field(default_factory=lambda: defaultdict(set))
    # maps Item to Location

    notify = directNotify.newCategory("ArchipelagoDataMiddleware")
    duTask = None

    def parsePrintJSON(self, data: dict):
        # This is somewhat temporary, if expanded should be key-mapped probably, but for 1 case 'if' works fine
        if data.get("type") != "Hint" and data.get("type") != "ItemSend":
            return

        receiver: int = data["receiving"]
        item: NetworkItem = data["item"]
        if receiver == self.client.slot:
            foundHint = (item.player, item.location)
            if data["type"] == "Hint" and foundHint not in self.hints[item.item]:
                self.hints[item.item].append(foundHint)
                self.attemptDistributedUpdate()
            elif data["type"] == "ItemSend":
                self.foundItems[item.item].add(foundHint)
                if foundHint not in self.hints[item.item]:
                    self.hints[item.item].append(foundHint)
                self.attemptDistributedUpdate()

    def getPlayerName(self, player):
        # We do a custom override so we don't display our own name on hints
        if player == self.client.slot:
            return ""
        return self.client.getPlayerName(player)

    def attemptDistributedUpdate(self):
        # This is done so we don't send 50 distributed updates in a row bricking the client for 10 seconds
        if self.duTask is None:
            self.duTask = taskMgr.doMethodLater(0.7, self.distributedUpdate, "archi-data-update", extraArgs=[])

    def distributedUpdate(self):
        self.toon.sendUpdate(
            "setArchipelagoData",
            [
                [(itemId, [
                    (self.getPlayerName(player), address, (player, address) in self.foundItems[itemId]) for player, address in datas
                ]) for itemId, datas in self.hints.items()]
            ]
        )
        self.duTask = None
