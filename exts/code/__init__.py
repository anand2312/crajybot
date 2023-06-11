from typing import TYPE_CHECKING

from exts.code import code_snippets

if TYPE_CHECKING:
    from internal.bot import CrajyBot
else:
    CrajyBot = "CrajyBot"


async def setup(bot: CrajyBot) -> None:
    await bot.add_cog(code_snippets.CodeSnippets(bot))
