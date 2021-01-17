import discord
import datetime
import enum


class EmbedType(enum.Enum):
    FAIL = 1
    SUCCESS = 2
    WARNING = 3
    BOT = 4


class CrajyEmbed(discord.Embed):
    def __init__(self, embed_type: EmbedType, **kwargs) -> None:
        super().__init__(**kwargs)
        mapping = {
            EmbedType.FAIL: 0xFF0000,
            EmbedType.SUCCESS: 0x32CD32,
            EmbedType.WARNING: 0xFFFF00,
            EmbedType.BOT: 0xA9A9A9
            }
        self.colour = mapping[embed_type]
        self.timestamp = datetime.datetime.utcnow()

    def quick_set_author(member: discord.Member) -> None:
        self.set_author(name=member.name, icon_url=member.avatar_url)

    def quick_set_footer(embed_type: EmbedType) -> None:
        self.set_footer(text="CrajyBot", icon_url=r"https://cdn.discordapp.com/avatars/709407268487037019/51903d2d3f56530e0cd3d405c6420d16.webp?size=1024")
