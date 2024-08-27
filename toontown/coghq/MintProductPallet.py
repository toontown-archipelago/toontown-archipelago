from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import MintProduct

class MintProductPallet(MintProduct.MintProduct):
    Models = {CashbotMintIntA: 'phase_10/models/cashbotHQ/DoubleCoinStack.bam',
     CashbotMintIntB: 'phase_10/models/cogHQ/DoubleMoneyStack.bam',
     CashbotMintIntC: 'phase_10/models/cashbotHQ/DoubleGoldStack.bam',
     LawbotStageIntA: 'phase_11/models/lawbotHQ/LB_paper_big_stacks3.bam',
     LawbotStageIntB: 'phase_11/models/lawbotHQ/LB_paper_big_stacks3.bam',
     LawbotStageIntC: 'phase_11/models/lawbotHQ/LB_paper_big_stacks3.bam',
     LawbotStageIntD: 'phase_11/models/lawbotHQ/LB_paper_big_stacks3.bam'}
    Scales = {CashbotMintIntA: 1.0,
     CashbotMintIntB: 1.0,
     CashbotMintIntC: 1.0,
     LawbotStageIntA: 1.0,
     LawbotStageIntB: 1.0,
     LawbotStageIntC: 1.0,
     LawbotStageIntD: 1.0}
