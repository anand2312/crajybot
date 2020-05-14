"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import random
import discord 
from discord.ext import commands
from pymongo import MongoClient

#mongodb initialization for economy stats
client = MongoClient("mongodb+srv://shriram:a1s2d3f4g5@cluster0-efytb.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.botuserdata

#bot token stuff; not to be messed with :linus_gun:
token_ = "NzA5NDA3MjY4NDg3MDM3MDE5.XrllLQ.FbL2vivvNxjxPT-wOfAvH32fK4QZ"
token = token_[:len(token_)-1]

#bot which controls everything; subclass of Client
bot = commands.Bot(command_prefix='$')

channels_available = ["bot-test","botspam-v2","botspam"] #Channels where the bot works
bot.remove_command('help') 
#Lets us implement our own help command instead of the built in one

@bot.event
async def on_ready(): #sends this message when bot starts working in #bot-tests
    await bot.get_channel(703141348131471440).send("I'm ready to fuck your mom.")

#ctx stands for context
@bot.command(name='members') #name of the command $members
async def returnMembers(ctx):
    membercount = ctx.guild.member_count #guild refers to the server.
    response = discord.Embed(title="Members" , description=f"""Number of members = {membercount}""") #Embed is what displays it in a box thing (I think)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='popi')
async def popi(ctx):
    reply = random.choice(["poopi really do be poopie though",f"{ctx.message.author.mention} is a poopie?oh no......"]) #Choice chooses 1 object from the list
    response = discord.Embed(title='popi',description=reply)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='help')
async def help(ctx):
    response = discord.Embed(title='Help',description='List of commands')
    response.add_field(name="$popi", value="popi", inline = False)
    response.add_field(name="$members", value="Returns number of members in server", inline = False)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

#ECONOMY CODE; ADD SPACE ABOVE THIS FOR OTHER UNRELATED FUNCTIONS PLEASE :linus_gun:

@bot.command(name='bal')
async def balance(ctx):
    data_bal = db.economyvalues.find_one({"name":str(ctx.message.author)})

    response = discord.Embed(title=str(ctx.message.author), description="Your Balance is:")
    response.add_field(name="Bank balance : ",value=f"{data_bal['bal']}", inline = False)
    response.add_field(name="Debt : ",value=f"{-(data_loan["debt"])}", inline = False)
    response.add_field(name="Net Worth : ",value=f"{data_bal['bal']-data_loan["debt"]}", inline = False)
    #all this is for 1) in Bank, 2) Debt, 3) Total bal

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name='work')
async def work(ctx):
    data_earn = db.economyvalues.find_one({"name":str(ctx.message.author)})
    curr_bal = data_earn["bal"]
    rand_val = random.randint(35,150)
    
    response = discord.Embed(title=str(ctx.message.author),description=f"You earned {rand_val}",colour=discord.Colour.green())

    db.economyvalues.update_one({"name":str(ctx.message.author)} , {'$set':{"bal" : rand_val + curr_bal}})
 
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name="rl" or "req-loan" or "request-loan") #self explanatory tbh
async def loan(ctx,loan_val:int):
    data_loan=db.economyvalues.find_one({"name":str(ctx.message.author)}) #Accessing values from mongo server
    curr_loan=data_loan["debt"] #Checking if any debt on the user

    response = discord.Embed(title=str(ctx.message.author),description=f"You took a loan of {loan_val}!",colour=discord.Colour.red()) # red bc u did a dum dum

    db.economyvalues.update_one({"name":str(ctx.message.author)} , {'$set':{"debt" : loan_val + curr_loan,"bal" : data_loan["bal"] + loan_val}}) 
    #updating debt and balance of user in mongo sever
    
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

bot.run(token)

