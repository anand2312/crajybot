from __future__ import annotations

from typing import cast

from discord import Interaction, Member, Message, TextStyle, User
from discord.app_commands import command, context_menu, Group
from discord.ui import Modal, TextInput
from prisma.models import Note

from logic.notes import create_note
from utils import embed as em


def create_embed(note: Note, user: Member | User) -> em.CrajyEmbed:
    embed = em.CrajyEmbed(
        title=f"Note Creation: ID {note.id}", embed_type=em.EmbedType.SUCCESS
    )
    embed.quick_set_author(user)
    embed.set_thumbnail(url=em.EmbedResource.NOTES.value)
    embed.description = (
        f"Added to your notes! Use `.notes return` to get all your stored notes."
    )
    return embed


class NoteModal(Modal, title="Create a note"):
    text = TextInput(label="Content", required=True, style=TextStyle.paragraph)

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)
        user = interaction.user
        content = self.text.value
        assert content
        note = await create_note(user, content)
        embed = create_embed(note, user)
        await interaction.followup.send(embed=embed)


notes_group = Group(name="notes", description="Manage your notes")


@notes_group.command(name="create", description="Create a note")
async def create_note_slash_cmd(interaction: Interaction) -> None:
    await interaction.response.send_modal(NoteModal())


@context_menu(name="Note this message")
async def create_note_msg_cmd(interaction: Interaction, message: Message) -> None:
    await interaction.response.defer(ephemeral=True, thinking=True)
    content = f"**{message.author.display_name}**:\n"
    content += (
        "> " + message.content[0:65] + "...\n\n" if len(message.content) > 65 else ""
    )
    content += f"[Jump]({message.jump_url})"
    note = await create_note(interaction.user, content)
    embed = create_embed(note, interaction.user)
    await interaction.followup.send(embed=embed)
