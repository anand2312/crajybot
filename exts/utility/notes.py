"""Some commands to store user notes."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import cast, TYPE_CHECKING

import discord
from discord.ext import commands
import more_itertools as mitertools

from internal.context import CrajyContext
from internal.enumerations import EmbedType
from logic.notes import (
    create_note,
    delete_note,
    delete_notes,
    fetch_notes,
    fetch_reminders,
)
from utils.converters import CustomTimeConverter
from utils import embed as em

if TYPE_CHECKING:
    from internal.bot import CrajyBot
else:
    CrajyBot = "CrajyBot"


class Notes(commands.Cog):
    def __init__(self, bot: CrajyBot) -> None:
        self.bot = bot

    async def remind(self, user: discord.Member | discord.User, about: int) -> None:
        """Function that will remind the user about the note with ID `about`."""
        note = await delete_note(about)
        embed = em.CrajyEmbed(title=f"You reminder is here.", embed_type=EmbedType.INFO)
        embed.description = note.raw_note
        embed.quick_set_author(user)
        embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
        await user.send(embed=embed)

    @commands.group(help="Note making commands.")
    async def notes(self, ctx: CrajyContext) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help("notes")

    @notes.command(
        name="create",
        aliases=["-c"],
        help="Saves a note. Notes are personal; only you can retrieve your notes. You can invoke these commands in"
        "DMs with the bot as well."
        "You can also specify a `time`, after which the bot should remind you about a note.",
    )
    async def notes_create(
        self,
        ctx: CrajyContext,
        time: commands.Greedy[CustomTimeConverter],
        *,
        content: str,
    ):
        is_reminder = False if time == [] else True
        td = cast(timedelta, time)
        if is_reminder:
            now = datetime.utcnow()
            exec_time = now + td
        else:
            exec_time = None

        note = await create_note(ctx.author, content, exec_time, is_reminder)
        embed = em.CrajyEmbed(
            title=f"Note Creation: ID {note.id}", embed_type=EmbedType.SUCCESS
        )
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.NOTES.value)

        if time == []:
            # don't schedule
            embed.description = f"Added to your notes! Use `.notes return` to get all your stored notes."
        else:
            now = datetime.utcnow()
            self.bot.scheduler.schedule(self.remind(ctx.author, note.id), now + td)
            embed.description = f"You will be reminded about this in {td}. Use `.notes return` to get all your stored notes."

        await ctx.maybe_reply(embed=embed)

    @notes.command(
        name="return",
        aliases=["-r"],
        help="DMs you all the notes that you have saved, or the specific note that you asked for. ",
    )
    async def notes_return(
        self, ctx: CrajyContext, note_id: commands.Greedy[int] = None  # type: ignore
    ) -> None:
        if note_id is None:
            notes = await fetch_notes(ctx.author)
        else:
            ids = cast(list[int], note_id)
            notes = await fetch_notes(ctx.author, *ids)
        if len(notes) == 0:
            embed = em.CrajyEmbed(title="Fetched Notes", embed_type=EmbedType.WARNING)

            assert self.bot.user

            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
            embed.description = (
                "You have no notes stored. Add a note with `.notes create`."
            )
            await ctx.check_mark()
            await ctx.author.send(embed=embed)

        embeds = []
        for row in notes:
            e = em.CrajyEmbed(title=f"Note: ID {row.id}", embed_type=EmbedType.SUCCESS)
            e.description = row.raw_note
            e.quick_set_author(ctx.author)
            e.set_thumbnail(url=em.EmbedResource.NOTES.value)
            embeds.append(e)

        pages = em.quick_embed_paginate(embeds)
        author_dm_channel = await ctx.author.create_dm()
        await ctx.check_mark()
        await pages.start(ctx, channel=author_dm_channel)

    @notes.command(
        name="pop",
        aliases=["-p"],
        help="Deletes notes from the database; deletes all notes or the specific note you asked for.",
    )
    async def notes_pop(self, ctx, note_id: commands.Greedy[int] = None) -> None:  # type: ignore
        ids = cast(list[int], note_id)
        quantifier = "all" if note_id is None else len(ids)
        plural = quantifier == "all" or len(ids) > 1
        confirm_embed = em.CrajyEmbed(
            title=f"Clearing {quantifier} note{'s' if plural else ''}",
            embed_type=EmbedType.WARNING,
        )
        confirm_embed.description = (
            f"Are you sure you want to clear your note{'s' if plural else ''}?"
        )
        confirm_embed.quick_set_author(ctx.author)
        confirm_embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
        ask = await ctx.maybe_reply(embed=confirm_embed, mention_author=True)

        decision = await ctx.get_confirmation(ask)

        if decision:
            if note_id is None:
                await delete_notes(ctx.author)
            else:
                await delete_notes(ctx.author, *ids)
            out = em.CrajyEmbed(title="Deleted Notes", embed_type=EmbedType.SUCCESS)
            out.description = "Deleted notes."
        else:
            out = em.CrajyEmbed(title="Operation aborted", embed_type=EmbedType.FAIL)
            out.description = "All your notes are safe."

        out.quick_set_author(ctx.author)
        out.set_thumbnail(url=em.EmbedResource.NOTES.value)
        return await ask.edit(embed=out)

    @commands.group(
        name="remind",
        aliases=["reminder", "remindme"],
        invoke_without_command=True,
        help="Alias for `.notes create`, but the `time` argument is compulsory now.",
    )
    async def create_reminder(
        self, ctx: CrajyContext, time: CustomTimeConverter, *, content: str
    ) -> None:
        return await self.notes_create(ctx, time, content=content)  # type: ignore

    @create_reminder.command(
        name="list", help="Returns a list of all reminders you have."
    )
    async def reminder_list(self, ctx: CrajyContext) -> None:
        data = await fetch_reminders(ctx.author)
        chunked = mitertools.chunked(data, 4)
        embeds = []
        for chunk in chunked:
            embed = em.CrajyEmbed(title="Reminders", embed_type=EmbedType.INFO)
            out_as_list = [
                f"__**Note ID:{i.id}**__\n{i.raw_note[:30]}..." for i in chunk
            ]
            embed.description = "\n".join(out_as_list)
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
            embeds.append(embed)
        pages = em.quick_embed_paginate(embeds)
        return await pages.start(ctx)
