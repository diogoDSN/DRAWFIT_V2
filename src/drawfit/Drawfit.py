import argparse
import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))


import drawfit.bot.drawfit_bot as dbot
import drawfit.parameters as prm
from discord.errors import LoginFailure

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-s', '--shell', action='store_true')
    
    args = parser.parse_args()
    prm.DEBUG_MODE = (not prm.DEBUG_MODE) if args.debug else prm.DEBUG_MODE
    prm.SHELL_MODE = (not prm.SHELL_MODE) if args.shell else prm.SHELL_MODE
    
    # Run bot
    with open(prm.TOKEN_PATH, 'r') as f:
        TOKEN = f.readline()[:-1]

    bot = dbot.DrawfitBot()
    try:
        bot.run(TOKEN)
    except LoginFailure:
        print(f"The login failed! Token passed (between \"\"):\n\"{TOKEN}\"")

if __name__ == "__main__":
    main()
