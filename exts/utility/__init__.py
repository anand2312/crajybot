from exts.utility import moderator
from exts.utility import misc


async def setup(bot):
    await bot.add_cog(moderator.Moderator(bot))
    await bot.add_cog(misc.Miscellaneous(bot))
    # bot.add_cog(notes.Notes(bot))
    # bot.add_cog(tags.Tags(bot))
