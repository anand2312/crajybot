import os
import dotenv

from utils.menu import Menu

dotenv.load_dotenv(dotenv.find_dotenv())

# TO DO: Switch to argparse

TOKEN = os.environ.get("TOKEN")

def setup() -> None:
    raise NotImplementedError()

def debug():
    print("DEBUG MODE")
    print(
        "Enter the name of the cog that you want to load. The name must match the filename."
    )
    print("For example; to load `cogs/amongus.py` - enter `amongus`.")
    print(
        "If you want to load multiple cogs, enter their names separated by spaces. For example; `amongus economy`."
    )
    func = lambda x: f"cogs.{x}"
    cogs = list(map(func, input().split()))
    from bot import bot

    @bot.event
    async def on_ready():  # sends this message when bot starts working in #bot-tests
        await bot.get_channel(int(os.environ.get("BOT_TEST_CHANNEL"))).send(
            f"Bot running in debug mode! Cogs loaded - {', '.join(cogs)}, jishaku."
        )
        print(f"Bot running in debug mode! Cogs loaded - {', '.join(cogs)}, jishaku.")

    for cog in cogs:
        bot.load_extension(cog)
    else:
        bot.load_extension("jishaku")
    bot.run(TOKEN)

if __name__ == "__main__":
    functions = [setup, debug]
    menu = Menu(
        *functions, heading="Bot Control", format_symbol="=", continue_prompt=False
    )
    menu.run()
