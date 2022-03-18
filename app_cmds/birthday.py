from __future__ import annotations

from datetime import datetime
from re import M
from discord import Interaction, Member
from discord.app_commands import context_menu, describe, Group, Namespace, Choice
from pytz import common_timezones_set, timezone as _timezone

from internal import enumerations as enums
from logic.birthday import fetch_birthday, update_birthday
from utils import embed as em


__all__ = [
    "fetch_birthday_user_cmd",
]


@context_menu(name="Fetch birthday")
async def fetch_birthday_user_cmd(interaction: Interaction, member: Member) -> None:
    try:
        embed = await fetch_birthday(member)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except ValueError as e:
        await interaction.response.send_message(e.args[0])


bday_group = Group(name="bday", description="Commands related to users birthdays")


@bday_group.command(name="set", description="Set a user's birthday")
@describe()
async def bday_set_slash_cmd(
    interaction: Interaction, date: str, timezone: str
) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)
    tz = _timezone(timezone)
    bday = datetime.strptime(date, "%d-%m-%Y")
    bday = tz.localize(bday)

    await update_birthday(interaction.user, bday)

    out = em.CrajyEmbed(title=f"Birthday Set!", embed_type=enums.EmbedType.SUCCESS)
    out.description = (
        f"{interaction.user.display_name}'s birthday is saved. They shall be wished."
    )
    out.set_thumbnail(url=em.EmbedResource.BDAY.value)
    out.quick_set_author(interaction.user)
    await interaction.followup.send(embed=out)


@bday_set_slash_cmd.autocomplete("timezone")
async def timezone_autocomplete(
    interaction: Interaction, current: str
) -> list[Choice[str]]:
    choices = [Choice(name=i, value=i) for i in common_timezones_set]
    choices.extend(
        [
            Choice(name=i, value="Asia/Kolkata")
            for i in ["India", "IST"]  # special case these because we use it more
        ]
    )

    return [
        Choice(name=i, value=i)
        for i in common_timezones_set
        if current.lower() in i.lower()
    ][0:10]
