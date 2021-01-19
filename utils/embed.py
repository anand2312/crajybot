import discord
from discord.ext import menus
import datetime
import enum
from internal.enumerations import EmbedType


class CrajyEmbed(discord.Embed):
    def __init__(self, embed_type: EmbedType, **kwargs) -> None:
        """Both quick_set_author and footer modify the existing Embed object, and not return a new one."""
        super().__init__(**kwargs)
        self.colour = embed_type.value
        self.timestamp = datetime.datetime.utcnow()

    def quick_set_author(self, member: discord.Member) -> None:
        self.set_author(name=member.name, icon_url=member.avatar_url)

    def quick_set_footer(self, embed_type: EmbedType) -> None:
        # implement different footers for different embed types.
        self.set_footer(text="CrajyBot", icon_url=r"https://cdn.discordapp.com/avatars/709407268487037019/51903d2d3f56530e0cd3d405c6420d16.webp?size=1024")


class EmbedResource(enum.Enum):
    """URLs and emojis to be used in embeds."""
    NOTES = r"https://media.discordapp.net/attachments/612638234782072882/800744704434110514/notes.png?width=384&height=384"
    BDAY = r"https://media.discordapp.net/attachments/612638234782072882/800965411130179584/fhnpyxb3ywi21-removebg-preview.png?width=508&height=277"
    LOVE_CALC = r"https://media.discordapp.net/attachments/612638234782072882/801042923050762251/how-technology-is-changing-the-way-we-love.png?width=545&height=408"
    TAG = r"https://media.discordapp.net/attachments/612638234782072882/801049755392016414/red-tags-vector-clipart.png?width=409&height=409"
    PIN = r"https://media.discordapp.net/attachments/612638234782072882/758190572526764052/emoji.png?width=58&height=58"
    TRASHCAN = r"https://media.discordapp.net/attachments/612638234782072882/801083964893691954/unknown.png?width=128&height=137"
    GREEN_UPDATE = r"https://media.discordapp.net/attachments/612638234782072882/801089944750915594/greenupdate.png?width=111&height=110"
    RED_UPDATE = r"https://media.discordapp.net/attachments/612638234782072882/801122219711397948/redupdate2.png?width=111&height=110"
    WARNING = r"https://media.discordapp.net/attachments/612638234782072882/801097916458205244/DPBue_correct.png?width=384&height=384"
    MINECRAFT = r"https://media.discordapp.net/attachments/757877755395309609/779682985163227146/apps.png?width=158&height=158"
    BANK = r"https://media.discordapp.net/attachments/612638234782072882/801121556029112350/unknown.png?width=84&height=74"
    PAYMENT = r"https://media.discordapp.net/attachments/612638234782072882/801123162431422474/monies.png?width=446&height=314"
    ROBBER_1 = r"https://media.discordapp.net/attachments/612638234782072882/801124352539099218/robbery-removebg-preview.png?width=448&height=314"
    ROBBER_2 = r"https://media.discordapp.net/attachments/612638234782072882/801124817810096149/robber1.png?width=433&height=325"
    LOSS = r"https://media.discordapp.net/attachments/703141348131471440/801170491825586186/f32b53ccfc1d7994dd6489b71068e55be6-loss-thumb.png?width=143&height=143"
    CHECK_EMOJI = "<:check:800771830116909066>"
    XMARK_EMOJI = "<:xmark:800773561093849119>"


class __ListEmbedSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, page):
        return page

def quick_embed_paginate(embeds: list) -> menus.MenuPages:
    """Does the two step process of making ListPageSource, and making MenuPages in one function."""
    source = __ListEmbedSource(embeds)
    return menus.MenuPages(source=source, clear_reactions_after=True)
