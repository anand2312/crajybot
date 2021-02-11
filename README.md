# Crajy Bot
Discord bot for our server, built with discord.py and MongoDB.

### Requirements
- Python 3.7 +
- Python pip - to install dependencies.
- PostgreSQL
- [A RapidAPI Key](https://rapidapi.com/marketplace) - some commands in the `stupid` cog need APIs. If you do not want to use them, you can remove the code for those commands from that cog.

### Setup
1. Clone the repository
2. Go through the setup procedure exposed by manage.py. Run
```python manage.py```
and pick the `setup` option.
3. It's that simple! Test run the bot with
```python manage.py``` and picking the `run` option.

### Points to remember
- This bot wasn't made with _releasing to public_ in mind, and as such some features may not work.
- This bot was made **very** specifically with our private Discord server in mind, and as such the bot will probably not work very well in _multiple_ servers at once. One running instance of the bot will serve _one_ server very well, but *may* get mixed up with different servers. 
 
 ### Setting up manually
 In case you want to set the files containing secrets yourself, this is the structure you'll have to follow:
 ###### secret/TOKEN.py
 ```python
 TOKEN = <your bot token>
 ```
 ###### secret/KEY.py
 ```python
 KEY = <your rapidapi key>
 ```
 ###### secret/constants.py
 ```python
 GUILD_ID = <the ID of the primary server where the bot will function>
 ROLE_NAME = <the ID of a role, who's name the bot will change periodically  ---see cogs/stupid.py for more information.>
 CHAT_MONEY_CHANNELS = [list of channel IDs where users will earn currency for chatting]
 GENERAL_CHAT = <ID of the server general chat>
 BOT_COMMANDER_ROLES = [list of IDs of roles that should be allowed to use bot moderator commands]
 BOT_ANNOUNCE_CHANNEL = <channel ID where the bot can announce stuff (stock price changing, bot online etc)
 DEFAULT_COGS = [list of cogs you want to be loaded when you run the bot. use the same file names as you see in the cogs folder, WITHOUT THE .py part. For example, 'amongus', 'minecraft']
 DB_CONNECTION_STRING = <postgres database connection string.>
 ```
### Hosting
You can host the bot virtually anywhere.
We've used [GCP](https://cloud.google.com/), and it works *very* well. The lowest end VM can comfortably run the bot.

### Disclaimer
We are in no way responsible if something goes wrong with your server. Use this code at your own risk.

### Support
Contact me on Discord - Ares#7286.
