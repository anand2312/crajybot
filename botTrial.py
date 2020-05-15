"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import random
import discord 
from discord.ext import commands
import json

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
    with open("economy-data.json","r") as data:
        data_bal = json.load(data)
    for i in data_bal:
        if i["user"] == str(ctx.message.author):
            user_dict = i                 #gets right dictionary with all user vals from a list of dicts.
    
    networth = user_dict["bal"] - user_dict["debt"]
    
    response = discord.Embed(title=str(ctx.message.author), description="Your Balance is:")
    response.add_field(name="Bank balance : ",value=f"{user_dict['bal']}", inline = False)
    response.add_field(name="Debt : ",value=f"{user_dict['debt'] * (-1)}", inline = False)
    response.add_field(name="Net Worth : ",value=networth, inline = False)
                       #all this is for 1) in Bank, 2) Debt, 3) Total bal

    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

'''@balance.error
async def bal_error(ctx,error):
    pass'''




@bot.command(name='work')
@commands.cooldown(1, 60, commands.BucketType.user)            #remember to increase the cooldown to at least an hour!
async def work(ctx):
        data = open("economy-data.json","r")
        data_bal = json.loads(data.readline())
        data.close()
        for i in data_bal:
            if i["user"] == str(ctx.message.author):
                user_index = data_bal.index(i)
        

        rand_val = random.randint(35,150)
        data_bal[user_index]["bal"] = data_bal[user_index]["bal"] + rand_val
        data = open("economy-data.json","w")
        json.dump(data_bal,data)    #changing value in main json file as well
        data.close()

        response = discord.Embed(title=str(ctx.message.author),description=f"You earned {rand_val}",colour=discord.Colour.green())

    
        if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@bot.command(name="req-loan", aliases = ["rl","request-loan"])    #beta loan command! repayment not yet made
async def loan(ctx,loan_val:int):
    with open("economy-data.json","r") as data:
        loan_data = json.load(data)
    for i in loan_data:
        if i["user"] == str(ctx.message.author):
            user_index = loan_data.index(i)

    response = discord.Embed(title=str(ctx.message.author),description=f"You took a loan of {loan_val}!",colour=discord.Colour.red()) # red bc u did a dum dum

    loan_data[user_index]["debt"] = loan_data[user_index]["debt"] + loan_val
    loan_data[user_index]["bal"] = loan_data[user_index]["bal"] + loan_val
    
    with open("economy-data.json","w") as data:
        json.dump(loan_data,data)
    if ctx.message.channel.name in channels_available: await ctx.message.channel.send(content=None,embed=response)

@work.error
async def work_error(ctx,error):             #only says "CommandOnCooldown", not the time remaining
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send(commands.CommandOnCooldown.__name__)


bot.run(token)

