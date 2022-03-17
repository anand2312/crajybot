import asyncio
from argparse import ArgumentParser

from loguru import logger

from bot import main


parser = ArgumentParser(prog="CrajyBot", description="Run CrajyBot")
parser.add_argument("-e", "--exts", help="List of extensions to load", nargs="*")

args = parser.parse_args()

func = lambda x: f"exts.{x}"
exts = list(map(func, args.exts))


logger.info(f"Starting bot")

if len(exts) == 0:
    asyncio.run(main())
else:
    asyncio.run(main(exts))
