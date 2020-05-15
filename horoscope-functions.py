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

@bot.event
async def on_ready():
    await bot.get_channel(703141348131471440).send("Horoscope tiem!! :quieres:")


@bot.command(name='horo-assign')
async def assign_horoscope(ctx):

    def check(author):
        def inner_check(message):
            if message.author != author:
                return False
            try:
                int(message.content)
                return True
            except ValueError:
                return False
        return inner_check

    response = discord.Embed(title='Horoscope',description='Please enter your date of birth: ')
    await ctx.message.channel.send(embed=response)
    msg = await bot.wait_for('message',check=check)
 
    with open("horo-data.json","r") as data:
        data_horo = json.load(data)
    for i in data_horo:
        if check_date(i,msg): sign = i["Zodiac"]


 
    response = discord.Embed(title='Horoscope',description=f'Congratulations! You are a {sign}')
    await ctx.message.channel.send(embed=response)
    
def check_date(jsondata, authordata):
    date = authordata.content.split('-')
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    sum = 0
    for i in range(int(date[1])-1):
        sum+=days[i]
    sum+=int(date[0])
    if 0<sum<19:sum+=366
    if jsondata["day_low"]<=sum<=jsondata["day_high"]: return True

bot.run(token)
    