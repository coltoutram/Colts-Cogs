from .speedtest import Speedtest

def setup(bot):
    n = Speedtest(bot)
    bot.add_cog(n)
