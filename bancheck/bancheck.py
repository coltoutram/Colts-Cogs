import discord
from discord.ext import commands
import aiohttp
import re
import os
from redbot.core import checks
from redbot.core import Config
from redbot.core.utils.antispam import AntiSpam
from dbans import DBans

dBans = DBans(token="Ww6KVpkMZ1")
URL = "https://bans.discordlist.net/api"
DEFAULT = {
"ENABLED" : True,
"guild" : None,
"ban" : False} # will add another day


class BanList():

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 54564894107)
        self.config.register_guild(**{"ENABLED":True})
        self.users = {}
        self.messages = {}; print('NOTICE: LOADED BANCHECK')
 

    def embed_maker(self, title, color, description):
        embed=discord.Embed(title=title, color=color, description=description)
        return embed

    async def lookup(self, user):
        async with aiohttp.ClientSession() as ses:
            resp = await self.session.post(URL, data=self.payload(user))
            final = await resp.json()
            resp.close()
            return final

    @checks.admin_or_permissions(manager_server=True)
    @commands.group(pass_context=True)
    async def bancheck(self, ctx):
        """Check new users against a ban list."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def channel(self, ctx, channel:discord.TextChannel=None):
        """Set the channel you want members to welcomed in"""
        if channel is None:
            channel = ctx.message.channel
        await self.config.guild(ctx.guild).channel.set(ctx.channel.id)
        try:
            await ctx.send(channel,
                embed=self.embed_maker(None ,0x008000,
                    ':white_check_mark: **I will send all ban check notices here.**'))
        except discord.errors.Forbidden:
            await ctx.send(channel, 
                ":no_entry: **I'm not allowed to send embeds here.**")

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def toggle(self, ctx):
        """Toggle ban checks on/off"""
        guild = ctx.message.guild
        if self.config.guild(guild).GUILD is None:
            return
        else:
            if await self.config.guild(guild).ENABLED():
                await self.config.guild(guild).ENABLED.set(False)
                await ctx.send("Bancheck is now Enabled.")
            else:
                await self.config.guild(guild).ENABLED.set(True)
                await ctx.send("Bancheck is now Disabled.")

    @bancheck.command(pass_context=True, name="search")
    async def _banlook(self, ctx, user:discord.Member=None):
        """Check if user is on the discordlists ban list."""
        if not user:
            return await ctx.send(embed=self.embed_maker("No User/ID found, did you forget to mention one?", 0x000000, None))
        checkID = user.id
        output = dBans.lookup(id=checkID)
        if output == True:
            print("User is in the banlist.")
            return await ctx.send(embed=self.embed_maker("Ban(s) Found!", 0xFF0000, None))
        if output == False:
            print("User is not in the banlist.")
            return await ctx.send(embed=self.embed_maker("No ban found", 0x008000, None))
        

    async def _banjoin(self, member):
        guild = member.guild
        enabled = await self.config.guild(guild).ENABLED()
        checkID = member
        output = dBans.lookup(id=checkID)
        channel_id = await self.config.guild(member.guild).channel()
        channel = self.bot.get_channel(channel_id)
        if enabled:
           return
        if output == False:
            return await channel.send(embed=self.embed_maker("Ban's Found! For more info and evidence check http://bans.discordlist.net",0xFF0000,'**Name:** {}\n**ID: **{}'.format(member.display_name, member.id)))
        if output == True:
            return await channel.send(embed=self.embed_maker("No ban found",0x008000,'**Name:** {}\n**ID: **{}'.format(member.display_name, member.id)))