  
from discord.ext import commands
from utils import timezone

class CustomTimeConverter(commands.Converter):
    """Returns a timedelta object."""
    async def convert(self, ctx, arg: str) -> timezone.Timedelta:
        return timezone.get_timedelta(arg)