from exts.games import games


def setup(bot):
    bot.add_cog(games.Games(bot))
