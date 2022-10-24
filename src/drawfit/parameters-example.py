# System path to your discord bot token
TOKEN_PATH = "/path/to/token/token.txt"
# System path to where your save will be
SAVE_PATH = "/path/where/to/save" + "drawfit_save.pickle"

# Commands and updates channels dictionaries. Fill with the servers and their respective channels you want to use.
COMMAND_CHANNELS = {'your server1' : ['a command channel'], 'your server2' : ['a command channel']}
UPDATES_CHANNELS = {'your server1' : ['an update channel'], 'your server2' : ['an update channel']}
QUERIES_CHANNELS = {'your server1' : ['a query channel'  ], 'your server2' : ['a query channel'  ]}



# Permissions dictionary. Fill the lists with the usernames of the users that have each permission. 
from drawfit.bot.permissions import Permissions
PERMISSIONS = {Permissions.OWNER: ['UserOwner#1234'], \
               Permissions.MODERATOR: ['UserModerator#0000'], \
               Permissions.NORMAL: ['UserNormal#4321']}

# Input the bots timezone (pytz name)
TIME_ZONE = 'Example/Timezone'