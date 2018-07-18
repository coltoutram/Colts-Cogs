import discord
from discord.ext import commands
from redbot.core import checks

class Playskip:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playskip(self, ctx, *, query):
        """Play and skip."""
        play = self.bot.get_command('play')
        skip = self.bot.get_command('skip')
        await ctx.invoke(play, query=query)
        await ctx.invoke(skip)
