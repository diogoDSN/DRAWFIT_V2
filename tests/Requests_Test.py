import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))) + '/main')


from updates.A_BWIN.RequestBWIN import BWIN_Odds
from updates.B_BETANO.RequestBETANO import BETANO_Odds
from updates.C_SOLVERDE.RequestSOLVERDE import SOLVERDE_Odds
from updates.D_MOOSH.RequestMOOSH import MOOSH_Odds
from updates.E_BETWAY.RequestBETWAY import BETWAY_Odds
from updates.F_BETCLIC.RequestBETCLIC import BETCLIC_Odds



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
