# reimplement a custom context that lazily pulls data from db, and maybe-reply.
from discord.ext import commands
import contextlib
from internal.enumerations import Table

class CrajyContext(commands.Context):
    """Custom context with two added features:
        - maybe_reply: replies to a message if there's a message between invocation message and reply
        - DB interaction; to easily get data from the db; the context has methods built to fetch the ctx.author's data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__.update(dict.fromkeys(["waiting", "result", "channel_used", "running", "failed"]))

    async def author_data(self, table: Table) -> dict:
        async with self.bot.db_pool.acquire() as connection:
            async with connection.transaction():
                ...

    async def maybe_reply(self, content=None, mention_author=False, **kwargs):
        """Replies if there is a message in between the command invoker and the bot's message."""
        await asyncio.sleep(0.05)
        with contextlib.suppress(discord.HTTPException):
            if getattr(self.channel,"last_message", False) != self.message:
                return await self.reply(content, mention_author=mention_author, **kwargs)
        await self.send(content, **kwargs)

    # get column keys for dictify from the table enum