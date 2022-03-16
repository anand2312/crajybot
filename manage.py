import asyncio
from typing import cast

from discord import TextChannel
from loguru import logger

from bot import bot, main
from secret.constants import BOT_TEST_CHANNEL
from utils.menu import Menu


def debug() -> None:
    print("DEBUG MODE")
    print("Enter extension(s) to load: ")
    func = lambda x: f"exts.{x}"
    cogs = list(map(func, input().split()))

    @bot.event
    async def on_ready() -> None:
        channel = cast(TextChannel, bot.get_channel(BOT_TEST_CHANNEL))

        if channel is None:
            logger.warning("Bot test channel not found in cache")
            return

        await channel.send(
            f"Bot running in debug mode! Cogs loaded - {', '.join(cogs)}, jishaku."
        )

    asyncio.run(main(cogs))


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    functions = [debug, run]
    menu = Menu(
        *functions, heading="CrajyBot runner", format_symbol="=", continue_prompt=False
    )
    menu.run()
