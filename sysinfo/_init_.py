from .sysinfo import Sysinfo

def setup(bot):
    n = Sysinfo(bot)
    bot.add_cog(n)
