from __future__ import annotations

from discord import Guild, Member, User
from prisma.models import Tag


async def create_tag(
    author: User | Member, guild: Guild, tag_name: str, content: str
) -> Tag:
    # check if tag with same name exists
    existing = await Tag.prisma().find_first(
        where={"tag_name": tag_name, "guildId": str(guild.id)}
    )
    if existing is not None:
        raise ValueError(f"A tag with name {tag_name} already exists in this guild")

    return await Tag.prisma().create(
        {
            "tag_name": tag_name,
            "content": content,
            "Guild": {"connect": {"id": str(guild.id)}},
            "User": {"connect": {"id": str(author.id)}},
        }
    )


async def delete_tag(id: int) -> Tag | None:
    return await Tag.prisma().delete({"id": id})


async def fetch_tag_for_guild(name: str, guild_id: int) -> Tag | None:
    return await Tag.prisma().find_first(
        where={"tag_name": name, "guildId": str(guild_id)}
    )


async def search_tags_for_guild(query: str, guild_id: int) -> list[Tag]:
    return await Tag.prisma().find_many(
        where={"tag_name": {"contains": query}, "guildId": str(guild_id)}
    )
