from .actionlogs import Actionlogs

def setup(bot):
    bot.add_cog(Actionlogs(bot))