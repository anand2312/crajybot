from exts.utility import moderator
from exts.utility import misc
from exts.utility import notes
from exts.utility import tags


async def setup(bot):
    await bot.add_cog(moderator.Moderator(bot))
    await bot.add_cog(misc.Miscellaneous(bot))
    await bot.add_cog(notes.Notes(bot))
    await bot.add_cog(tags.Tags(bot))
