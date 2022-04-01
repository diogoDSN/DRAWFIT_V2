from sys import path
from os.path import dirname, abspath

#path.append(dirname(abspath(__path__)))

from main.updates.A_BWIN.RequestBWIN import BWIN_Odds
from main.updates.B_BETANO.RequestBETANO import BETANO_Odds
from main.updates.C_SOLVERDE.RequestSOLVERDE import SOLVERDE_Odds
from main.updates.D_MOOSH.RequestMOOSH import MOOSH_Odds
from main.updates.E_BETWAY.RequestBETWAY import BETWAY_Odds
from main.updates.F_BETCLIC.RequestBETCLIC import BETCLIC_Odds



def testSiteInfo(webSite, siteName):
    results = webSite()
    print("---" + siteName + " START---")
    for odd in results:
        print(odd)

    print("---" + siteName + " END---\n")


print("START TESTS:\n")

testSiteInfo(BWIN_Odds, "BWIN")
testSiteInfo(BETANO_Odds, "BETANO")
testSiteInfo(SOLVERDE_Odds, "SOLVERDE")
testSiteInfo(MOOSH_Odds, "MOOSH")
testSiteInfo(BETWAY_Odds, "BETWAY")
testSiteInfo(BETCLIC_Odds, "BETCLIC")


print("END TESTS\n")
