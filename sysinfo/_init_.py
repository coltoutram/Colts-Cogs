from .sysinfo import SysInfo

def setup(bot):
    n = SysInfo(bot)
    bot.add_cog(n)
