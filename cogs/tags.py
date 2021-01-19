from discord.ext import commands
import more_itertools as mitertools

from utils import embed as em
from internal import enumerations as enums


class Tags(commands.Cog):
    """tags have been made into their own cog (attempt) to reduce the noise in stupid.py"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['tag'], help="Tags.")
    async def wat(self, ctx):
        pass

    @wat.command(name="add", aliases=["-a"])
    async def add_to_wat(self, ctx, key, *, output):
        await self.bot.db_pool.execute("INSERT INTO tags(tag_name, content, author) VALUES($1, $2. $3)", key, output, ctx.author.id)
        embed = em.CrajyEmbed(title="Added tag.", embed_type=enums.EmbedType.BOT)
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        await ctx.maybe_reply(embed=embed)

    @wat.command(name="remove", aliases=["-r"])
    async def remove_from_wat(self, ctx, key):
        confirm_embed = em.CrajyEmbed(title="Deleting Tags.", embed_type=enums.EmbedType.WARNING)
        confirm_embed.description = f"Are you sure you want to delete tag named `{key}`?"
        confirm_embed.quick_set_author(ctx.author)
        confirm_embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        ask = await ctx.maybe_reply(embed=confirm_embed)
        response = await ctx.get_confirmation(ask)

        if not response:
            # operation aborted; user responded with no
            embed = em.CrajyEmbed(title="Deleting Tags.", embed_type=enums.EmbedType.BOT)
            embed.description = f"Did not delete the tag."
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
            return await ask.edit(embed=embed)

        owner = await self.bot.db_pool.fetchval("SELECT author FROM tags WHERE tag_name=$1", key)

        if ctx.author.guild_permissions.administrator or owner == ctx.author.id:
            await self.bot.db_pool.execute("DELETE FROM tags WHERE tag_name=$1", key)
            embed = em.CrajyEmbed(title="Tag Deleted.", embed_type=enums.EmbedType.BOT)
            embed.description = f"Tag named `{key}` has been removed from the database."
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        else:
            embed = em.CrajyEmbed(title="Tag Deleted.", embed_type=enums.EmbedType.FAIL)
            embed.description = f"You can only delete tags that you made."
            embed.quick_set_author(ctx.author)
            embed.set_thumbnail(url=em.EmbedResource.TAG.value)

        return await ask.edit(embed=embed)

    @wat.command(name="edit-output", aliases=["edit-out"])
    async def edit_wat_output(self, ctx, key, *, output):
        embed = em.CrajyEmbed(title="Editing Tag: Content", embed_type=enums.EmbedType.BOT)
        embed.description = f"Edited `{key}` tag output."
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        await self.bot.db_pool.execute("UPDATE tags SET content=$1 WHERE tag_name=$2", output, key)
        await ctx.maybe_reply(embed=embed)

    @wat.command(name="edit-key", aliases=["edit-name"])
    async def edit_wat_key(self, ctx, key, new_key):
        embed = em.CrajyEmbed(title="Editing Tag: Name", embed_type=enums.EmbedType.BOT)
        embed.description = f"Edited `{key}` tag output."
        embed.quick_set_author(ctx.author)
        embed.set_thumbnail(url=em.EmbedResource.TAG.value)
        await self.bot.db_pool.execute("UPDATE tags SET tag_name=$1 WHERE tag_name=$2", new_key, key)
        await ctx.maybe_reply(embed=embed) 

    @wat.command(name="use", aliases=["-u"])
    async def use(self, ctx, *, key):
        content = await self.bot.db_pool.fetchval("SELECT content FROM tags WHERE tag_name=$1", key)
        await ctx.reply(content)

    @wat.command(name="list", aliases=["-l"])
    async def list_(self, ctx):
        all_tags = await self.bot.db_pool.fetch("SELECT tag_name FROM tags")
        chunked_tags = mitertools.chunked(all_tags, 6)
        embeds = []
        for chunk in chunked_tags:
            page = em.CrajyEmbed(title="All Tags.", description="\n".join(chunk), embed_type=enums.EmbedType.BOT)
            page.set_thumbnail(url=em.EmbedResource.TAG.value)
            page.quick_set_author(ctx.author)
            embeds.append(page)

        pages = em.quick_embed_paginate(embeds)
        await pages.start(ctx)

    @wat.command(name="search", aliases=["-s"])
    async def wat_search(self, ctx, key):
        matches = await self.bot.db_pool.fetch("SELECT tag_name FROM tags WHERE LOWER(tag_name) LIKE %$1%", key.lower())
        embeds = []

        if len(matches) == 0:
            embed = em.CrajyEmbed(title="Tag Search Results", description=f"No tags found matching {key}.", embed_type=enums.EmbedType.FAIL)
            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.TAG)
            return await ctx.maybe_reply(embed=embed)

        for chunk in mitertools.chunked(matches, 6):
            embed = em.CrajyEmbed(title="Tag Search Results", description="\n".join(f"• {i['tag_name']}" for i in chunk), embed_type=enums.EmbedType.INFO)
            embed.quick_set_author(self.bot.user)
            embed.set_thumbnail(url=em.EmbedResource.TAG)
            embeds.append(embed)
        
        pages = em.quick_embed_paginate(embeds)
        await pages.start(ctx)


def setup(bot):
    bot.add_cog(Tags(bot))