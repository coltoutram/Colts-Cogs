from .massmove import Massmove

def setup(bot):
    n = Massmove(bot)
    bot.add_cog(n)
