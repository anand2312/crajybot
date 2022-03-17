"""Some functions to remember and wish your server members."""
from datetime import datetime, timezone
from typing import cast, TYPE_CHECKING, Optional, Union

import discord
import pytz
from discord import Member, User
from discord.ext import commands, tasks
from loguru import logger

from internal import enumerations as enums
from internal.context import CrajyContext
from internal.enumerations import EmbedType
from logic.birthday import (
    birthdays_today,
    fetch_birthday,
    list_guild_birthdays,
    update_birthday,
)
from utils import embed as em

if TYPE_CHECKING:
    from internal.bot import CrajyBot
else:
    CrajyBot = "CrajyBot"


class Birthday(commands.Cog):  # TO DO: Make this public-workable
    def __init__(self, bot: CrajyBot) -> None:
        self.bot = bot
        self.bot.task_loops["bday"] = self.birthday_loop

    @commands.group(
        name="bday",
        aliases=["birthday"],
        help="Retrieve a birthday date. Could be your own if no user is specified, or a specified user.",
        invoke_without_command=True,
    )
    async def bday(
        self, ctx: CrajyContext, person: Union[Member, User, None] = None
    ) -> None:
        person = person or ctx.author
        embed = await fetch_birthday(cast(Member, person))
        await ctx.maybe_reply(embed=embed)

    @bday.command(
        name="add",
        aliases=["-a"],
        help="Add a birthday date. Could be your own if no user is specified, or a specified user.",
    )
    @commands.guild_only()
    async def bday_add(self, ctx: CrajyContext, person: Optional[Member] = None):
        if person is None:
            person = cast(Member, ctx.author)

        ask_embed = em.CrajyEmbed(
            title=f"Setting Birthday for {person.display_name}",
            embed_type=enums.EmbedType.INFO,
        )
        ask_embed.description = f"Enter the date in DD-MM-YYYY format"
        ask_embed.set_thumbnail(url=em.EmbedResource.BDAY.value)
        ask_embed.quick_set_author(person)

        ask_message = await ctx.maybe_reply(embed=ask_embed)

        def check(m: discord.Message) -> bool:
            return (
                m.author == ctx.author
                and len(m.content.split("-")) == 3
                and m.guild is not None
            )

        def tz_check(m: discord.Message) -> bool:
            return m.content in pytz.all_timezones_set

        reply = await self.bot.wait_for("message", check=check, timeout=30)
        date = datetime.strptime(reply.content, "%d-%m-%Y")

        tz_prompt = await ctx.send("Enter your timezone")

        tz_message = await self.bot.wait_for("message", check=tz_check, timeout=30)
        tz = pytz.timezone(tz_message.content)
        date = tz.localize(date)

        await update_birthday(person, date)

        out = em.CrajyEmbed(title=f"Birthday Set!", embed_type=enums.EmbedType.SUCCESS)
        out.description = (
            f"{person.display_name}'s birthday is saved. They shall be wished."
        )
        out.set_thumbnail(url=em.EmbedResource.BDAY.value)
        out.quick_set_author(person)

        await tz_prompt.delete()
        return await ask_message.edit(embed=out)

    @bday.command(
        name="all", aliases=["list"], help="Get a list of all birthdays saved."
    )
    @commands.guild_only()
    async def bday_all(self, ctx: CrajyContext):
        if ctx.guild is None:
            # will be caught by the deco, but done here for type checking
            return

        response = em.CrajyEmbed(
            title="Everyone's birthdays", embed_type=enums.EmbedType.INFO
        )
        response.set_thumbnail(url=em.EmbedResource.BDAY.value)

        all_data = await list_guild_birthdays(ctx.guild)

        for person in all_data:
            person_obj = ctx.guild.get_member(int(person.id))

            if person_obj is None:
                continue

            if person.birthday is None:
                continue

            response.add_field(
                name=person_obj.display_name,
                value=person.birthday.strftime("%d %B %Y"),
                inline=False,
            )
        await ctx.maybe_reply(embed=response)

    async def send_wish(
        self, channel: discord.TextChannel, person: discord.Member
    ) -> None:
        embed = em.CrajyEmbed(
            title=f"Happy Birthday {person.display_name}!",
            embed_type=EmbedType.SUCCESS,
        )
        embed.quick_set_author(person)
        await channel.send(embed=embed)

    @tasks.loop(hours=24)
    async def birthday_loop(self):
        # TO DO: Make more fine-tuned loop which will schedule a wish in case it isn't the exact time at loop execution.
        logger.info("Started birthday loop")
        users = await birthdays_today()
        logger.debug(f"Today's birthdays: {users}")

        for user in users:
            now = datetime.now(timezone.utc)
            if user.Guild is None:
                logger.warning(
                    f"BDAY LOOP: No guilds found for user {user.id}; inconsistency"
                )
                return

            guild = self.bot.get_guild(int(user.Guild[0].id))

            if guild is None:
                logger.warning(
                    f"BDAY LOOP: Guild {user.Guild[0].id} could not be found"
                )
                return

            person_obj = guild.get_member(int(user.id))

            if person_obj is None:
                logger.warning(f"BDAY LOOP: User object not found for {user.id}")
                return

            embed = em.CrajyEmbed(
                title=f"Happy Birthday {person_obj.display_name}!",
                embed_type=EmbedType.SUCCESS,
            )
            embed.quick_set_author(person_obj)

            for guild in user.Guild:
                guild_obj = self.bot.get_guild(int(guild.id))
                if guild_obj is None:
                    logger.info(f"BDAY LOOP: Guild object {guild.id=} not found ")
                    continue
                if guild.bot_channel is None:
                    logger.info(
                        f"BDAY LOOP: Bot channel not registered for guild {guild.id}"
                    )
                    continue

                channel = cast(
                    discord.TextChannel, guild_obj.get_channel(int(guild.bot_channel))
                )

                if channel is None:
                    logger.info(
                        f"BDAY LOOP: Channel not found {guild.bot_channel=} for {guild.id=}"
                    )
                    continue

                assert user.birthday
                user_birthday = user.birthday.replace(year=now.year)
                difference = user_birthday - now

                self.bot.scheduler.schedule(
                    self.send_wish(channel, person_obj), datetime.utcnow() + difference
                )

    @birthday_loop.before_loop
    async def birthdayloop_before(self):
        await self.bot.wait_until_ready()
