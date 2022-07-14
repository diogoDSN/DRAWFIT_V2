import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))


import drawfit.bot.drawfit_bot as dbot
from drawfit.parameters import TOKEN_PATH
from discord.errors import LoginFailure

def main():

    with open(TOKEN_PATH, 'r') as f:
        TOKEN = f.readline()[:-1]

    bot = dbot.DrawfitBot()
    try:
        bot.run(TOKEN)
    except LoginFailure:
        print(f"The login failed! Token passed (between \"\"):\n\"{TOKEN}\"")

if __name__ == "__main__":
    main()
