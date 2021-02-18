from exts.games import amongus, games

def setup(bot):
    bot.add_cog(amongus.AmongUs(bot))
    bot.add_cog(games.Games(bot))
