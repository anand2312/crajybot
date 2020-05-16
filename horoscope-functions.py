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
    msg = await ask_date(ctx)
    sign = get_zodiac(msg)
    update_json_database(msg,sign)
    response = discord.Embed(title='Horoscope',description=f'Congratulations! You are a {sign}')
    await ctx.message.channel.send(embed=response)
    
async def ask_date(ctx):
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
    return await bot.wait_for('message',check=check)

def check_date(jsondata, authordata):
    date = authordata.content.split('-')
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    sum = 0
    for i in range(int(date[1])-1):
        sum+=days[i]
    sum+=int(date[0])
    if 0<sum<19:sum+=366
    if jsondata["day_low"]<=sum<=jsondata["day_high"]: return True

def get_zodiac(msg):
    data = open("horo-data.json","r")
    data_horo = json.load(data)
    for i in data_horo:
        if check_date(i,msg): 
            zodiac = i["Zodiac"]
            data.close()
            return zodiac

def update_json_database(msg,sign):
    data = open("economy-user-data.json","r")
    econ_data = json.loads(data.readline())
    data.close()

    for i in econ_data:
        if i["user"] == str(msg.author):
            user_index = econ_data.index(i)

    econ_data[user_index]["zodiac_sign"] = sign
    with open("economy-user-data.json","w") as data:
        json.dump(econ_data,data)

bot.run(token)
    