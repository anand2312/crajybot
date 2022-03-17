from __future__ import annotations

from discord.app_commands import Command, ContextMenu, Group

from app_cmds import birthday
from app_cmds import note

__all__ = ["cmds", "groups"]


cmds: list[Command | ContextMenu] = [
    birthday.fetch_birthday_user_cmd,
    note.create_note_msg_cmd,
]
groups: list[Group] = [note.notes_group, birthday.bday_group]
