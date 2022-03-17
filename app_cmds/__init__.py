from __future__ import annotations

from discord.app_commands import Command, ContextMenu, Group

from app_cmds import birthday

__all__ = ["cmds", "groups"]


cmds: list[Command | ContextMenu] = [birthday.fetch_birthday_user_cmd]
groups: list[type[Group]] = []
