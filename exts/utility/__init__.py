from exts.utility import moderator  # , notes, tags


async def setup(bot):
    await bot.add_cog(moderator.Moderator(bot))
    # bot.add_cog(notes.Notes(bot))
    # bot.add_cog(tags.Tags(bot))
