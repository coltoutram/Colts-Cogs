from .autorole import Autorole

def setup(bot):
    n = Autorole(bot)
    bot.add_cog(n)
