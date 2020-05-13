"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import discord
import random
from pymongo import MongoClient

#mongodb initialization for economy stats
client = MongoClient("mongodb+srv://bot-dev:linusgun@cluster0-efytb.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.botuserdata


#bot token stuff; not to be messed with :linus_gun:
token_ = "NzA5NDA3MjY4NDg3MDM3MDE5.XrllLQ.FbL2vivvNxjxPT-wOfAvH32fK4QZ"
token = token_[:len(token_)-1]

client =  discord.Client()
@client.event
async def on_ready():    #sends this message when bot starts working in #bot-tests
    await client.get_channel(703141348131471440).send("I'm ready to fuck your mom.")

@client.event
async def on_message(message):
    guild_id = client.get_guild(298871492924669954) #server ID variable that gets info from our server
    channels = ["bot-test","botspam-v2","botspam"]  #limiting bot usage to these channels

    if str(message.channel) in channels:
        if message.content[0] == "$":
            if message.content.lower() == "$members":  #returns number of users
                emb1 = discord.Embed(title = "Members" , description = f"""Number of members = {guild_id.member_count}""")
                await message.channel.send(content = None, embed =  emb1)

            elif message.content.lower() == "$popi":   #popi
                n = random.randint(1,2)
                if n == 1:
                    emb2 = discord.Embed(title = "popi" , description = f"poopi really do be poopie though")
                    await message.channel.send(content = None, embed = emb2)
                elif n == 2:
                    emb2 = discord.Embed(title = "popi" , description = f"{message.author.mention} is a poopie?oh no......")
                    await message.channel.send(content = None, embed = emb2)

            elif message.content.lower() == "$sexrating":   #returns random sex rating value b/w 1 and 5
                emb3 = discord.Embed(title = "Sexrating" , description = f"{random.randint(1,5)} {client.get_emoji(703648807271006379)}" )  #creating embded, lookin saxy
                await message.channel.send(content = None, embed =  emb3)

            elif message.content.lower() == "$help":  #help command
                emb4 = discord.Embed(title = "Help" , description = "List of commands")
                #adding fields to embed 
                emb4.add_field(name = "$popi", value = "popi", inline = False)
                emb4.add_field(name = "$members", value = "Returns number of members in server", inline = False)
                emb4.add_field(name = "$sexrating", value = f"Are you at your sexual peak today? {client.get_emoji(708951950162395166)}", inline = False)

                await message.channel.send(content = None, embed = emb4 )


            #ECONOMY CODE; ADD SPACE ABOVE THIS FOR OTHER UNRELATED FUNCTIONS PLEASE :linus_gun:

            elif message.content.lower() == "$bal":
                data_bal = db.economyvalues.find_one({"name":str(message.author)})
                emb5 = discord.Embed(title = str(message.author), description = f"Bank balance : {data_bal['bal']}")
                await message.channel.send(content = None, embed = emb5)
                
            elif message.content.lower() == "$work":   #just test commands, we can change the names later
                data_earn = db.economyvalues.find_one({"name":str(message.author)})
                curr_bal = data_earn["bal"]
                rand_val = random.randint(35,150)

                embed = discord.Embed(title = str(message.author), description = f"You earned {rand_val}", colour = discord.Colour.green())

                db.economyvalues.update_one({"name":str(message.author)} , {'$set':{"bal" : rand_val + curr_bal}})
                await message.channel.send(content = None, embed = embed)
            


client.run(token)


