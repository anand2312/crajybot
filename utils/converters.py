import re
from datetime import timedelta

from discord.ext import commands
from utils import timezone


FORMATTED_CODE_REGEX = re.compile(
    r"```(?P<lang>[a-z+]+)?\s*" r"(?P<code>.*)" r"\s*" r"```", re.DOTALL | re.IGNORECASE
)


class CustomTimeConverter(commands.Converter):
    """Returns a timedelta object."""

    async def convert(self, _: commands.Context, arg: str) -> timedelta:
        return timezone.get_timedelta(arg)


class KwargConverter(commands.Converter):
    """Takes a string kwarg and returns a dict.
    This has to be used along with Greedy and dict merging for multiple kwargs."""

    async def convert(self, _: commands.Context, arg: str) -> dict:
        return dict([arg.split("=")])


class LanguageConverter(commands.Converter):
    async def convert(self, _: commands.Context, argument: str):
        if argument.lower() not in {"python", "rust", "javascript", "go"}:
            raise commands.BadArgument("Not a valid language")
        return argument.lower()


class CodeBlockConverter(commands.Converter):
    async def convert(self, _: commands.Context, code: str):
        match = FORMATTED_CODE_REGEX.search(code)
        if match:
            code = match.group("code")

        return match, code
