from __future__ import annotations
from pathlib import Path
from traceback import print_exception

import discord
from discord.ext import commands
from loguru import logger

from internal.bot import CrajyBot
from secret.TOKEN import TOKEN


intents = discord.Intents.default()
intents.members = True  # TO DO: Investigate feature-loss with Member intents disabled
intents.message_content = True

bot = CrajyBot(
    command_prefix=commands.when_mentioned_or("."),
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="cute panda videos or something."
    ),
    intents=intents,
    owner_id=271586885346918400,
)


async def main(exts: list[str] | None = None) -> None:
    if exts is not None:
        for ext in exts:
            await bot.load_extension(ext)

    else:
        for ext in Path("./exts").iterdir():
            if ext.name in ["__pycache__", "__init__.py"]:
                continue
            try:
                await bot.load_extension(f"exts.{ext.name}")
            except Exception as e:
                logger.error(f"Error occurred while loading {ext=}")
                print_exception(type(e), e, e.__traceback__)
                continue

    try:
        await bot.load_extension("jishaku")
    except Exception as e:
        logger.warning(
            "Can't load jishaku; jishaku doesn't yet support async setup/teardown"
        )

    logger.info("Finished loading extensions")

    async with bot:
        await bot.start(TOKEN)
