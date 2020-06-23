import discord
from redbot.core import commands
from redbot.core import checks
import asyncio

BaseCog = getattr(commands, "Cog", object)

class Massmove(BaseCog):
    """Massmove users to another voice channel"""


    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(move_members=True)
    async def massmove(self, ctx, from_channel: discord.VoiceChannel, to_channel: discord.VoiceChannel):
        """Massmove users to another voice channel. Use voice channel ID's."""
        await self._massmove(ctx, from_channel, to_channel)

    async def _massmove(self, ctx, from_channel, to_channel):
        """Internal function: Massmove users to another voice channel"""
        try:
            print('Starting move on SID: {}'.format(from_channel.guild.id))
            print('Getting copy of current list to move')
            voice_list = list(from_channel.members)
            for member in voice_list:
                await member.move_to(to_channel)
                print('Member {} moved to channel {}'.format(member.id, to_channel.id))
                await asyncio.sleep(0.05)
        except discord.Forbidden:
            await ctx.send('I have no permission to move members.')
        except discord.HTTPException:
            await ctx.send('A error occured. Please try again')

