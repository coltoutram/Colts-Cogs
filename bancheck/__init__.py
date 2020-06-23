from .bancheck import BanList


def setup(bot):
    n = BanList(bot)
    bot.add_listener(n._banjoin,"on_member_join")
    bot.add_cog(n)
