import sys

import discord
from discord.ext import commands
from prisma.models import Guild

from internal.context import CrajyContext

from utils import embed as em
from internal import enumerations as enums


class Moderator(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: CrajyContext) -> bool:
        """Restricts commands to administrators only"""
        return ctx.author.guild_permissions.administrator  # type: ignore

    @commands.is_owner()
    @commands.command(name="remove-user", help="Remove a user from the bot database.")
    async def remove_user(self, ctx: CrajyContext, member: discord.Member) -> None:
        confirm_embed = em.CrajyEmbed(
            title="Deleting User Data",
            description=f"Are you sure you want to delete all of {member.display_name}'s data?",
            embed_type=enums.EmbedType.WARNING,
        )
        confirm_embed.set_thumbnail(url=em.EmbedResource.WARNING.value)
        confirm_embed.quick_set_author(self.bot.user)

        ask = await ctx.reply(embed=confirm_embed)
        response = await ctx.get_confirmation(ask)

        if response:
            await self.bot.delete_member(member)
            confirm_embed.description = f"Deleted data for user: {member.display_name}."
            confirm_embed.color = enums.EmbedType.SUCCESS.value
            await ask.edit(embed=confirm_embed)
            await ctx.check_mark()
        else:
            confirm_embed.description = "Did not delete data."
            confirm_embed.color = enums.EmbedType.FAIL.value
            await ask.edit(embed=confirm_embed)
            await ctx.x_mark()

    @commands.is_owner()
    @commands.command(name="reload-module", aliases=["reloadm"])
    async def reload_module(self, ctx: CrajyContext, module: str) -> None:
        removes = []
        for name in sys.modules:
            if name.startswith(module):
                removes.append(name)
        for name in removes:
            sys.modules.pop(name)
        await ctx.send(f"Reloaded {module}")

    @commands.guild_only()
    @commands.command(name="bot-channel", aliases=["setup"])
    async def setup_guild(
        self, ctx: CrajyContext, channel: discord.TextChannel
    ) -> None:
        """Set the channel to which CrajyBot should send announcements to."""
        if ctx.guild is None:  # this is caught by the deco, but done for type checking
            return

        await Guild.prisma().update(
            {"bot_channel": str(channel.id)}, {"id": str(ctx.guild.id)}
        )

        await ctx.reply("Announcement channel set ✅")
