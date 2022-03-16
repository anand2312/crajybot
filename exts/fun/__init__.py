from typing import TYPE_CHECKING

from exts.fun import birthday  # , stupid

if TYPE_CHECKING:
    from internal.bot import CrajyBot
else:
    CrajyBot = "CrajyBot"


async def setup(bot: CrajyBot) -> None:
    await bot.add_cog(birthday.Birthday(bot))
    # await bot.add_cog(stupid.Stupid(bot))


# TODO: load stupid cog
