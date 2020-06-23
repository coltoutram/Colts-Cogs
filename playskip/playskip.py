import discord
import asyncio
import time
from redbot.core import commands
from redbot.core import checks

BaseCog = getattr(commands, "Cog", object)

class Playskip(BaseCog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playskip(self, ctx, *, query):
        """Play and skip."""
        play = self.bot.get_command('play')
        skip = self.bot.get_command('skip')
        await ctx.invoke(play, query=query)
        await asyncio.sleep(1)
        await ctx.invoke(skip)
