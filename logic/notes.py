from __future__ import annotations
from datetime import datetime

from discord import Member, User
from prisma.models import Note, User as DbUser


async def create_note(
    member: User | Member,
    content: str,
    when: datetime | None = None,
    reminder: bool = False,
) -> Note:
    return await Note.prisma().create(
        {
            "raw_note": content,
            "reminder": reminder,
            "reminder_time": when,
            "User": {"connect": {"id": str(member.id)}},
        }
    )


async def delete_note(id: int) -> Note:
    note = await Note.prisma().delete({"id": id})
    if note is None:
        raise ValueError(f"Note with ID {id} not found")

    return note


async def delete_notes(user: Member | User, *ids: int) -> None:
    if len(ids) > 0:
        await Note.prisma().delete_many({"id": {"in": list(ids)}})
    else:
        await Note.prisma().delete_many({"userId": str(user.id)})


async def fetch_notes(user: Member | User, *ids: int) -> list[Note]:
    if len(ids) == 0:
        db_user = await DbUser.prisma().find_first(
            where={
                "id": str(user.id),
            },
            include={"Note": {"order_by": {"created_at": "desc"}}},
        )
    else:
        db_user = await DbUser.prisma().find_first(
            where={
                "id": str(user.id),
            },
            include={
                "Note": {
                    "where": {"id": {"in": list(ids)}},
                    "order_by": {"created_at": "desc"},
                }
            },
        )

    if db_user is None:
        return []
    if db_user.Note is None:
        return []
    return db_user.Note


async def fetch_reminders(user: User | Member, *ids: int) -> list[Note]:
    if len(ids) == 0:
        db_user = await DbUser.prisma().find_first(
            where={
                "id": str(user.id),
            },
            include={
                "Note": {
                    "order_by": {"created_at": "desc"},
                    "where": {
                        "reminder": True,
                    },
                }
            },
        )
    else:
        db_user = await DbUser.prisma().find_first(
            where={
                "id": str(user.id),
            },
            include={
                "Note": {
                    "where": {
                        "id": {"in": list(ids)},
                        "reminder": True,
                    },
                    "order_by": {"created_at": "desc"},
                }
            },
        )

    if db_user is None:
        return []
    if db_user.Note is None:
        return []
    return db_user.Note
