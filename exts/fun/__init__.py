from exts.fun import birthday, stupid

def setup(bot):
    bot.add_cog(birthday.Birthday(bot))
    bot.add_cog(stupid.Stupid(bot))
