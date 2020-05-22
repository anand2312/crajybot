import os
import discord 
import json
from discord.ext import commands
from random import choice

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
    data = open("rpg-data.json","r")
    rpg_data = json.loads(data.readline())
    data.close()

    for i in rpg_data:
        if i["user"] == str(msg.author):
            user_index = rpg_data.index(i)

    rpg_data[user_index]["zodiac_sign"] = sign
    with open("rpg-data.json","w") as data:
        json.dump(rpg_data,data)


@bot.command(name='battle')
async def battle(ctx,person:discord.Member,bet:int):
    battle_state, contestant_data = await begin_battle(ctx,person,ctx.message.author,bet)
    await process_battle(battle_state,ctx,contestant_data)
    
    
#Battle beginning    
async def begin_battle(ctx,person,author,bet):
    await send_challenge(ctx,person,author,bet)
    reply = await get_reply(ctx,person)
    battle_state = await check_reply(ctx,person,author,reply.content,bet)
    contestant_data = get_contestant_data(person,author)
    #deduct_from_balance(person,author,bet,contestant_data)
    await display_beginning_stats(ctx,person,author,contestant_data)
    return battle_state, contestant_data

#Sub Functions of Begin Battle:

async def send_challenge(ctx,person,author,bet):
    msg = discord.Embed(title='Battle', description=f'{author.mention} challenges {person.mention} to a battle \n\n {person.mention} do you accept?')
    msg.add_field(name='Bet', value=bet)
    await ctx.message.channel.send(embed=msg)

async def get_reply(ctx,person):
    def check(m): 
        nonlocal person
        if m.content in ['yes','no'] and m.author == person:
            return True

    return await bot.wait_for('message',check=check)

async def check_reply(ctx,person,author,reply,bet):
    if reply == 'yes':
        msg = discord.Embed(title='Battle', description=f'{person.mention} has accepted the challenge')
        msg.add_field(name='Challenger', value=author.name)
        msg.add_field(name='Challengee', value=person.name)
        msg.add_field(name='Winner\'s Prize: ', value=str(2*bet)+' + 5% winner\'s balance')
        await ctx.channel.send(embed = msg)
        return True
        
    elif reply == 'no':
        msg = discord.Embed(title='Battle', description=f'{person.mention} has declined the challenge')
        await ctx.channel.send(embed = msg)
        return False
    
def get_contestant_data(person,author):
    data = open("rpg-data.json","r")
    data_rpg = json.load(data)
    data.close()
    for i in data_rpg:
        if i['user'] == str(author):
            author_data = i
            author_index = data_rpg.index(i)
        if i['user'] == str(person):
            person_data = i
            person_index = data_rpg.index(i)
    return [author_data,person_data,author_index,person_index]
    
def deduct_from_balance(person,author,bet,contestant_data):
    data = open('economy-data.json','r')
    econ_data = json.load(data)
    data.close()
    econ_data[contestant_data[2]]['bal'] -= bet
    econ_data[contestant_data[3]]['bal'] -= bet
    with open('economy-data.json','w') as data:
        json.dump(econ_data,data)

async def display_beginning_stats(ctx,person,author,contestant_data):
    author_data = contestant_data[0]
    person_data = contestant_data[1]

    stats_beginning = discord.Embed(title='Battle: Stats')
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name=author.name, value=author_data['zodiac_sign'])
    stats_beginning.add_field(name=person.name, value=person_data['zodiac_sign'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Health', value=author_data['hp'])
    stats_beginning.add_field(name='Health', value=person_data['hp'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Attack', value=author_data['attack'])
    stats_beginning.add_field(name='Attack', value=person_data['attack'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Defense', value=author_data['defense'])
    stats_beginning.add_field(name='Defense', value=person_data['defense'])

    starter = discord.Embed(title='The Battle Begins!')

    await ctx.channel.send(embed=stats_beginning)
    await ctx.channel.send(embed=starter)

#Battle Process
async def process_battle(battle_state,ctx,contestant_data):
    turn_count = 0
    player_1 = 0
    player_2 = 0
    while battle_state:
        turn_count+=1
        player_1, player_2 = await get_turn(ctx,contestant_data,turn_count,player_1,player_2)
        action = await get_player_choice(ctx,contestant_data,player_1)
        await process_action(ctx,contestant_data,player_1,player_2,action.content)
        update_statuses(contestant_data,player_1,player_2)
        player_1, player_2 = await change_turn(ctx,contestant_data,player_1,player_2)
    
    

#Sub Functions of Process Battle:

async def get_turn(ctx,contestant_data,turn_count,player_1=0,player_2=0):
    if turn_count == 1: 
        player_1 = choice([0,1])
        if player_1 == 0: player_2 = 1
        else: player_2 = 0
    response = discord.Embed(title=f'Turn {turn_count}: ',description=f"{contestant_data[player_1]['user']}'s Turn")
    await ctx.channel.send(embed=response)
    return player_1, player_2
    
async def get_player_choice(ctx,contestant_data,player_1):
    def check(msg):
        if str(msg.author) == contestant_data[player_1]['user'] and msg.content in contestant_data[player_1]['battle_options']: return True
        
    a = contestant_data[player_1]['battle_options'][0]
    b = contestant_data[player_1]['battle_options'][1]
    c = contestant_data[player_1]['battle_options'][2]
        
    response = f''' {contestant_data[player_1]['user']}, What would you like to do?\n{a,b,c}'''
    await ctx.channel.send(response)
    return await bot.wait_for('message',check=check)

async def process_action(ctx,contestant_data,player_1,player_2,action):
    if action == 'attack': await process_attack(ctx,contestant_data,player_1,player_2)
    elif action == 'defend': await process_defense(ctx,contestant_data,player_1)
    #elif action == 'use item': await process_use_item(ctx,contestant_data,player_1,player_2)  Will implement once items are made

def update_statuses(contestant_data,player_1,player_2):
    for i in contestant_data[0:1]:
        for j in i['battle_counters']:
            if i['battle_counters'][j][0] >=1:
                i['battle_counters'][j][0]-=1
                if i['battle_counters'][j][0]==0:
                    i[j] -= i['battle_counters'][j][1]

async def change_turn(ctx,contestant_data,player_1,player_2):
    response = discord.Embed(title='Battle Outcome: ',description=f"{contestant_data[player_1]['user']}'s turn has ended'")
    player_1, player_2 = player_2, player_1
    await ctx.channel.send(embed=response)
    return player_1, player_2


#Sub functions of process action:
async def process_attack(ctx,contestant_data,player_1,player_2):
    damage = contestant_data[player_1]['attack'] - contestant_data[player_2]['defense']//10 + choice([-3,-2,-1,0,1,2,3])
    contestant_data[player_2]['hp'] -= damage
    response = discord.Embed(title='Battle Status:',description=f"{contestant_data[player_1]['user']} dealt {damage} damage to the opposing player!")
    await ctx.channel.send(embed = response)

async def process_defense(ctx,contestant_data,player_1):
    contestant_data[player_1]['battle_counters']['defense']=[2,40]
    contestant_data[player_1]['defense'] += 40
    response = discord.Embed(title='Battle Status:',description=f"{contestant_data[player_1]['user']} defended!")
    await ctx.channel.send(embed = response)



bot.run(token)