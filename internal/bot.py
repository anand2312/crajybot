import asyncio
from collections import defaultdict

from aiohttp import ClientSession
from aioscheduler import TimedScheduler
import asyncpg
from discord.ext import commands

from internal.help_class import HelpCommand
from internal.enumerations import EmbedType
from internal.context import CrajyContext
from secret.constants import *
from utils.embed import CrajyEmbed


class CrajyBot(commands.Bot):
    """Subclass of commands.Bot with some attributes set."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, help_command=HelpCommand(), case_insensitive=True, **kwargs)
        self.chat_money_cache = defaultdict(lambda: 0)
        self.db_pool = self.loop.run_until_complete(asyncpg.create_pool(DB_CONNECTION_STRING))
        self.__version__ = "3.0a"
        self.scheduler = TimedScheduler()    # task scheduler for reminders/notes 
        self.session = ClientSession()     # aiohttp clientsession for API interactions

    async def on_ready(self):
        self.scheduler.start()
        embed = CrajyEmbed(embed_type=EmbedType.BOT, description="Ready!")
        embed.quick_set_author(self.user)
        m = await self.get_channel(BOT_ANNOUNCE_CHANNEL).send(embed=embed)
        ctx = await self.get_context(m)
        await self.reschedule_tasks(ctx)

    async def on_member_join(self, member):
        """When a new member joins, add them to the database and greet them in DMs."""
        await self.register_new_member(member)
        embed = CrajyEmbed(embed_type=EmbedType.SUCCESS, title="Hi! Welcome to Crajy!")
        embed.quick_set_author(member)
        embed.quick_set_footer(self.user)
        await member.send(embed=embed)

    async def on_member_remove(self, member):
        """When a member leaves, quietly remove them from the database."""
        await self.delete_member(member)

    async def on_command_error(self, ctx, error):
        """Global error handler."""
        embed = CrajyEmbed(embed_type=EmbedType.FAIL, title="Command Errored.")
        embed.quick_set_footer(self.user)

        if isinstance(error, commands.CommandOnCooldown):
            embed.description = F"{ctx.author.display_name}, you have to wait {int(error.retry_after/60)} minutes before using this command again."
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            if ctx.message.content.startswith(".."):
                pass
            else:
                embed.description = f"Command {ctx.invoked_with} not found."
                return await ctx.send(embed=embed)
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

    async def get_context(self, message, *, cls=None):
        """Overriding get_context to use custom context."""
        return await super().get_context(message, cls=CrajyContext)

    async def reschedule_tasks(self, ctx):
        """Reschedule unfinished tasks that were stored in the database.
        Bot gets_context from the ready message it sends which can be used to get the guild object for get_member."""
        print("Loading unfinished tasks from database.")
        notes_cog = self.get_cog("Notes")
        #this query assumes that the only tasks are going to be reminders from the notes table. update as necessary.
        remaining_tasks = await self.db_pool.fetch("SELECT user_id, note_id, exec_time FROM notes NATURAL JOIN tasks")
        for record in remaining_tasks:
            author = ctx.guild.get_member(record["user_id"])
            self.scheduler.schedule(notes_cog.remind(author, record["note_id"]), record["exec_time"])
        print("Loaded unfinished tasks.")

    async def process_commands(self, message):
        """Triggers typing in channels before sending a message."""
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if ctx.valid and getattr(ctx.cog, "qualified_name", None) != "Jishaku":
            await ctx.trigger_typing()
        await self.invoke(ctx)

    async def register_new_member(self, member):
        async with self.db_pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("INSERT INTO economy VALUES($1)", member.id)
                await connection.execute("INSERT INTO user_details VALUES($1)", member.id)
                await connection.execute("INSERT INTO inventories VALUES($1)", member.id)
        
    async def delete_member(self, member):
        async with self.db_pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM economy WHERE user_id=$1", member.id)
    
