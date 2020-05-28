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

@bot.command(name='test')
async def test(ctx):
    response = discord.Embed(title='Name', description='Absolute MadLad')
    message = await ctx.message.channel.send(embed = response)
    print(type(message))

bot.run(token)