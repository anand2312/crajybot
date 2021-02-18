"""Commands to help organize Among Us games."""
import discord
from discord.ext import commands
import asyncio

from utils import embed as em
from internal import enumerations as enums


class AmongUs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status = False
        self.data = {"user": None, "code": None, "server": None}
        self.embed = None

    @commands.Cog.listener()
    async def on_message(self, message):
        """Checks through chat and displays the current game room code, and server.
        Responds whenever someone says 'code' or 'server' in chat."""
        if self.status is False or message.author == self.bot.user:
            return
        if "code" in message.content.lower() or "server" in message.content.lower():
            await message.channel.send(embed=self.embed)

    @commands.group(
        name="among_us",
        aliases=["amongus", "play", "among-us"],
        invoke_without_command=True,
        help="Command to save the room code and server when starting a new game.",
    )
    async def among_us(self, ctx):
        """Command to save the room code and server when starting a new game."""
        if self.status is True:
            return await ctx.reply(
                f"{ctx.author.mention}, {self.data['user'].name} has already started a game.\nCode: ``{self.data['code']}``\nServer: ``{self.data['server']}``"
            )
        # checks
        def code_check(m):
            return (
                m.author == ctx.author
                and len(m.content) == 6
                and all([i.isalpha() for i in m.content])
            )

        def server_check(m):
            return m.author == ctx.author and m.content.lower() in [
                "asia",
                "europe",
                "north america",
                "na",
            ]

        await ctx.send("Enter the room code")
        code = await self.bot.wait_for("message", check=code_check, timeout=25)
        await ctx.send("Enter server: (Europe, Asia, North America)")
        server = await self.bot.wait_for("message", check=server_check, timeout=25)

        # updating data
        self.status = True
        self.data["user"] = ctx.author
        self.data["code"] = code.content.upper()
        self.data["server"] = server.content.capitalize()

        self.embed = em.CrajyEmbed(
            title="Among Us time!",
            description=f"Code: {self.data['code']}\nServer: {self.data['server']}",
            embed_type=enums.EmbedType.INFO,
        )
        self.embed.quick_set_author(ctx.author)

        await ctx.send(embed=self.embed)

    @among_us.command(
        name="end",
        help="Command to end the game session, and have the bot stop responding to messages that contain 'code' or 'server'.",
    )
    async def end(self, ctx):
        """Command to end the game session, and have the bot stop responding to messages that contain 'code' or 'server'."""
        if self.status is False:
            raise Exception("What are you trying to end? No one is playing now.")

        if (
            ctx.author == self.data["user"]
            or ctx.author.guild_permissions.administrator
        ):
            self.status = False
            self.data = {"user": None, "code": None, "server": None}
            self.embed = None

            return await ctx.send("Game session ended ggwp")

    @among_us.command(
        name="update", help="Command to update the room code and/or server of the game."
    )
    async def update(self, ctx):
        """Command to update the room code and/or server of the game."""
        if self.status is False:
            raise Exception("What are you trying to update? No one is playing now.")

        # checks
        def code_check(m):
            return (
                m.author == ctx.author
                and len(m.content) == 6
                and all([i.isalpha() for i in m.content])
            )

        def server_check(m):
            return m.author == ctx.author and m.content.lower() in [
                "asia",
                "europe",
                "north america",
            ]

        if (
            ctx.author == self.data["user"]
            or ctx.author.guild_permissions.administrator
        ):
            await ctx.send("Enter the room code")
            code = await self.bot.wait_for("message", check=code_check, timeout=25)
            await ctx.send("Enter server: (Europe, Asia, North America)")
            server = await self.bot.wait_for("message", check=server_check, timeout=25)

            self.data["user"] = ctx.author
            self.data["code"] = code.content.upper()
            self.data["server"] = server.content.capitalize()

            self.embed = em.CrajyEmbed(
                title="Among Us time!",
                description=f"Code: {self.data['code']}\nServer: {self.data['server']}",
                embed_type=enums.EmbedType.SUCCESS,
            )
            self.embed.quick_set_author(ctx.author)

            await ctx.check_mark()
            return await ctx.send(embed=self.embed)
