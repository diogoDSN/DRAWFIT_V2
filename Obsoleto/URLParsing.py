import requests as r
from urllib import parse as parse

url = parse.urlparse("https://cds-api.bwin.pt/bettingoffer/fixtures?x-bwin-accessid=YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx&lang=pt&country=PT&userCountry=PT&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds=4&regionIds=20&competitionIds=102848&skip=0&take=50&sortBy=Tags")


print(str(url) + "\n\n")

string = ""
for c in url[4]:
    if c != "&":
        string += c
    else:
        print(string)
        string = ""
