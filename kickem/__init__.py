from .penis import Penis

def setup(bot):
    n = Penis(bot)
    bot.add_cog(n)
