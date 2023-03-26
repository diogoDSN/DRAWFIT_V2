
# **DRAWFIT_V2**
## Upgraded DRAWFIT bot using HTTP requests and discord.py
The Drawfit project deploys a fully functional programmable discord bot for following draw odds on any soccer game.  
Currently 5 options:

- Bwin
- Betano
- Betclic
- Solverde
- Moosh

## Deploying with docker

1. Create your own discord bot  
To create your own discord bot go to [discord developer portal](https://discord.com/login?redirect_to=%2Fdevelopers) and follow the instructions [here](https://www.pythondiscord.com/pages/guides/pydis-guides/contributing/setting-test-server-and-bot-account/) under ***Setting up a Bot Account*** to create your bot and add it to your server.

2. Fill your bot parameters  
To parametrize the bot copy the ***docker-compose-example.yml*** file and rename it to ***docker-compose.yml***. In the new file fill the first lines, between the START and END comments, with your parameters.

3. Create your ssl certificates  
The certificates should be placed within a ***.certificates*** folder in the root of the project. If you haven't run the project yet you can use the utility script in the root of the project in the following way:

```
sh src/ssl/make_certificates.sh
```

4. Turn the bot on  
After the certificates have been created run the boot with:
```
sudo docker-compose up -d
```

## Accessing the database

The database is exposed on port 45371 of your local machine. If you want o access it there are two available users:
1. drawfit_read_only  
Some of this user's intended uses are backups and data analysis tools.  
Permissions: SELECT on all database tables.

2. postgres  
This user is available as a way to restore your database, but aside from this specific use case it is not recomended.  
Permissions: SUPERUSER.  

If you want to connect with any of these users you will have to create a certidicate with a common name, CN, equal to that of the specific user, drawfit_read_only or postgres, signed by the root CA in the ***.certicates*** folder.

## Notes

To function correctly the bot needs multiple permissions and intents:

> General Permissions to send, read and react to messages on a channel.
 - Allows basic bot functionality;

> Manage Messages Channel Permission
 - Needed for the browse command to transition correclty between pages;

> Server Members Intent
 - **Needed to check permissions;**
 - Collect info on members to costumize answers;
 - Check authors of messages for correct command interactions;