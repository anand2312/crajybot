from __future__ import annotations

import asyncio
import logging
import traceback
import typing
from io import StringIO

import discord
from aiohttp import ClientSession
from aioscheduler import TimedScheduler
from discord.ext import commands, tasks
from prisma import Prisma
from prisma.models import User, Guild, Tag

from internal.help_class import HelpCommand
from internal.enumerations import EmbedType
from internal.context import CrajyContext
from secret.constants import BOT_TEST_CHANNEL
from utils.embed import CrajyEmbed


ContextT = typing.TypeVar("ContextT", bound=commands.Context)


class CrajyBot(commands.Bot):
    """Subclass of commands.Bot with some attributes set."""

    __version__: str
    db: Prisma
    session: ClientSession
    scheduler: TimedScheduler
    logger: logging.Logger
    vars: dict[str, object]
    task_loops: dict[str, tasks.Loop]

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(
            *args, help_command=HelpCommand(), case_insensitive=True, **kwargs
        )
        self.__version__ = "5.0a"

        self.db = Prisma()
        self.task_loops = dict()
        self.scheduler = TimedScheduler()  # task scheduler for reminders/notes
        self.vars = {}  # set all other misc bot vars here
        self.logger = logging.getLogger(__name__)

    async def setup_hook(self) -> None:
        # Initialize all connections here
        self.logger.info("Running setup hook")
        await self.db.connect()
        self.logger.info("Connected to database")
        self.session = ClientSession()

        for name, loop in self.task_loops.items():
            loop.start()
            self.logger.info(f"Started task loop: {name}")

        self.scheduler.start()

    async def on_ready(self) -> None:
        self.logger.info("Bot Online!")

        if self.user is None:
            self.logger.warning("on-ready terminated early as self.user was None")
            return

        embed = CrajyEmbed(embed_type=EmbedType.BOT, description="Ready!")
        embed.quick_set_author(self.user)

        channel = typing.cast(discord.TextChannel, self.get_channel(BOT_TEST_CHANNEL))

        if channel is None:
            self.logger.warning("Bot test channel not found")
            return

        m = await channel.send(embed=embed)

    async def on_member_join(self, member: discord.Member) -> None:
        """When a new member joins, add them to the database."""
        await User.prisma().create(
            {"id": str(member.id), "guilds": {"connect": {"id": str(member.guild.id)}}}
        )

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Register a guild to the database."""
        await Guild.prisma().create({"id": str(guild.id)})

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """Remove the guild from the database"""
        await Guild.prisma().delete(where={"id": str(guild.id)})

    async def on_member_remove(self, member: discord.Member) -> None:
        """When a member leaves, quietly remove them from the database."""
        await User.prisma().update(
            data={"guilds": {"disconnect": [{"id": str(member.guild.id)}]}},
            where={"id": str(member.id)},
        )

    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        """If a message is edited, reprocess it for commands."""
        if before.author.bot:
            return

        ctx = await self.get_context(after)
        await self.invoke(ctx)

    async def on_command_error(
        self, ctx: CrajyContext, error: Exception
    ) -> typing.Optional[discord.Message]:
        """Global error handler."""
        embed = CrajyEmbed(embed_type=EmbedType.FAIL, title="Command Errored.")
        embed.quick_set_footer(embed_type=EmbedType.FAIL)

        if isinstance(error, commands.CommandOnCooldown):
            wait = int(error.retry_after / 60)
            embed.description = f"{ctx.author.display_name}, you have to wait {wait} minutes before using this command again."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            if ctx.invoked_with is None:
                return

            tag = await Tag.prisma().find_first(
                where={"tag_name": {"equals": ctx.invoked_with}}
            )

            if tag:
                return await ctx.reply(tag.content)
        elif isinstance(error, asyncio.TimeoutError):
            embed.description = f"You took too long to respond for: {ctx.invoked_with}"
            return await ctx.message.edit(embed=embed)
        elif isinstance(error, commands.UserInputError):
            embed.description = f"Improper argument passed."
            if ctx.command is None:
                return
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=embed)
        else:
            buffer = StringIO()
            traceback.print_exception(
                type(error), error, error.__traceback__, file=buffer
            )
            buffer.seek(0)
            await ctx.send(
                "whoops", file=discord.File(buffer, "traceback.txt")  # type: ignore
            )
            self.logger.error(buffer.getvalue())
            raise error

    async def get_context(
        self, message: discord.Message, *, cls: typing.Type[ContextT] = CrajyContext
    ) -> ContextT:
        """Overriding get_context to use custom context."""
        return await super().get_context(message, cls=cls)  # type: ignore

    async def process_commands(self, message: discord.Message) -> None:
        """Triggers typing in channels before sending a message."""
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if ctx.valid and getattr(ctx.cog, "qualified_name", None) != "Jishaku":
            await ctx.trigger_typing()
        await self.invoke(ctx)

    async def load_extension(
        self, name: str, *, package: typing.Optional[str] = None
    ) -> None:
        self.logger.info(f"Loading extesion: {name}")
        return await super().load_extension(name, package=package)

    async def unload_extension(
        self, name: str, *, package: typing.Optional[str] = None
    ) -> None:
        self.logger.info(f"Unloading extesion: {name}")
        return await super().unload_extension(name, package=package)

    async def reload_extension(
        self, name: str, *, package: typing.Optional[str] = None
    ) -> None:
        self.logger.info(f"Reloading extesion: {name}")
        return await super().reload_extension(name, package=package)
