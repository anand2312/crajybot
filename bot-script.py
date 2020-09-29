"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import random
import discord
from discord import activity
from discord import guild 
from discord.ext import commands,tasks, menus
import asyncio
from pymongo import MongoClient
from random import choice
from TOKEN import TOKEN
#local mongodb database stuff
client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]

economy_collection = db["econ_data"]
rpg_collection = db["rpg_data"]
store_collection = db["store_data"]

#bot which controls everything; subclass of Client
bot = commands.Bot(command_prefix='.', activity=discord.Activity(type=discord.ActivityType.watching, name="thug_sgt"))

channels_available = ["bot-test","botspam-v2","botspam"] #Channels where the bot works
chat_money_channels = ['another-chat']
bot.remove_command('help') 
#Lets us implement our own help command instead of the built in one
class HelpMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        response = discord.Embed(title = "Help", description = "Click on the appropriate emoji.")
        response.add_field(name = "Economy Commands", value = "Click on the 🤑 emoji.", inline = False)
        response.add_field(name = "Battle Commands", value = "Click on the ⚔️ emoji", inline = False)
        response.add_field(name = "Moderator Commands", value = "Click on the 🔨 emoji", inline = False)
        response.add_field(name = "Stupid Commands", value = "Click on the 🤪 emoji", inline = False)
        return await ctx.send(embed=response)

    @menus.button('🤑')
    async def economy_help(self, payload):
        embed = discord.Embed(title="Economy Commands", description="List of Economy commands")
        embed.add_field(name="Income commands", value="work, slut, crime", inline=False)
        embed.add_field(name=".shop", value="Displays available items in shop.", inline=False)
        embed.add_field(name=".inv <user>", value="Displays selected user's inv, if not specified displays your inv", inline=False)
        embed.add_field(name=".buy <number> <item>", value="Buys item from shop.", inline=False)
        embed.add_field(name=".sell <number> <item>", value="Sells item back to shop.", inline=False)
        embed.add_field(name=".bal <user>", value="Displays your balance. Works similar to inv", inline=False)
        embed.add_field(name=".with <amount>", value="Withdraw amount from your bank", inline=False)
        embed.add_field(name=".dep <amount>", value="Deposit amount to bank", inline=False)
        embed.add_field(name=".givemoney <user> <amount>", value="Donate money to others.", inline=False)
        embed.add_field(name=".get-loan <amount>", value="Get a loan of specified amount", inline=False)
        embed.add_field(name=".repay-loan", value="Repay your loan (completely, not bit by bit)", inline=False)
        embed.add_field(name=".roulette <amount> <bet>", value="Roulette", inline=False)
        embed.add_field(name=".rrr <amount>", value="Starts a session of Reverse Russian Roulette", inline=False)
        embed.add_field(name=".cf <amount>", value="Cock fight.", inline=False)
        await self.message.edit(embed=embed)

    @menus.button('🔨')
    async def moderator_help(self, payload):
        embed = discord.Embed(title="Moderator Commands", description = "List of moderator commands")
        embed.add_field(name=".change-money <action> <cash/bank> <user> <amount>", value = "Action can be remove/add/set.")
        embed.add_field(name=".c-inv <action> <amount> <item> <user>", value = "Same actions as $cm, but for inventory.")
        embed.add_field(name=".change-stock <item> <number>", value ="Used to change stock remaining of an item in shop.")
        embed.add_field(name="there are more but i'm lazy", value="pensive", inline=False)
        await self.message.edit(embed=embed)

    @menus.button('🤪')
    async def stupid_help(self, payload):
        embed = discord.Embed(title="Stupid Commands", description = "List of all stupid commands")
        embed.add_field(name=".fancy <text>", value = "Prints fancy version of your text (command can also be .f)", inline=False)
        embed.add_field(name=".love-calc <person1> <person2>", value = "Don't put person1 if you want to use yourself as person1 😳 (command can also be .lc)", inline=False) 
        embed.add_field(name=".weird", value="MaKeS tHe texT lIkE tHis (.w)", inline=False)
        embed.add_field(name=".wat commands", value=".use (-u) \n .add (-a) \n .search (-s)", inline=False)
        embed.add_field(name=".owo", value="makes youw text owoified", inline=False)
        await self.message.edit(embed=embed)
@bot.event
async def on_ready(): #sends this message when bot starts working in #bot-tests
    await bot.get_channel(703141348131471440).send("its popi time!!")

@bot.event   
async def on_message(message):
    #chat money
    if message.author.bot: return
    if str(message.channel) in chat_money_channels:
        economy_collection.update_one({"user":message.author.id}, {"$inc": {"cash": 10}})
    await bot.process_commands(message)

@bot.event    #to be tested!
async def on_member_join(member):
    check = economy_collection.find_one({'user': member.id})
    if check is None:
        economy_collection.insert_one({
                "user" : str(member),
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
#testing some cogs stuff
@bot.command()
@commands.has_any_role("admin","Bot Dev")
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    response = discord.Embed(title="Cog Loaded", description=str(extension), colour=discord.Color.green())
    await ctx.message.channel.send(content=None, embed=response)

@bot.command()
@commands.has_any_role("admin","Bot Dev")
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    response = discord.Embed(title="Cog Unloaded", description=str(extension), colour=discord.Color.red())
    await ctx.message.channel.send(content=None, embed=response)

@bot.command(name='popi')
async def popi(ctx):
    reply = random.choice(["poopi really do be poopie though",f"{ctx.message.author.mention} is a poopie?oh no......"]) #Choice chooses 1 object from the list
    response = discord.Embed(title='popi',description=reply)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='help')
async def help(ctx):
    menu = HelpMenu(clear_reactions_after=300)
    await menu.start(ctx)

#TESTING AUTO PRICE CHANGE OF STOCK
@tasks.loop(seconds =  10800)
async def stock_price():
    rand_sign = random.choice(["+","-"])
    if rand_sign == "+": rand_val = random.randint(1,6)
    else: rand_val = -random.randint(1,6)
    stock_data = store_collection.find_one({'name':'Stock'})
    new_price = stock_data['price'] + rand_val
    store_collection.update_one({'name':'Stock'},{"$inc":{"price":rand_val}})
    await message_channel.send(f"Stock price : {new_price}")

@stock_price.before_loop
async def stock_price_before():
    global message_channel
    await bot.wait_until_ready()
    message_channel = bot.get_channel(704911379341115433)

@tasks.loop(seconds=600)
async def color_loop():
    role = guild.get_role(740456742684459041)
    colors = [discord.Color.green(), discord.Color.red(), discord.Color.blurple(), discord.Color.blue(), discord.Color.teal(), discord.Colour.magenta()]
    await role.edit(colour=random.choice(colors))

@color_loop.before_loop
async def colorloop_before():
    global guild
    await bot.wait_until_ready()
    guild = bot.get_guild(298871492924669954)

#loading cogs

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
