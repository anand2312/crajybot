# reimplement a custom context that lazily pulls data from db, and maybe-reply.
import discord
from discord.ext import commands
import contextlib
from internal.enumerations import Table

class CrajyContext(commands.Context):
    """Custom context with two added features:
        - maybe_reply: replies to a message if there's a message between invocation message and reply
        - DB interaction; to easily get data from the db; the context has methods built to fetch the ctx.author's data.
    """
    async def user_data(self, table: Table, member: discord.Member = None) -> dict:
        """Returns `user`s data from the `table` specified.
        `user` defaults to ctx.author.
        The data returned is in an instance of asyncpg.Record - a tuple/dict hybrid, and can use both indexing and key lookup."""
        if member is None:
            member = self.author

        return await self.bot.db_pool.fetchrow(f"SELECT * FROM {table.name} WHERE user_id=$1", member.id)

    async def maybe_reply(self, content=None, mention_author=False, **kwargs):
        """Replies if there is a message in between the command invoker and the bot's message."""
        await asyncio.sleep(0.05)
        with contextlib.suppress(discord.HTTPException):
            if getattr(self.channel,"last_message", False) != self.message:
                return await self.reply(content, mention_author=mention_author, **kwargs)
        await self.send(content, **kwargs)
