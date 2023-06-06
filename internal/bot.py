from __future__ import annotations

import asyncio
import traceback
import typing
from io import StringIO

import discord
from aiohttp import ClientSession
from aioscheduler import TimedScheduler
from discord.ext import commands, tasks
from loguru import logger
from prisma import Prisma, register
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
    vars: dict[str, object]
    task_loops: dict[str, tasks.Loop]

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(
            *args,
            application_id=709407268487037019,
            help_command=HelpCommand(),
            case_insensitive=True,
            **kwargs,
        )
        self.__version__ = "5.0"

        self.db = Prisma()
        self.task_loops = dict()
        self.scheduler = TimedScheduler()  # task scheduler for reminders/notes
        self.vars = {}  # set all other misc bot vars here

    async def setup_hook(self) -> None:
        # Initialize all connections here
        logger.info("Running setup hook")
        await self.db.connect()
        register(self.db)

        logger.info("Connected to database")
        self.session = ClientSession()

        for name, loop in self.task_loops.items():
            loop.start()
            logger.info(f"Started task loop: {name}")

        self.scheduler.start()

    async def on_ready(self) -> None:
        logger.info("Bot Online!")

        if self.user is None:
            logger.warning("on-ready terminated early as self.user was None")
            return

        embed = CrajyEmbed(embed_type=EmbedType.BOT, description="Ready!")
        embed.quick_set_author(self.user)

        channel = self.get_channel(BOT_TEST_CHANNEL)

        if channel is None:
            logger.warning("Bot test channel not found")
            return

        await channel.send(embed=embed)

    async def on_member_join(self, member: discord.Member) -> None:
        """When a new member joins, add them to the database."""
        if member.bot:
            return
        logger.info(f"{member.id} joined {member.guild.id}, adding to database")
        await User.prisma().create(
            {"id": str(member.id), "Guild": {"connect": {"id": str(member.guild.id)}}}
        )

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Register a guild to the database."""
        logger.info(f"Joined {guild.id=}")
        await Guild.prisma().create(
            {
                "id": str(guild.id),
            }
        )
        for member in guild.members:
            if member.bot:
                continue
            # you might be thinking why i'm doing a query in a loop here
            # "are you stupid? that's n queries that could be done in 1!"
            # prisma client py doesn't support create_many with SQLite
            # and i don't want to set up postgres

            # this query creates a new row in the users table if it doesn't already exists
            # after that, it links that row to the guild
            # otherwise, it updates the existing member, linking it with the guild
            await User.prisma().upsert(
                where={"id": str(member.id)},
                data={
                    "update": {"Guild": {"connect": [{"id": str(guild.id)}]}},
                    "create": {
                        "id": str(member.id),
                        "Guild": {"connect": [{"id": str(guild.id)}]},
                    },
                },
            )
        logger.success(f"Finished adding data for guild {guild.id}")

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """Remove the guild from the database"""
        logger.info(f"Removed from {guild.id=}")
        await Guild.prisma().delete(where={"id": str(guild.id)})

    async def on_member_remove(self, member: discord.Member) -> None:
        """When a member leaves, quietly remove them from the database."""
        logger.info(f"Removing {member.id=} from database")
        await User.prisma().update(
            data={"Guild": {"disconnect": [{"id": str(member.guild.id)}]}},
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
            logger.error(buffer.getvalue())
            raise error

    async def get_context(
        self, message: discord.Message, *, cls: typing.Type[ContextT] = CrajyContext
    ) -> ContextT:
        """Overriding get_context to use custom context."""
        return await super().get_context(message, cls=cls)  # type: ignore

    async def load_extension(
        self, name: str, *, package: typing.Optional[str] = None
    ) -> None:
        logger.info(f"Loading extesion: {name}")
        return await super().load_extension(name, package=package)

    async def unload_extension(
        self, name: str, *, package: typing.Optional[str] = None
    ) -> None:
        logger.info(f"Unloading extesion: {name}")
        return await super().unload_extension(name, package=package)

    async def reload_extension(
        self, name: str, *, package: typing.Optional[str] = None
    ) -> None:
        logger.info(f"Reloading extesion: {name}")
        return await super().reload_extension(name, package=package)
