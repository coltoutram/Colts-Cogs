import discord
from redbot.core.utils.antispam import AntiSpam
from discord.ext import commands
from redbot.core import checks

class Playskip:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playskip(self, ctx, *, query):
        """Play and skip."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()
        else:
            skip = self.bot.get_command('skip')
            play = self.bot.get_command('play')
            await ctx.invoke(skip)
            await ctx.invoke(play, query=query)