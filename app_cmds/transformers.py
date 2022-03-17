from datetime import timedelta

from discord import Interaction
from discord.app_commands import Transformer

from utils.timezone import get_timedelta


class TimedeltaTransformer(Transformer):
    @classmethod
    async def transform(cls, _: Interaction, value: str) -> timedelta:
        return get_timedelta(value)
