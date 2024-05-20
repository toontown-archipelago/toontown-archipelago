from . import Street

class BRStreet(Street.Street):

    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)

    def enter(self, requestStatus):
        Street.Street.enter(self, requestStatus)
        self.loader.hood.setFog()

    def exit(self):
        Street.Street.exit(self)
        self.loader.hood.setNoFog()
