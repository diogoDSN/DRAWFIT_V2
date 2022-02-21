from requests_html import HTMLSession
from bs4 import BeautifulSoup


BWIN_LIGA_ITALIA_SERIE_B = "https://sports.bwin.pt/pt/sports/futebol-4/apostar/it%C3%A1lia-20/s%C3%A9rie-b-102848"
EQUIPA = "Ascoli"

def get_odd(equipa1, equipa2, liga, verbose=False):
    """
    Returns:    The odd if it was found
    Throws:     OddNotFoundException if odd was not found
    """

    session = HTMLSession()
    if (verbose):
        print("GET " + liga)
    liga_page = session.get(liga)
    if (verbose):
        print("Rendering...")
    liga_page.html.render(timeout=99999, wait=5, retries=20)

    # Parse the html TODO
    if (verbose):
        print("Parsing Soup")

    soup = BeautifulSoup(liga_page.html.html, 'html.parser')

    print("Soup:\n" + soup.prettify())


    i=0
    for game in soup.find_all(class_="grid-event ms-active-highlight ng-star-inserted"):
        i += 1
        teams = game.find_all(class_="participant")
        print("Jogo " + str(i) + ":\t" + teams[0].string + " vs " + teams[1].string + "\n")
    return 0


get_odd(0, 1, BWIN_LIGA_ITALIA_SERIE_B, verbose=True)

#try:
 #   print(get_odd(EQUIPA, BWIN_LIGA_ITALIA_SERIE_B))
#catch TODO