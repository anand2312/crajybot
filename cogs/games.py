import discord
from discord.ext import commands
from pymongo import MongoClient
import tictactoe
import random
from KEY import *
import asyncio
import datetime
from random_word import RandomWords
from PyDictionary import PyDictionary
from akinator.async_aki import Akinator


client = MongoClient("mongodb://localhost:27017/")
db = client["bot-data"]
games_leaderboard = db["games"]

d = PyDictionary()
r = RandomWords()

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tictactoe", 
                      aliases=["ttt"],
                      help="Play tictactoe with another person!",
                      brief="Play tictactoe with another person!",
                      usage="<person>")
    @commands.cooldown(1, 30, type=commands.BucketType.channel)
    async def ttt(self, ctx, opponent: discord.Member = None):
        if opponent == ctx.message.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("you moron, trying to play with yourself.")

        board = tictactoe.initial_state()
        player = random.choice([tictactoe.X, tictactoe.O])
        next_player = tictactoe.X if player == tictactoe.O else tictactoe.O
        players = {tuple(tictactoe.X): ctx.author, tuple(tictactoe.O): opponent} #check cause of error because tuple() is unnecesary

        main_message_embed = discord.Embed(title="TicTacToe Game!",
                                            description=f"{ctx.author.mention} has challenged {opponent.mention}!\n {players[tuple(player)]} makes the first move.",
                                            timestamp=datetime.datetime.utcnow())
        main_message_embed.set_thumbnail(url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
        main_message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        main_message_embed.set_footer(text=opponent.display_name, icon_url=opponent.avatar_url)
        main_message_embed.color = discord.Color.blue()
        main_message = await ctx.send(embed=main_message_embed)
        main_message_embed.set_thumbnail(url=discord.Embed.Empty)

        top_row_message = await ctx.send("*top row*")
        for i in ["↖", "⬆", "↗"]:
            await top_row_message.add_reaction(i)

        middle_row_message = await ctx.send(content="*middle row*")
        for i in ["⬅", "⏺", "➡"]:
            await middle_row_message.add_reaction(i)

        bottom_row_message = await ctx.send(content="*bottom row*")
        for i in["↙", "⬇", "↘"]:
            await bottom_row_message.add_reaction(i)

        def player_check(reaction, user):
            if str(reaction.emoji) in ["↖", "⬆", "↗", "⬅", "⏺", "➡", "↙", "⬇", "↘"] and user == players[player]:
                return True

            return False

        while not tictactoe.terminal(board):
            reaction, _ = await self.bot.wait_for("reaction_add", check=player_check, timeout=180)
            message_of_reaction = reaction.message

            if reaction:
                main_message_embed.color = discord.Color.red()
                await message_of_reaction.clear_reaction(reaction.emoji)
                main_message_embed = tictactoe.update_board(main_message_embed, reaction.emoji, player)
                player, next_player = next_player, player
                main_message_embed.description += f"\n{players[player]}'s turn"  # maybe move to better place
                await main_message.edit(embed=main_message_embed)

        main_message_embed.description = f"{players[next_player]} destroyed {players[player]}!\n Good Game!"
        main_message_embed.color = discord.Color.green()
        await main_message.edit(embed=main_message_embed)
        tictactoe.reset_board()

    @ttt.error
    async def ttt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message_embed = discord.Embed(title="TicTacToe Game!",
                                          description="There's an on going game, please wait for it to get over!",
                                          timestamp=datetime.datetime.utcnow())
            message_embed.set_thumbnail(
                url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
            message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            message_embed.color = discord.Color.red()
            return await ctx.send(embed=message_embed)

        elif isinstance(getattr(error, 'original'), asyncio.TimeoutError):
            message_embed = discord.Embed(title="TicTacToe Game!",
                                          description="The player did not play a move in time, the match is ended.",
                                          timestamp=datetime.datetime.utcnow())
            message_embed.set_thumbnail(
                url=r"https://media.discordapp.net/attachments/749227065512820736/755093446263439540/download.png")
            message_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            message_embed.color = discord.Color.red()
            ctx.command.reset_cooldown(ctx)
            tictactoe.reset_board()
            return await ctx.send(embed=message_embed)

    @commands.command(name="guess")
    async def guess(self, ctx):
        await ctx.send(f"{ctx.author.mention}, check your DMs!")
        #wait_for checks
        def reply_check(m):
            if m.author == ctx.message.author and m.guild is None:
                return True

        def answer_check(m):
            nonlocal answer
            if m.author != ctx.message.author and m.content.lower() == answer_val.lower():
                return True

        await ctx.author.send("Send the word that everyone has to guess! Send 'plshelp' if you don't have a word.")
        try:
            answer = await self.bot.wait_for('message', check=reply_check, timeout=30)
            if answer.content == 'plshelp':
                await ctx.author.send("Note: the auto word picking thing may not always work (no word might be sent to the channel, incorrect meaning) etc so, dont blame me too much :(")
                try:
                    async with ctx.author.dm_channel.typing():
                        answer_val = r.get_random_word(hasDictionaryDef="true", maxLength=6)
                        clue_dict = d.meaning(answer_val)
                        answer_val = answer_val.lower()
                    clue_val = list(clue_dict.values())
                    await ctx.author.dm_channel.send(f"Chosen a word! The word is **{answer_val}**")
                except:
                    await ctx.author.send("whoops something fucked up. Starting the command again 😔....")
                    return await self.guess(ctx)
                await ctx.send(f"{ctx.author.mention} has chosen a word! Everyone has 1 minute to guess it.")
                await ctx.send(f"Clue - **{clue_val}**")
                try:
                    reply = await self.bot.wait_for('message', check=answer_check, timeout=60)
                except asyncio.TimeoutError:
                    return await ctx.send(f"Time up! No one guessed the word. The word was **{answer_val}**")
        
                games_leaderboard.update_one({"user":str(reply.author)}, {"$inc":{"wins":1}}, upsert=True)
                return await ctx.send(f"{reply.author.mention} got it right! The word was **{reply.content}**")

            else:
                await ctx.author.send("Send a clue for your word!")
                clue = await self.bot.wait_for('message', check=reply_check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.author.send("Time up!")
        
        await ctx.send(f"{ctx.author.mention} has chosen a word! Everyone has 1 minute to guess it.")
        answer_val = answer.content
        clue_val = clue.content
        await ctx.send(f"Clue - **{clue_val}**")

        try:
            reply = await self.bot.wait_for('message', check=answer_check, timeout=60)
        except asyncio.TimeoutError:
            return await ctx.send(f"Time up! No one guessed the word. The word was **{answer_val}**")
        
        games_leaderboard.update_one({"user":str(reply.author)}, {"$inc":{"wins":1}}, upsert=True)
        return await ctx.send(f"{reply.author.mention} got it right! The word was **{reply.content}**")


    @commands.command(name="akinator", aliases=["aki"])
    async def akinator_game(self, ctx):
        
        aki = Akinator()
        first = await ctx.send("Processing... \n**This command is in beta, don't complain.**")
        q = await aki.start_game()

        game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q, url=r"https://en.akinator.com/", color=discord.Color.blurple())
        game_embed.set_footer(text=f"You have 10 seconds to add a reaction")

        option_map = {'✅': 'y', '❌':'n', '🤷‍♂️':'p', '😕':'pn', '⁉️': 'i'}
        count = 0

        def option_check(reaction, user):
                return user==ctx.author and reaction.emoji in ['◀️', '✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔']

        while aki.progression <= 80:
            if count == 0:
                await first.delete()
                game_message = await ctx.send(embed=game_embed)
                count += 1
            else:
                await game_message.delete()
                game_message = await ctx.send(content=None, embed=game_embed)

            for emoji in ['◀️', '✅', '❌', '🤷‍♂️', '😕', '⁉️', '😔']:
                await game_message.add_reaction(emoji)

            option, _ = await self.bot.wait_for('reaction_add', check=option_check) 
            if option.emoji == '😔':
                return await ctx.send("Game ended.")
            async with ctx.channel.typing():
                if option.emoji == '◀️':   #to go back to previous question
                    try:
                        q = await aki.back()
                    except:   #excepting trying to go beyond 1 first question
                        pass
                    #editing embed for next question
                    game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q, url=r"https://en.akinator.com/", color=discord.Color.blurple())
                    continue
                else:
                    q = await aki.answer(option_map[option.emoji])
                    #editing embed for next question
                    game_embed = discord.Embed(title=f"{str(ctx.author.nick)}'s game of Akinator", description=q, url=r"https://en.akinator.com/", color=discord.Color.blurple())
                    continue
        
        await aki.win()

        result_embed = discord.Embed(title="My guess....", colour=discord.Color.dark_blue())
        result_embed.add_field(name=f"My first guess is **{aki.first_guess['name']}**", value=aki.first_guess['description'], inline=False)
        result_embed.set_footer(text="Was I right? Add the reaction accordingly.")
        result_embed.set_image(url=aki.first_guess['absolute_picture_path'])
        result_message = await ctx.send(embed=result_embed)
        for emoji in ['✅', '❌']:
            await result_message.add_reaction(emoji)

        option, _ = await self.bot.wait_for('reaction_add', check=option_check, timeout=10)
        if option.emoji ==  '✅':
            final_embed = discord.Embed(title="I'm a fuckin genius", color=discord.Color.green())
        elif option.emoji == '❌':
            final_embed = discord.Embed(title="Oof", description="Maybe try again?", color=discord.Color.red())
        
        return await ctx.send(content=None, embed=final_embed)


    @commands.command(name="games-leaderboard", aliases=["g-lb", "glb", "g-top", "gtop", "games-top"])
    async def games_top(self, ctx):
        out = ""
        for i, j in enumerate(games_leaderboard.find({"$query":{}, "$orderby":{"wins":-1}})):
            out += f"{i+1}. {j['user']}  **{j['wins']}** wins\n"
        await ctx.send(out)
    

def setup(bot):
    bot.add_cog(Games(bot))