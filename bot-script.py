"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import random
import discord 
from discord.ext import commands,tasks
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
bot = commands.Bot(command_prefix='.')

channels_available = ["bot-test","botspam-v2","botspam"] #Channels where the bot works
chat_money_channels = ['another-chat']
bot.remove_command('help') 
#Lets us implement our own help command instead of the built in one

@bot.event
async def on_ready(): #sends this message when bot starts working in #bot-tests
    await bot.get_channel(703141348131471440).send("its popi time!!")
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name="thug_sgt"))

@bot.event   
async def on_message(message):
    #chat money
    if str(message.channel) in chat_money_channels:
        economy_collection.find_one_and_update({"user":str(message.author)}, {"$inc":{"cash":10}})
    await bot.process_commands(message)

@bot.event    #to be tested!
async def on_member_join(member):
    check = economy_collection.find_one({'user':str(member)})
    if check is None:
        economy_collection.insert_one({
                "user" : str(member),
                "cash" : 0,
                "bank" : 2500,
                "inv" : 
                    {"stock" : 0, "chicken" : 0, "heist tools" : 0},
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
    response = discord.Embed(title = "Help", description = "Click on the appropriate emoji within 10 seconds")
    response.add_field(name = "Economy Commands", value = "Click on the 🤑 emoji.", inline = False)
    response.add_field(name = "Battle Commands", value = "Click on the ⚔️ emoji", inline = False)
    response.add_field(name = "Moderator Commands", value = "Click on the 🔨 emoji", inline = False)
    response.add_field(name = "Stupid Commands", value = "Click on the 🤪 emoji", inline = False)
    message = await ctx.message.channel.send(content = None, embed = response)

    await message.add_reaction('🤑')
    await message.add_reaction('⚔️')
    await message.add_reaction('🔨')
    await message.add_reaction('🤪')
    await asyncio.sleep(10)

    message = await ctx.message.channel.fetch_message(message.id)
    rxns = message.reactions
    for i in rxns:
        if i.count > 1:
            if i.emoji == '🤑':
                embed=discord.Embed(title="Economy Commands", description="List of Economy commands")
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
                await message.edit(content = None, embed = embed)
            elif i.emoji == '⚔️':   
                embed = discord.Embed(title="Battle!", description="under development")
                await message.edit(content = None, embed = embed)
            elif i.emoji == '🔨':
                embed = discord.Embed(title="Moderator Commands", description = "List of moderator commands")
                embed.add_field(name=".change-money <action> <cash/bank> <user> <amount>", value = "Action can be remove/add/set.")
                embed.add_field(name=".c-inv <action> <amount> <item> <user>", value = "Same actions as $cm, but for inventory.")
                embed.add_field(name=".change-stock <item> <number>", value ="Used to change stock remaining of an item in shop.")
                await message.edit(content = None, embed = embed)
            elif i.emoji == '🤪':
                embed = discord.Embed(title="Stupid Commands", description = "List of all stupid commands")
                embed.add_field(name=".fancy <text>", value = "Prints fancy version of your text (command can also be .f)")
                embed.add_field(name=".love-calc <person1> <person2>", value = "Don't put person1 if you want to use yourself as person1 😳 (command can also be .lc)") 
                embed.add_field(name=".weird", description="MaKeS tHe texT lIkE tHis (.w)")
            break
"""
#--------------------RPG / HORO FUNCTIONS----------------------
#global variables
battle_ongoing = False
turn_count = 1

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
    sum_ = 0                               #renamed sum to sum_ to retain sum functionality
    for i in range(int(date[1])-1):
        sum_+=days[i]
    sum_+=int(date[0])
    if 0<sum_<19:sum_+=366
    if jsondata["day_low"]<=sum_<=jsondata["day_high"]: return True

def get_zodiac(response):
    data = open("horo-data.json","r")
    data_horo = json.load(data)
    for i in data_horo:
        if check_date(i,response): 
            zodiac = i["Zodiac"]
            data.close()
            return zodiac

def update_json_database(response,sign):
    data = open("rpg-data.json","r")
    rpg_data = json.loads(data.readline())
    data.close()

    for i in rpg_data:
        if i["user"] == str(response.author):
            user_index = rpg_data.index(i)

    rpg_data[user_index]["zodiac_sign"] = sign
    with open("rpg-data.json","w") as data:
        json.dump(rpg_data,data)


@bot.command(name='battle')
async def battle(ctx,person:discord.Member,bet:int):
    if person != ctx.author:
        if battle_ongoing == False:
            battle_state, contestant_data, stats, battle_status = await begin_battle(ctx,person,ctx.message.author,bet)
        if battle_state == True:
            await process_battle(battle_state,ctx,contestant_data,stats,battle_status)
            await end_battle(ctx,contestant_data,bet)
            
    else:
        response = discord.Embed(title='Error',description='Another battle is ongoing. Please wait.')
        await ctx.message.channel.send(embed=response)
    
#Battle beginning    
async def begin_battle(ctx,person,author,bet):
    await send_challenge(ctx,person,author,bet)
    reply = await get_reply(ctx,person)
    battle_state = await check_reply(ctx,person,author,reply.content,bet)
    if battle_state:
        contestant_data = get_contestant_data(person,author)
        #deduct_from_balance(person,author,bet,contestant_data)
        stats, battle_status = await display_beginning_stats(ctx,person,author,contestant_data)
        return battle_state, contestant_data, stats, battle_status
    return battle_state,None,None,None
    

#Sub Functions of Begin Battle:

async def send_challenge(ctx,person,author,bet):
    response = discord.Embed(title='Battle', description=f'{author.mention} challenges {person.mention} to a battle \n\n {person.mention} do you accept?')
    response.add_field(name='Bet', value=str(bet)+" + 5% of your balance if you win")
    await ctx.message.channel.send(embed=response)

async def get_reply(ctx,person):
    def check(m): 
        nonlocal person
        if m.content in ['yes','no'] and m.author == person:
            return True

    return await bot.wait_for('message',check=check)

async def check_reply(ctx,person,author,reply,bet):
    if reply == 'yes':
        response = discord.Embed(title='Battle', description=f'{person.mention} has accepted the challenge')
        response.add_field(name='Challenger', value=author.name)
        response.add_field(name='Challengee', value=person.name)
        response.add_field(name='Winner\'s Prize: ', value=str(2*bet)+' + 5% winner\'s balance')
        global battle_ongoing
        battle_ongoing = True
        return True
        
    elif reply == 'no':
        response = discord.Embed(title='Battle', description=f'{person.mention} has declined the challenge')
        await ctx.channel.send(embed = response)
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
    if econ_data[contestant_data[2]]['cash'] >= bet and econ_data[contestant_data[3]]['cash'] >= bet:
        econ_data[contestant_data[2]]['cash'] -= bet
        econ_data[contestant_data[3]]['cash'] -= bet
        with open('economy-data.json','w') as data:
            json.dump(econ_data,data)


async def display_beginning_stats(ctx,person,author,contestant_data):
    stats_beginning = make_stats_embed(contestant_data)

    starter = discord.Embed(title='The Battle Begins!')

    stats = await ctx.channel.send(embed=stats_beginning)
    battle_status = await ctx.channel.send(embed=starter)

    return stats, battle_status

def make_stats_embed(contestant_data): #Used in process battle too
    author_data = contestant_data[0]
    person_data = contestant_data[1]

    stats_beginning = discord.Embed(title='Battle: Stats')
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name=author_data['user'], value=author_data['zodiac_sign'])
    stats_beginning.add_field(name=person_data['user'], value=person_data['zodiac_sign'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Health', value=author_data['hp'])
    stats_beginning.add_field(name='Health', value=person_data['hp'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Attack', value=author_data['attack'])
    stats_beginning.add_field(name='Attack', value=person_data['attack'])
    stats_beginning.add_field(name='|',value='|')
    stats_beginning.add_field(name='Defense', value=author_data['defense'])
    stats_beginning.add_field(name='Defense', value=person_data['defense'])

    return stats_beginning

#Battle Process
async def process_battle(battle_state,ctx,contestant_data,stats,battle_status):
    player_1 = 0
    player_2 = 0
    global turn_count
    while battle_state:
        if turn_count == 1:player_1, player_2, player_turn = await get_turn(ctx,contestant_data,player_1,player_2)
        if turn_count == 1:action, player_choice = await get_player_choice(ctx,contestant_data,player_1)
        else: action = await get_player_choice(ctx,contestant_data,player_1)
        battle_status_response = await process_action(ctx,contestant_data,player_1,player_2,action.content)
        player_1, player_2 = await update_battle(ctx,contestant_data,player_1,player_2,stats,battle_status,player_turn,player_choice,battle_status_response,action)
        if contestant_data[0]['hp']<=0 or contestant_data[1]['hp']<=0:
            await asyncio.sleep(2)
            await stats.delete()
            await battle_status.delete()
            await player_turn.delete()
            await player_choice.delete()
            battle_state=False
        
    
#Sub Functions of Process Battle:

async def get_turn(ctx,contestant_data,player_1=0,player_2=0):
    global turn_count
    if turn_count == 1: 
        player_1 = choice([0,1])
        if player_1 == 0: player_2 = 1
        else: player_2 = 0
    response = discord.Embed(title=f'Turn {turn_count}: ',description=f"{contestant_data[player_1]['user']}'s Turn")
    player_turn = await ctx.channel.send(embed=response)
    return player_1, player_2, player_turn
    
async def get_player_choice(ctx,contestant_data,player_1):
    global turn_count

    def check(m):
        if str(m.author) == contestant_data[player_1]['user'] and m.content in contestant_data[player_1]['battle_options']: return True

    if turn_count == 1:
        response = discord.Embed(title='Player Choice',description=f''' {contestant_data[player_1]['user']}, What would you like to do?\n{contestant_data[player_1]['battle_options']}''')
        player_choice = await ctx.channel.send(embed=response)
        return await bot.wait_for('message',check=check), player_choice
    return await bot.wait_for('message',check=check)

async def process_action(ctx,contestant_data,player_1,player_2,action):
    if action == 'attack': battle_status_response = await process_attack(ctx,contestant_data,player_1,player_2)
    elif action == 'defend': battle_status_response = await process_defense(ctx,contestant_data,player_1)
    #elif action == 'use item': await process_use_item(ctx,contestant_data,player_1,player_2)  Will implement once items are made
    return battle_status_response

async def update_battle(ctx,contestant_data,player_1,player_2,stats,battle_status,player_turn,player_choice,battle_status_response,action):
    global turn_count
    turn_count+=1
    update_statuses(contestant_data,player_1,player_2)

    new_stats = make_stats_embed(contestant_data)
    new_battle_status = discord.Embed(title='Battle Status:',description=f"{battle_status_response.description}\n{contestant_data[player_1]['user']}'s turn has ended'")
    
    
    player_1, player_2 = player_2, player_1
  

    new_player_turn = discord.Embed(title=f'Turn {turn_count}: ',description=f"{contestant_data[player_1]['user']}'s Turn")
    new_player_choice = discord.Embed(title='Player Choice',description=f''' {contestant_data[player_1]['user']}, What would you like to do?\n{contestant_data[player_1]['battle_options']}''')

    await stats.edit(embed=new_stats)
    await battle_status.edit(embed=new_battle_status)
    await player_turn.edit(embed=new_player_turn)
    await player_choice.edit(embed=new_player_choice)
    await action.delete()
    return player_1, player_2

#Sub functions of update battle:
def update_statuses(contestant_data,player_1,player_2):

    for i in contestant_data[0:1]:
        for j in i['battle_counters']:
            if i['battle_counters'][j][0] >=1:
                i['battle_counters'][j][0]-=1
                if i['battle_counters'][j][0]==0:
                    i[j] -= i['battle_counters'][j][1]

#Sub functions of process action:
async def process_attack(ctx,contestant_data,player_1,player_2):
    damage = contestant_data[player_1]['attack'] - contestant_data[player_2]['defense']//10 + choice([-3,-2,-1,0,1,2,3])
    contestant_data[player_2]['hp'] -= damage
    battle_status_response = discord.Embed(title='Battle Status:',description=f"{contestant_data[player_1]['user']} dealt {damage} damage to the opposing player!")
    return battle_status_response
    
async def process_defense(ctx,contestant_data,player_1):
    contestant_data[player_1]['battle_counters']['defense']=[2,40]
    contestant_data[player_1]['defense'] += 40
    battle_status_response = discord.Embed(title='Battle Status:',description=f"{contestant_data[player_1]['user']} defended!")
    return battle_status_response

#End Battle
async def end_battle(ctx,contestant_data,bet):
    global battle_ongoing
    battle_ongoing = False
    if contestant_data[0]['hp'] == 0:
        winner = contestant_data[2]
    else: winner = contestant_data[3]
    data = open('economy-data.json','r')
    econ_data = json.load(data)
    data.close()
    amt = int(2*bet + 0.05*econ_data[winner]['cash'])
    econ_data[winner]['bal'] += amt
    response = discord.Embed(title=f"{econ_data[winner]['user']} wins!",
    description=f"{econ_data[winner]['user']} wins {amt}")
    with open('economy-data.json','w') as data:
        json.dump(econ_data,data)

    await ctx.channel.send(embed=response)
"""

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

#loading cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#bot.load_extension('cogs.stupid')
stock_price.start()
bot.run(TOKEN)
