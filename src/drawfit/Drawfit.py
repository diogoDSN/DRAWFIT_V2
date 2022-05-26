import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))

import drawfit.bot.drawfit_bot as dbot

def main():

    with open("/tmp/test_token.txt", 'r') as f:
        TOKEN = f.readline()[:-1]

    bot = dbot.DrawfitBot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
