import sys
from os.path import dirname, abspath

sys.path.append(dirname(abspath(__file__)))

from drawfit.bot import DrawfitBot


def main():
    TOKEN = "OTUxOTEzMzQzNDk1NTY5NDY4.YiuYYg.GN4Jlpve1TnCLjJUnNVjSs9L5Uk"

    bot = DrawfitBot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
