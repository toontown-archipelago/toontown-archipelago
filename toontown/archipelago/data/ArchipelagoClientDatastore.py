import dataclasses


@dataclasses.dataclass
class ArchipelagoClientDatastore:
    hints: dict[int, list[tuple[str, int, bool]]] = dataclasses.field(default_factory=dict)

    def setHints(self, hints):
        self.hints = dict(hints)
        if hasattr(base.localAvatar, "checkPage"):
            base.localAvatar.checkPage.regenerateScrollList()

    def getHint(self, itemId):
        return self.hints.get(itemId, [])
