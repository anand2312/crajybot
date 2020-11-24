"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import random

import datetime

import discord
from discord.ext import commands, tasks, menus

import asyncio
from aiohttp import ClientSession
from pymongo import MongoClient

from random import choice
from secret.TOKEN import TOKEN
from secret.constants import *
from utils.help_class import HelpCommand
from utils.timezone import BOT_TZ

intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix='.',
                   activity=discord.Activity(type=discord.ActivityType.watching, name="thug_sgt"),
                   help_command=HelpCommand(),
                   intents=intents)

bot.session = ClientSession()   #aiohttp clientsession
 
bot.mongo = MongoClient("mongodb://localhost:27017/")   #mongodb database
db = bot.mongo["bot-data"]

bot.economy_collection = db["econ_data"]
bot.store_collection = db["store_data"]
bot.games_leaderboard = db["games"]
bot.stupid_collection = db["stupid"]
bot.notes_collection = db["notes"]
bot.bday_collection = db["bday"]
bot.pins_collection = db["pins"]
bot.role_names_collection = db["role"]
 
@bot.event
async def on_ready(): # sends this message when bot starts working in #bot-tests
    await bot.get_channel(BOT_ANNOUNCE_CHANNEL).send("Online!")
    print("Bot Running!")

@bot.event   
async def on_message(message):
    #chat money. 
    if message.author.bot: return
    if message.channel.id in CHAT_MONEY_CHANNELS:
        bot.economy_collection.update_one({"user":message.author.id}, {"$inc": {"cash": 10}})
    await bot.process_commands(message)

@bot.event    #adds a new user to the bot database
async def on_member_join(member):
    check = bot.economy_collection.find_one({'user': member.id})
    if check is None:
        bot.economy_collection.insert_one({
                "user" : member.id,
                "cash" : 0,
                "bank" : 2500,
                "inv" : 
                    {"stock": 0, "chicken": 0, "heist tools": 0, "role name": 0},
                "debt" : 0,
                "zodiac_sign" : ""
            })
        await member.send("You have been added to our bot database!")
    else:
        return

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Command errored", color=discord.Color.red())
    if isinstance(error, commands.CommandOnCooldown):
        embed.description = f"Time remaining = {int(error.retry_after/60)} mins"
        return await ctx.send(embed=embed)
    else:
        embed.description = str(error)
        return await ctx.send(embed=embed)

@bot.command(name='popi')   #bot ping command
async def popi(ctx):
    reply = random.choice(["poopi really do be poopie though",f"{ctx.author.mention} is a poopie?oh no......"]) #Choice chooses 1 object from the list
    response = discord.Embed(title='popi',description=reply)
    response.set_footer(text=f"Ping- {bot.latency * 1000} ms")
    return await ctx.send(embed=response)

@bot.command()      
@commands.has_any_role(*BOT_COMMANDER_ROLES)
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        response = discord.Embed(title="Cog Loaded", description=extension, color=discord.Color.green())
    except Exception as e:
        response = discord.Embed(title=f"{extension} cog load failed", description=str(e), color=discord.Color.red())
    await ctx.send(embed=response)

@bot.command()
@commands.has_any_role(*BOT_COMMANDER_ROLES)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    response = discord.Embed(title="Cog Unloaded", description=extension, colour=discord.Color.red())
    await ctx.send(embed=response)

#TESTING AUTO PRICE CHANGE OF STOCK
@tasks.loop(hours=3)
async def stock_price():
    rand_sign = random.choice(["+","-"])
    if rand_sign == "+": rand_val = random.randint(1,6)
    else: rand_val = -random.randint(1,6)
    stock_data = bot.store_collection.find_one({'name':'Stock'})
    new_price = stock_data['price'] + rand_val
    bot.store_collection.update_one({'name': 'Stock'}, {"$inc": {"price": rand_val}})
    await message_channel.send(f"Stock price : {new_price}")

@stock_price.before_loop
async def stock_price_before():
    global message_channel
    await bot.wait_until_ready()
    message_channel = bot.get_channel(BOT_ANNOUNCE_CHANNEL)

@tasks.loop(hours=24)
async def birthday_loop():
    data = bot.bday_collection.find()
    for person in data:
        if person['date'].strftime("%d-%B") == datetime.datetime.now(BOT_TZ).strftime('%d-%B'):
            person_obj = discord.utils.get(guild.members, name=person['user'].split("#")[0])
            await wishchannel.send(f"It's {person_obj.mention}'s birthday today! @here")

@birthday_loop.before_loop
async def birthdayloop_before():
    global guild
    global wishchannel
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)
    wishchannel = guild.get_channel(GENERAL_CHAT)

#loading cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

birthday_loop.start()
stock_price.start()

bot.run(TOKEN)
