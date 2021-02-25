import asyncio
import contextlib
import typing as t

import discord
from discord.ext import commands

from internal.enumerations import Table
from utils.embed import CrajyEmbed, EmbedResource


class CrajyContext(commands.Context):
    """Custom context with two added features:
    - maybe_reply: replies to a message if there's a message between invocation message and reply
    - DB interaction; to easily get data from the db; the context has methods built to fetch the ctx.author's data.
    """

    async def check_mark(self, target_message: discord.Message = None):
        if target_message is None:
            target_message = self.message
        try:
            await target_message.add_reaction(EmbedResource.CHECK_EMOJI.value)
        except:
            pass

    async def x_mark(self, target_message: discord.Message = None):
        if target_message is None:
            target_message = self.message
        try:
            await target_message.add_reaction(EmbedResource.XMARK_EMOJI.value)
        except:
            pass

    async def get_confirmation(self, target_message=None):
        """Asks the user for confirmation via reaction. `message` represents the initial message where the question is asked and reactions are added.
        Returns :: bool."""
        if target_message is None:
            target_message = self.message
        await self.check_mark(target_message)
        await self.x_mark(target_message)

        def check(reaction, member):
            if (
                str(reaction.emoji)
                in (EmbedResource.CHECK_EMOJI.value, EmbedResource.XMARK_EMOJI.value)
                and member == self.author
            ):
                return True

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=check, timeout=30
            )
            await target_message.clear_reactions()
            if str(reaction.emoji) == EmbedResource.CHECK_EMOJI.value:
                return True
            else:
                return False
        except Exception as e:
            if isinstance(e, asyncio.TimeoutError):
                await target_message.clear_reactions()
                return False
            elif isinstance(e, discord.errors.Forbidden):
                if str(reaction.emoji) == EmbedResource.CHECK_EMOJI.value:
                    return True
                else:
                    return False

    @contextlib.asynccontextmanager
    async def reaction_menu(
        self,
        prompt: t.Union[discord.Embed, CrajyEmbed],
        *emojis: t.Tuple[t.Union[str, discord.Emoji]],
    ) -> t.Generator[discord.Reaction, None, None]:
        """Edits self.message to `prompt`, and then adds the specified `emojis` as reactions.
        Yields :: The first reaction that the user made."""
        await self.message.edit(embed=prompt)

        emoji_set = set()
        for emoji in emojis:
            await self.message.add_reaction(emoji)
            emoji_set.add(str(emoji))

        def check(
            reaction: discord.Reaction, user: t.Union[discord.Member, discord.User]
        ) -> bool:
            return reaction.message == self.message and str(reaction) in emoji_set

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=check, timeout=60
            )
            yield reaction
        except Exception as e:
            if isinstance(e, discord.errors.Forbidden):
                return
        finally:
            await self.message.clear_reactions()
            return

    async def get_user_data(
        self, *, member: discord.Member = None, table: Table
    ) -> dict:
        """Returns `user`s data from the `table` specified.
        `user` defaults to ctx.author.
        The data returned is in an instance of asyncpg.Record - a tuple/dict hybrid, and can use both indexing and key lookup."""
        if member is None:
            member = self.author

        return await self.bot.db_pool.fetchrow(
            f"SELECT * FROM {table.name} WHERE user_id=$1", member.id
        )

    async def maybe_reply(
        self, content: str = None, mention_author: bool = False, **kwargs
    ):
        """Replies if there is a message in between the command invoker and the bot's message."""
        await asyncio.sleep(0.05)
        with contextlib.suppress(discord.HTTPException):
            if getattr(self.channel, "last_message", False) != self.message:
                return await self.reply(
                    content, mention_author=mention_author, **kwargs
                )
        return await self.send(content, **kwargs)
