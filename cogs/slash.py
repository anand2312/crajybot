from discord.ext import commands
from discord_slash import cog_ext, SlashCommand, SlashContext, utils

class CrajySlashCommands(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, auto_register=True, override_type=True)

        self.bot = bot
        self.bot.slash.get_cog_commands(self)
        
    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)
        
    @cog_ext.cog_slash(name="wat", 
                       description="Use a wat command",
                       guild_ids=[298871492924669954], 
                       options=[utils.manage_commands.create_option(
                            name="use", 
                            description="Which tag to bring.",
                            option_type=3,
                            required=True)])
    async def slash_wat(self, ctx: SlashContext, use: str):
        existing = await self.bot.db_pool.fetchval("SELECT content FROM tags WHERE LOWER(tag_name)=$1", use)
        await ctx.send(content=existing)

def setup(bot):
    bot.add_cog(CrajySlashCommands(bot))
