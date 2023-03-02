from os import environ

# Commands and updates channels dictionaries. Fill with the servers and their respective channels you want to use.
COMMAND_CHANNELS = {environ['SERVER_NAME'] : [environ['COMMANDS_CHANNEL']]}
UPDATES_CHANNELS = {environ['SERVER_NAME'] : [environ['UPDATES_CHANNEL']]}
QUERIES_CHANNELS = {environ['SERVER_NAME'] : [environ['QUERIES_CHANNEL']]}

# Input the bots timezone (pytz name)
TIME_ZONE = environ['DRAWFIT_TIME_ZONE']

# Logs config
DEBUG_MODE = False
SHELL_MODE = False
