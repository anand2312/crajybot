from typing import TYPE_CHECKING

import discord
from discord.ext import commands
import more_itertools as mitertools
from prisma.models import Tag

from internal import enumerations as enums
from internal.context import CrajyContext
from logic.tags import (
    create_tag,
    delete_tag,
    fetch_tag_for_guild,
    search_tags_for_guild,
)
from utils import embed as em

if TYPE_CHECKING:
    from internal.bot import CrajyBot
else:
    CrajyBot = "CrajyBot"


class Tags(commands.Cog):
    """tags have been made into their own cog (attempt) to reduce the noise in stupid.py"""

    def __init__(self, bot: CrajyBot) -> None:
        self.bot = bot

    @commands.group(aliases=["tag"], help="Tags.")
    @commands.guild_only()
    async def wat(self, ctx: CrajyContext) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(self.wat)

    @wat.command(name="add", aliases=["-a"])
    @commands.guild_only()
    async def add_to_wat(self, ctx: CrajyContext, key: str, *, output: str) -> None:
        assert ctx.guild
        await create_tag(ctx.author, ctx.guild, key, output)
        embed = em.CrajyEmbed(title="Added tag.", embed_type=enums.EmbedType.BOT)
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        await ctx.maybe_reply(embed=embed)

    @wat.command(name="remove", aliases=["-r"])
    @commands.guild_only()
    async def remove_from_wat(self, ctx: CrajyContext, key: str) -> None:
        confirm_embed = em.CrajyEmbed(
            title="Deleting Tags.", embed_type=enums.EmbedType.WARNING
        )
        confirm_embed.description = (
            f"Are you sure you want to delete tag named `{key}`?"
        )
        confirm_embed.quick_set_author(ctx.author)
        confirm_embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        ask = await ctx.maybe_reply(embed=confirm_embed)
        response = await ctx.get_confirmation(ask)

        if not response:
            # operation aborted; user responded with no
            embed = em.CrajyEmbed(
                title="Deleting Tags.", embed_type=enums.EmbedType.BOT
            )
            embed.description = f"Did not delete the tag."
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
            await ask.edit(embed=embed)
            return

        assert ctx.guild

        tag = await Tag.prisma().find_first(
            where={"tag_name": key, "guildId": str(ctx.guild.id)}
        )

        assert isinstance(ctx.author, discord.Member)

        if tag is None:
            await ctx.maybe_reply(f"Tag `{key}` not found")
            return

        if (
            ctx.author.guild_permissions.administrator
            or int(tag.userId) == ctx.author.id
        ):
            await delete_tag(tag.id)
            embed = em.CrajyEmbed(title="Tag Deleted.", embed_type=enums.EmbedType.BOT)
            embed.description = f"Tag named `{key}` has been removed from the database."
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        else:
            embed = em.CrajyEmbed(title="Tag Deleted.", embed_type=enums.EmbedType.FAIL)
            embed.description = f"You can only delete tags that you made."
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)

        await ask.edit(embed=embed)

    @wat.command(name="edit-output", aliases=["edit-out"])
    @commands.guild_only()
    async def edit_wat_output(
        self, ctx: CrajyContext, key: str, *, output: str
    ) -> None:
        assert ctx.guild

        tag = await fetch_tag_for_guild(key, ctx.guild.id)

        if tag is None:
            await ctx.maybe_reply(f"Tag with name `{key}` not found ❌")
            return

        embed = em.CrajyEmbed(
            title="Editing Tag content", embed_type=enums.EmbedType.BOT
        )
        embed.description = f"Edited `{key}` tag output."
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.TAG.value)

        assert isinstance(ctx.author, discord.Member)

        if (
            ctx.author.guild_permissions.administrator
            or int(tag.userId) == ctx.author.id
        ):
            await Tag.prisma().update({"content": output}, {"id": tag.id})
            await ctx.maybe_reply(embed=embed)
        else:
            await ctx.maybe_reply(f"You cannot edit this tag ❌")

    @wat.command(name="edit-key", aliases=["edit-name"])
    @commands.guild_only()
    async def edit_wat_key(self, ctx: CrajyContext, key: str, new_key: str) -> None:
        assert ctx.guild

        tag = await fetch_tag_for_guild(key, ctx.guild.id)
        if tag is None:
            await ctx.maybe_reply(f"Tag with name `{key}` not found ❌")
            return

        embed = em.CrajyEmbed(title="Editing Tag name", embed_type=enums.EmbedType.BOT)
        embed.description = f"Edited `{key}` tag output."
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.TAG.value)

        assert isinstance(ctx.author, discord.Member)

        if (
            ctx.author.guild_permissions.administrator
            or int(tag.userId) == ctx.author.id
        ):
            await Tag.prisma().update({"tag_name": new_key}, {"id": tag.id})
            await ctx.maybe_reply(embed=embed)
        else:
            await ctx.maybe_reply(f"You cannot edit this tag ❌")

    @wat.command(name="use", aliases=["-u"])
    @commands.guild_only()
    async def use(self, ctx: CrajyContext, *, key: str) -> None:
        assert ctx.guild
        tag = await fetch_tag_for_guild(key, ctx.guild.id)
        if tag is None:
            await ctx.send(f"Tag `{key}` not found")
            return
        await ctx.reply(tag.content)

    @wat.command(name="list", aliases=["-l"])
    @commands.guild_only()
    async def list_(self, ctx: CrajyContext) -> None:
        assert ctx.guild
        assert self.bot.user

        all_tags = await Tag.prisma().find_many(where={"guildId": str(ctx.guild.id)})
        chunked_tags = mitertools.chunked(all_tags, 6)
        embeds = []

        if len(all_tags) == 0:
            embed = em.CrajyEmbed(
                title=f"Tags for {ctx.guild.name}",
                description=f"No tags saved in this server.",
                embed_type=enums.EmbedType.FAIL,
            )
            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
            await ctx.maybe_reply(embed=embed)
            return

        for chunk in chunked_tags:
            page = em.CrajyEmbed(
                title="All Tags.",
                description="\n".join(i.tag_name for i in chunk),
                embed_type=enums.EmbedType.BOT,
            )
            page.set_thumbnail(url=em.EmbedResource.TAG.value)
            page.quick_set_author(ctx.author)
            embeds.append(page)
        pages = em.quick_embed_paginate(embeds)
        await pages.start(ctx)

    @wat.command(name="search", aliases=["-s"])
    async def wat_search(self, ctx: CrajyContext, key: str) -> None:
        assert ctx.guild
        assert self.bot.user

        matches = await search_tags_for_guild(key, ctx.guild.id)
        embeds = []

        if len(matches) == 0:
            embed = em.CrajyEmbed(
                title="Tag Search Results",
                description=f"No tags found matching {key}.",
                embed_type=enums.EmbedType.FAIL,
            )
            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
            await ctx.maybe_reply(embed=embed)
            return

        for chunk in mitertools.chunked(matches, 6):
            embed = em.CrajyEmbed(
                title="Tag Search Results",
                description="\n".join(f"• {i.tag_name}" for i in chunk),
                embed_type=enums.EmbedType.INFO,
            )
            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
            embeds.append(embed)

        pages = em.quick_embed_paginate(embeds)
        await pages.start(ctx)
