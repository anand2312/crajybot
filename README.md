# Crajy Bot
Discord bot for our server, built with discord.py and MongoDB.
Well, at least till people started cloning this repository.

### Requirements
- >= Python 3.7 
- Python pip - to install dependencies.
- MongoDB

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
- MongoDB was picked to store data because of 
   1. It's easy to set up
   2. It's easy to use
 I've used the `PyMongo` MongoDB driver, which isn't async (it blocks.) 
 The database and driver runs fast enough, but this is because the data is small (only a few thousand documents at _max_) and the server is running on localhost on the same VM as the bot. **BUT** if you plan on using this in more servers/under more load, definitely don't use PyMongo - use Motor, the async mongo driver, OR use PostgreSQL (asyncpg is _really_ fast)
 
Contact me on Discord Ares#7286 if you have any issues!
