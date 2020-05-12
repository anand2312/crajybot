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
                await message.channel.send(f"""Number of members = {guild_id.member_count}""")

            elif message.content.lower() == "$popi":   #popi
                n = random.randint(1,2)
                if n == 1:
                    await message.channel.send(f"poopi really do be poopie though")
                elif n == 2:
                    await message.channel.send(f"{message.author.mention} is a poopie?oh no......")

            elif message.content.lower() == "$sexrating":   #returns random sex rating value b/w 1 and 5
                await message.channel.send(f"{random.randint(1,5)} {client.get_emoji(703648807271006379)}")

    

client.run(token)


