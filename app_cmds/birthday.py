from discord import Interaction, Member
from discord.app_commands import command, context_menu

from logic.birthday import fetch_birthday


__all__ = [
    "fetch_birthday_user_cmd",
]


@context_menu(name="Fetch birthday")
async def fetch_birthday_user_cmd(interaction: Interaction, member: Member) -> None:
    print("hi", interaction)
    embed = await fetch_birthday(member)
    await interaction.response.send_message(embed=embed, ephemeral=True)
