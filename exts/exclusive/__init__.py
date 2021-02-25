from exts.exclusive import betting, economy


def setup(bot):
    bot.add_cog(betting.Betting(bot))
    bot.add_cog(economy.Economy(bot))
