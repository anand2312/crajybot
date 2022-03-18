"""Some fun commands."""
from __future__ import annotations

import random
from typing import TYPE_CHECKING, Literal, Optional

import discord
from discord.ext import commands

from internal.context import CrajyContext
from internal import enumerations as enums
from utils import embed as em

if TYPE_CHECKING:
    from internal.bot import CrajyBot
else:
    CrajyBot = "CrajyBot"


class Stupid(commands.Cog):
    def __init__(self, bot: CrajyBot) -> None:
        self.bot = bot

    @commands.command(name="love-calc", aliases=["lc", "love", "lovecalc"])
    async def love_calc(
        self, ctx: CrajyContext, sname: str, fname: Optional[str] = None
    ) -> None:
        if fname is None:
            fname = ctx.author.display_name

        async with ctx.channel.typing():
            percent = random.randint(1, 100)
            if percent >= 50:
                embed = em.CrajyEmbed(
                    title="Love Calculator", embed_type=enums.EmbedType.SUCCESS
                )
                embed.quick_set_author(ctx.author)
                embed.set_thumbnail(url=em.EmbedResource.LOVE_CALC.value)
                embed.add_field(name="That poor person", value=sname, inline=False)
                embed.add_field(name="Percent", value=percent, inline=True)
            else:
                embed = em.CrajyEmbed(
                    title="Love Calculator", embed_type=enums.EmbedType.FAIL
                )
                embed.quick_set_author(ctx.author)
                embed.set_thumbnail(url=em.EmbedResource.LOVE_CALC.value)
                embed.add_field(name="That poor person", value=sname, inline=False)
                embed.add_field(name="Percent", value=percent, inline=True)
            sent_message = await ctx.maybe_reply(embed=embed)
            await ctx.check_mark(sent_message)

    @commands.command(name="weird", aliases=["w"])
    async def weird(self, ctx: CrajyContext, *, message: str) -> None:
        out = ""
        curr_func = "lower"
        for i in message:
            if curr_func == "lower":
                out += i.lower()
                curr_func = "upper"
            else:
                out += i.upper()
                curr_func = "lower"
        await ctx.maybe_reply(out)

    @commands.command(name="emojify")
    async def emojify(self, ctx: CrajyContext, *, message: str) -> None:
        emojis = {
            "a": "🇦",
            "b": "🇧",
            "c": "🇨",
            "d": "🇩",
            "e": "🇪",
            "f": "🇫",
            "g": "🇬",
            "h": "🇭",
            "i": "🇮",
            "j": "🇯",
            "k": "🇰",
            "l": "🇱",
            "m": "🇲",
            "n": "🇳",
            "o": "🇴",
            "p": "🇵",
            "q": "🇶",
            "r": "🇷",
            "s": "🇸",
            "t": "🇹",
            "u": "🇺",
            "v": "🇻",
            "w": "🇼",
            "x": "🇽",
            "y": "🇾",
            "z": "🇿",
        }
        out = ""
        for letter in message.lower():
            if letter.isalpha():
                out += f"{emojis[letter]} "
            else:
                out += letter
        await ctx.maybe_reply(out)

    @commands.command(name="owo", aliases=["uwu"])
    async def owo(self, ctx: CrajyContext, *, text: str) -> None:
        out = ""
        for i in text:
            case = "upper" if i.isupper() else "lower"
            if i.lower() in ["l", "r"]:
                out += "w" if case == "lower" else "W"
            else:
                out += i

        await ctx.maybe_reply(out)

    @commands.command(
        name="change-presence",
        aliases=["changepresence", "changestatus", "change-status"],
        help="Change the bot's status.",
    )
    @commands.cooldown(1, 600)
    async def change_presence(
        self,
        ctx: CrajyContext,
        activity: Literal["playing", "watching", "listening", "streaming"],
        *,
        status: str,
    ) -> None:
        if len(status) > 30 and activity != "streaming":
            raise ValueError(
                f"Inputted status ({len(status)}) longer than 30 characters."
            )

        discord_activity = discord.Activity(name=status)

        if activity.lower() == "playing":
            discord_activity.type = discord.ActivityType.playing
        elif activity.lower() == "listening":
            discord_activity.type = discord.ActivityType.listening
        elif activity.lower() == "watching":
            discord_activity.type = discord.ActivityType.watching
        elif activity.lower() == "streaming":
            name, url = status.split("|")
            discord_activity = discord.Streaming(name=name, url=url)

        await ctx.check_mark()
        return await self.bot.change_presence(
            status=discord.Status.online, activity=discord_activity
        )
