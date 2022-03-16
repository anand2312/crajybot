from __future__ import annotations

from datetime import datetime, timedelta
from typing import Union

from discord import Guild, Member, User
from prisma.models import User as DbUser, Guild as DbGuild


async def fetch_birthday(member: Member) -> datetime:
    db_member = await DbUser.prisma().find_first(
        where={"id": {"equals": str(member.id)}}
    )
    if db_member is None:
        db_member = await DbUser.prisma().create(
            {"id": str(member.id), "Guild": {"connect": {"id": str(member.guild.id)}}}
        )

    if db_member.birthday is None:
        raise ValueError("User's birthday has not been registered yet.")

    return db_member.birthday


async def update_birthday(member: Union[Member, User], bday: datetime) -> None:
    await DbUser.prisma().update({"birthday": bday}, {"id": str(member.id)})


async def list_guild_birthdays(guild: Guild) -> list[DbUser]:
    db_guild = await DbGuild.prisma().find_unique(
        {"id": str(guild.id)}, {"User": {"order_by": {"birthday": "asc"}}}
    )

    if db_guild is None:
        await DbGuild.prisma().create({"id": str(guild.id)})
        return []

    return db_guild.User or []


async def birthdays_in_timedelta(td: timedelta = timedelta(days=1)) -> list[DbUser]:
    bound = datetime.utcnow() + td
    return await DbUser.prisma().find_many(
        where={"birthday": {"lte": bound}},
        order={"birthday": "asc"},
        include={"Guild": True},
    )