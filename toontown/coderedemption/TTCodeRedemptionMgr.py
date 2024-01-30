from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify

class TTCodeRedemptionMgr(DistributedObject):
    neverDisable = 1
    notify = directNotify.newCategory('TTCodeRedemptionMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        base.codeRedemptionMgr = self

    def delete(self):
        if hasattr(base, 'codeRedemptionMgr'):
            if base.codeRedemptionMgr is self:
                del base.codeRedemptionMgr
        DistributedObject.delete(self)
        return

    def redeemCode(self, code, callback):
        self.notify.debug('redeemCode(%s)' % code)
        self.sendUpdate('redeemCode', [code])
        callback(1, 0)  # Result in failure no matter what, this is not implemented

    def redeemCodeResult(self, context, result, awardMgrResult):
        self.notify.debug('redeemCodeResult(%s, %s, %s)' % (context, result, awardMgrResult))
