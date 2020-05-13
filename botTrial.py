"""
Horoscopebot
insert further documentation here, insert documentation near new functions or variables you make as well.

"""
import os
import discord
import random

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
    channels = ["botspam","bot-test","botspam-v2"]  #limiting bot usage to these channels

    '''if "popi" in message.content.lower():
        await message.channel.send("poopi do be lookin poopie")'''

    if message.content[0] == "$":
        if str(message.channel) in channels:
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
                emb4.add_field(name = "$popi", value = "popi")
                emb4.add_field(name = "$members", value = "Returns number of members in server")
                emb4.add_field(name = "$sexrating", value = f"Are you at your sexual peak today? {client.get_emoji(708951950162395166)}")
                
                await message.channel.send(content = None, embed = emb4 )
            

'''@client.event    #testing if it detects updates to nicknames, it does
async def on_member_update(before,after):
    n = after.nick
    if n:
        last = before.nick
        if last:
            await after.edit(nick = "popi")
        else:
            await after.edit(nick = "popi")'''
    

client.run(token)


