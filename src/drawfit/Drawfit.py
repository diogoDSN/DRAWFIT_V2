import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))

import drawfit.bot.drawfit_bot as dbot
from drawfit.parameters import TOKEN_PATH

def main():

    with open(TOKEN_PATH, 'r') as f:
        TOKEN = f.readline()[:-1]

    bot = dbot.DrawfitBot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
