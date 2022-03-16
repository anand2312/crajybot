from __future__ import annotations
from pathlib import Path

import discord
from discord.ext import commands
from loguru import logger

from internal.bot import CrajyBot
from secret.TOKEN import TOKEN


intents = discord.Intents.default()
intents.members = True  # TO DO: Investigate feature-loss with Member intents disabled
intents.messages = True
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
            await bot.load_extension(f"exts.{ext.name}")

    try:
        await bot.load_extension("jishaku")
    except Exception as e:
        logger.info(
            "Can't load jishaku; jishaku doesn't yet support async setup/teardown"
        )

    logger.info("Finished loading extensions")

    async with bot:
        await bot.start(TOKEN)
