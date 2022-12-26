import argparse
import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))


import drawfit.bot.drawfit_bot as dbot
from drawfit.parameters import TOKEN_PATH
from discord.errors import LoginFailure
from drawfit.utils import DEBUG_MODE, SHELL_MODE

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-s', '--shell', action='store_true')
    
    args = parser.parse_args()
    
    DEBUG_MODE = args.debug
    SHELL_MODE = args.shell
        
    
    # Run bot
    with open(TOKEN_PATH, 'r') as f:
        TOKEN = f.readline()[:-1]

    bot = dbot.DrawfitBot()
    try:
        bot.run(TOKEN)
    except LoginFailure:
        print(f"The login failed! Token passed (between \"\"):\n\"{TOKEN}\"")

if __name__ == "__main__":
    main()
