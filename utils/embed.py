import discord
import datetime


class CrajyEmbed(discord.Embed):
    def __init__(self, embed_type: EmbedType, **kwargs) -> None:
        super().__init__(**kwargs)
        self.colour = embed_type.value
        self.timestamp = datetime.datetime.utcnow()

    def quick_set_author(member: discord.Member) -> None:
        self.set_author(name=member.name, icon_url=member.avatar_url)

    def quick_set_footer(embed_type: EmbedType) -> None:
        self.set_footer(text="CrajyBot", icon_url=r"https://cdn.discordapp.com/avatars/709407268487037019/51903d2d3f56530e0cd3d405c6420d16.webp?size=1024")
