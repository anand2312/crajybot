from __future__ import annotations

from datetime import datetime, timedelta
from typing import Union

from discord import Guild, Member, User
from prisma.models import User as DbUser, Guild as DbGuild

from internal import enumerations as enums
from utils import embed as em


async def _fetch_birthday(member: Member) -> DbUser:
    db_member = await DbUser.prisma().find_first(
        where={"id": {"equals": str(member.id)}}
    )
    if db_member is None:
        db_member = await DbUser.prisma().create(
            {"id": str(member.id), "Guild": {"connect": {"id": str(member.guild.id)}}}
        )

    if db_member.birthday is None:
        raise ValueError("User's birthday has not been registered yet.")

    return db_member


async def fetch_birthday(member: Member) -> em.CrajyEmbed:
    user_data = await _fetch_birthday(member)

    assert user_data.birthdate
    assert user_data.birthday

    embed = em.CrajyEmbed(
        title=f"{member.display_name}'s birthday",
        description=user_data.birthdate,
        embed_type=enums.EmbedType.INFO,
    )
    embed.set_thumbnail(url=em.EmbedResource.BDAY.value)
    embed.quick_set_author(member)

    today = datetime.today()
    this_year_date = datetime.strptime(
        user_data.birthdate + f" {today.year}", "%d %B %Y"
    )
    remaining = this_year_date - today

    if remaining < timedelta(seconds=0):
        # birthday is in the past; get next birthday
        next_birthday = this_year_date.replace(year=today.year + 1)
        remaining = next_birthday - today

    embed.set_footer(text=f"Their birthday is in {remaining}")

    return embed


async def update_birthday(member: Union[Member, User], bday: datetime) -> None:
    date = bday.strftime("%d %B")
    await DbUser.prisma().update(
        {"birthday": bday, "birthdate": date}, {"id": str(member.id)}
    )


async def list_guild_birthdays(guild: Guild) -> list[DbUser]:
    db_guild = await DbGuild.prisma().find_unique(
        {"id": str(guild.id)}, {"User": {"order_by": {"birthday": "asc"}}}
    )

    if db_guild is None:
        await DbGuild.prisma().create({"id": str(guild.id)})
        return []

    return db_guild.User or []


async def birthdays_today() -> list[DbUser]:
    today = datetime.utcnow()
    query = (
        "SELECT * FROM User "
        "WHERE strftime('%d', DATETIME(ROUND(birthday / 1000), 'unixepoch')) = ? "
        "AND strftime('%m', DATETIME(ROUND(birthday / 1000), 'unixepoch')) = ?"
    )
    users = await DbUser.prisma().query_raw(
        query, f"{today.day:02}", f"{today.month:02}"
    )

    for user in users:
        guild_query = (
            "SELECT t1.* FROM Guild t1 "
            "INNER JOIN _GuildToUser t2 ON t1.id = t2.A "
            "WHERE t2.B = ?"
        )
        guilds = await DbGuild.prisma().query_raw(guild_query, user.id)
        user.Guild = guilds

    return users
