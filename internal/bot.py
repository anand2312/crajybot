import asyncio
from collections import defaultdict
import dotenv
import logging
import typing
import os

from aiohttp import ClientSession
from aioscheduler import TimedScheduler
import asyncpg
import discord
from discord.ext import commands

from internal.help_class import HelpCommand
from internal.enumerations import EmbedType
from internal.context import CrajyContext
from utils.embed import CrajyEmbed


dotenv.load_dotenv(dotenv.find_dotenv())


class CrajyBot(commands.Bot):
    """Subclass of commands.Bot with some attributes set."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, help_command=HelpCommand(), case_insensitive=True, **kwargs
        )
        self.chat_money_cache = defaultdict(int)
        self.task_loops = dict()
        self.db_pool = self.loop.run_until_complete(
            asyncpg.create_pool(os.environ.get("DB_CONNECTION_STRING"))
        )
        self.__version__ = "4.0a"
        self.scheduler = TimedScheduler()  # task scheduler for reminders/notes
        self.session = ClientSession()  # aiohttp clientsession for API interactions

        self.logger = logging.getLogger("discord")
        self.logger.setLevel(logging.WARNING)
        handler = logging.FileHandler(
            filename="discord.log", encoding="utf-8", mode="w"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        self.logger.addHandler(handler)

        # run table creation
        self.loop.run_until_complete(self.initialize_db())

    async def on_ready(self) -> None:
        self.logger.info("Bot Online!")
        self.scheduler.start()
        embed = CrajyEmbed(embed_type=EmbedType.BOT, description="Ready!")
        embed.quick_set_author(self.user)
        m = await self.get_channel(int(os.environ.get("BOT_TEST_CHANNEL"))).send(
            embed=embed
        )
        ctx = await self.get_context(m)
        await self.reschedule_tasks(ctx)

    async def on_member_join(self, member: discord.Member) -> None:
        """When a new member joins, add them to the database and greet them in DMs."""
        await self.register_new_member(member)
        embed = CrajyEmbed(embed_type=EmbedType.SUCCESS, title="Hi! Welcome to Crajy!")
        embed.quick_set_author(member)
        embed.quick_set_footer(self.user)
        await member.send(embed=embed)

    async def on_member_remove(self, member: discord.Member) -> None:
        """When a member leaves, quietly remove them from the database."""
        await self.delete_member(member)

    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        """If a message is edited, reprocess it for commands."""
        if before.author.bot:
            return

        ctx = await self.get_context(after)
        await self.invoke(ctx)

    async def on_command_error(self, ctx: CrajyContext, error: Exception) -> typing.Optional[discord.Message]:
        """Global error handler."""
        embed = CrajyEmbed(embed_type=EmbedType.FAIL, title="Command Errored.")
        embed.quick_set_footer(self.user)

        if isinstance(error, commands.CommandOnCooldown):
            embed.description = f"{ctx.author.display_name}, you have to wait {int(error.retry_after/60)} minutes before using this command again."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            tag = await self.db_pool.fetchval(
                "SELECT content FROM tags WHERE tag_name=$1", ctx.invoked_with
            )
            if tag:
                return await ctx.reply(tag)
        elif isinstance(error, asyncio.TimeoutError):
            embed.description = f"You took too long to respond for: {ctx.invoked_with}"
            return await ctx.message.edit(embed=embed)
        elif isinstance(error, commands.UserInputError):
            embed.description = f"Improper argument passed."
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=embed)
        else:
            embed.title = "Unexpected error occurred."
            embed.description = str(error)
            await ctx.send(embed=embed)
            raise error

    async def get_context(self, message: discord.Message, *, cls=None):
        """Overriding get_context to use custom context."""
        return await super().get_context(message, cls=CrajyContext)

    async def reschedule_tasks(self, ctx: CrajyContext):
        """Reschedule unfinished tasks that were stored in the database.
        Bot gets_context from the ready message it sends which can be used to get the guild object for get_member."""
        self.logger.info("Loading unfinished tasks from database.")
        notes_cog = self.get_cog("Notes")
        # this query assumes that the only tasks are going to be reminders from the notes table. update as necessary.
        remaining_tasks = await self.db_pool.fetch(
            "SELECT user_id, note_id, exec_time FROM notes NATURAL JOIN tasks"
        )
        for record in remaining_tasks:
            author = ctx.guild.get_member(record["user_id"])
            self.scheduler.schedule(
                notes_cog.remind(author, record["note_id"]), record["exec_time"]
            )
        print("Loaded unfinished tasks.")

    async def process_commands(self, message: discord.Message) -> None:
        """Triggers typing in channels before sending a message."""
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if ctx.valid and getattr(ctx.cog, "qualified_name", None) != "Jishaku":
            await ctx.trigger_typing()
        await self.invoke(ctx)

    async def register_new_member(self, member: discord.Message) -> None:
        async with self.db_pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("INSERT INTO economy VALUES($1)", member.id)
                await connection.execute(
                    "INSERT INTO user_details VALUES($1)", member.id
                )
                await connection.execute(
                    "INSERT INTO inventories VALUES($1)", member.id
                )

    async def delete_member(self, member: discord.Message) -> None:
        async with self.db_pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    "DELETE FROM economy WHERE user_id=$1", member.id
                )

    async def initialize_db(self) -> None:
        with open("crajybot.sql") as f:
            queries = f.read().split(";")
        
        for query in queries:
            try:
                await self.db_pool.execute(query)
            except Exception as e:
                self.logger.warn(f"DB initialization: {str(e)}")
