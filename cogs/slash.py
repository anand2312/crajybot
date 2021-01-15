from discord.ext import commands
from discord_slash import cog_ext, SlashCommand, SlashContext

class CrajySlashCommands(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, auto_register=True, override_type=True)

        self.bot = bot
        self.bot.slash.get_cog_commands(self)
        
    @cog_ext.cog_subcommand(base="wat", name="use", guild_ids=[298871492924669954])
    async def slash_wat(self, ctx: SlashContext, text: str):
        existing = await self.bot.stupid_collection.find_one({"key": text})
        await ctx.send(content=existing["output"])

def setup(bot):
    bot.add_cog(CrajySlashCommands(bot))