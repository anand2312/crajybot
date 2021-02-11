from datetime import timedelta  

from discord.ext import commands
from utils import timezone

class CustomTimeConverter(commands.Converter):
    """Returns a timedelta object."""
    async def convert(self, ctx, arg: str) -> timedelta:
        return timezone.get_timedelta(arg)
    
    
class KwargConverter(commands.Converter):
    """Takes a string kwarg and returns a dict.
    This has to be used along with Greedy and dict merging for multiple kwargs."""
    async def convert(self, ctx, arg: str) -> dict:
        return dict([arg.split("=")])
    
