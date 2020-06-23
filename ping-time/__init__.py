from .pingtime import Pingtime

def setup(bot):
    n = Pingtime(bot)
    bot.add_cog(n)
