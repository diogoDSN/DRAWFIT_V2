import requests as r
from urllib import parse as parse

url = parse.urlparse("https://offer.cdn.begmedia.com/api/pub/v2/competitions/30?application=1024&countrycode=pt&fetchMultipleDefaultMarkets=true&forceCompetitionInfo=true&language=pt&sitecode=ptpt")


print(str(url) + "\n\n")

string = ""
for c in url[4]:
    if c != "&":
        string += c
    else:
        print(string)
        string = ""
