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
    await bot.get_channel(703141348131471440).send("Bruh")


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

def check_date(jsondata, authordata):         #Is called inside ask_date()
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


@bot.command(name='battle')
async def battle(ctx,person:discord.Member):
    battle_state = await begin_battle(ctx,person,ctx.message.author)
   

    
    
    
    
async def begin_battle(ctx,person,author):  #main sub function 1
    author = ctx.message.author
    await send_challenge(ctx,person)
    reply = await get_reply(ctx,person)
    battle_state = await check_reply(ctx,person,reply)
    display_beginning_stats(ctx,author,person)
    return battle_state

async def send_challenge(ctx,person):
    msg = discord.Embed(title='Battle', description=f'{ctx.author.mention} challenges {person.mention} to a battle \n\n {person.mention} do you accept?')
    await ctx.message.channel.send(embed=msg)

async def get_reply(ctx,person):
    def check(m): 
        nonlocal person
        if m.content in ['yes','no'] and m.author == person:
            return True

    reply = await bot.wait_for('message',check=check)
    return reply.content

async def check_reply(ctx,person,reply):
    if reply == 'yes':
        msg = discord.Embed(title='Battle', description=f'{person.mention} has accepted the challenge')
        msg.add_field(name='Challenger', value=ctx.author.name)
        msg.add_field(name='Challengee', value=person.name)
        await ctx.message.channel.send(embed = msg)
        return True
    elif reply == 'no':
        msg = discord.Embed(title='Battle', description=f'{person.mention} has declined the challenge')
        await ctx.message.channel.send(embed = msg)
        return False

async def display_beginning_stats(ctx,person,author):
    data = open("horo-data.json","r")
    data_horo = json.load(data)
    stats_beginning = discord.Embed(title='Battle: Stats')
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name=author.name, value=data_horo[1]['Zodiac'])
    stats_beginning.add_field(name=person.name, value=data_horo[2]['Zodiac'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Health', value=data_horo[1]['hp'])
    stats_beginning.add_field(name='Health', value=data_horo[2]['hp'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Attack', value=data_horo[1]['attack'])
    stats_beginning.add_field(name='Attack', value=data_horo[2]['attack'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Defense', value=data_horo[1]['defense'])
    stats_beginning.add_field(name='Defense', value=data_horo[2]['defense'])
    await ctx.channel.send(embed=stats_beginning)



bot.run(token)