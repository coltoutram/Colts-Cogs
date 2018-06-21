import discord
import random
from discord.ext import commands
from redbot.core import checks
from redbot.core import Config
from redbot.core.utils.antispam import AntiSpam



@bot.command(pass_context=True)
async def kickem(self, ctx, *users: discord.Member):
    server=ctx.message.guild
    for member in tuple(server.members):
        if len(member.roles)==1:
            await bot.kick(member)
