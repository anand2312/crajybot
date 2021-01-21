"""Some commands to store user notes."""
from typing import Optional
from datetime import datetime

import discord
from discord.ext import commands, menus

from utils.converters import CustomTimeConverter
from internal.enumerations import EmbedType
from utils import embed as em


class Notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def remind(self, user: discord.Member, about: int) -> None:
        """Function that will remind the user about the note with ID `about`."""
        data = await self.bot.db_pool.fetchval("DELETE FROM notes WHERE note_id = $1 RETURNING raw_note", about)
        embed = em.CrajyEmbed(title=f"You reminder is here.", embed_type=EmbedType.INFO)
        embed.description = data
        embed.quick_set_author(user)
        embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
        return await user.send(embed=embed)

    @commands.group(name="Note making command.")
    async def notes(self, ctx):
        await ctx.send_help(notes)

    @notes.command(name="create",
                   aliases=["-c"],
                   help="Saves a note. Notes are personal; only you can retrieve your notes. You can invoke these commands in"
                        "DMs with the bot as well."
                        "You can also specify a `time`, after which the bot should remind you about a note.")
    async def notes_create(self, ctx, time: Optional[CustomTimeConverter], *, content):
        note_id = await self.bot.db_pool.fetchval("INSERT INTO notes(user_id, raw_note) VALUES($1, $2) RETURNING note_id", ctx.author.id, content)
        embed = em.CrajyEmbed(title=f"Note Creation: ID {note_id}", embed_type=EmbedType.SUCCESS)
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.NOTES.value)

        if time is None:
            # don't schedule
            embed.description = f"Added to your notes! Use `.notes return` to get all your stored notes."
        else:
            now = datetime.utcnow()
            self.bot.scheduler.schedule(self.remind(ctx.author, note_id), now + time)
            embed.description =  f"You will be reminded about this in {time}. Use `.notes return` to get all your stored notes."

        await ctx.maybe_reply(embed=embed)

    @notes.command(name="return", 
                   aliases=["-r"],
                   help="DMs you all the notes that you have saved, or the specific note that you asked for. ")
    async def notes_return(self, ctx, note_id: commands.Greedy[int] = None):
        if note_id is None:
            data = await self.bot.db_pool.fetch("SELECT note_id, raw_note FROM notes WHERE user_id=$1", ctx.author.id)
        else:
            data = await self.bot.db_pool.fetch("SELECT note_id, raw_note FROM notes WHERE user_id=$1 AND note_id=ANY($2::INT[])", ctx.author.id, note_id)
        if not data:     # if no records
            embed = em.CrajyEmbed(title="Fetched Notes", embed_type=EmbedType.WARNING)
            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
            embed.description = "You have no notes stored. Add a note with `.notes create`."
            await ctx.check_mark()
            return await ctx.author.send(embed=embed)
        
        embeds = []
        for row in data:
            e = em.CrajyEmbed(title=f"Note: ID {row['note_id']}", embed_type=EmbedType.SUCCESS)
            e.description = row['raw_note']
            e.quick_set_author(ctx.author)
            e.set_thumbnail(url=em.EmbedResource.NOTES.value)
            embeds.append(e)

        pages = em.quick_embed_paginate(embeds)
        author_dm_channel = await ctx.author.create_dm()
        await ctx.check_mark()
        await pages.start(ctx, channel=author_dm_channel)

    @notes.command(name="pop",
                   aliases=["-p"],
                   help="Deletes notes from the database; deletes all notes or the specific note you asked for.")
    async def notes_pop(self, ctx, note_id: commands.Greedy[int] = None):
        confirm_embed = em.CrajyEmbed(title="Clearing all notes", embed_type=EmbedType.WARNING)
        confirm_embed.description = "Are you sure you want to clear your notes?"
        confirm_embed.quick_set_author(ctx.author)
        confirm_embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
        ask = await ctx.maybe_reply(embed=confirm_embed, mention_author=True)

        decision = await ctx.get_confirmation(ask)

        if decision:
            if note_id is None:
                await self.bot.db_pool.execute("DELETE FROM notes WHERE user_id=$1", ctx.author.id)
            else:
                await self.bot.db_pool.execute("DELETE FROM notes WHERE user_id=$1 AND note_id=ANY($2::INT[])", ctx.author.id, note_id)
            out = em.CrajyEmbed(title="Deleted Notes", embed_type=EmbedType.SUCCESS)
            out.description = "Deleted notes."
        else:
            out = em.CrajyEmbed(title="Operation aborted", embed_type=EmbedType.FAIL)
            out.description = "All your notes are safe."

        out.quick_set_author(ctx.author)
        out.set_thumbnail(url=em.EmbedResource.NOTES.value)
        return await ask.edit(embed=out)

    @commands.command(name="remind", aliases=["reminder", "remindme"],
                      help="Alias for `.notes create`, but the `time` argument is compulsory now.")
    async def create_reminder(self, ctx, time, *, content):
        return await self.notes_create(ctx, time, content=content)

def setup(bot):
    bot.add_cog(Notes(bot))
