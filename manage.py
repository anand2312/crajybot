import asyncio
from argparse import ArgumentParser

from loguru import logger

from bot import main


parser = ArgumentParser(prog="CrajyBot", description="Run CrajyBot")
parser.add_argument("-e", "--exts", help="List of extensions to load", nargs="*")

args = parser.parse_args()

logger.info(f"Starting bot")

if args.exts is None:
    asyncio.run(main())
else:
    func = lambda x: f"exts.{x}"
    exts = list(map(func, args.exts))
    asyncio.run(main(exts))
