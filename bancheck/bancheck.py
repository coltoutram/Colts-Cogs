import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from dbans import DBans

dBans = DBans(token="TKDcIwZaeb")
DEFAULT = {
"ENABLED" : True,
"guild" : None}


class BanList():

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 54564894107)
        self.config.register_guild(**{"ENABLED":True})
        self.users = {}
        self.messages = {}

    async def __local_check(self, ctx):
        return False
    
    @checks.admin_or_permissions(manager_server=True)
    @commands.group(pass_context=True)
    async def bancheck(self, ctx):
        """Check if users are banned on bans.discordlist.com"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def channel(self, ctx, channel:discord.TextChannel=None):
        """Set the channel you want members to welcomed in"""
        if channel is None:
            channel = ctx.message.channel
        await self.config.guild(ctx.guild).channel.set(channel.id)
        try:
                infomessage = "Channel has been set to {}".format(channel.mention)
                e = discord.Embed(title="Channel Successfully Set!", colour=discord.Colour.green())
                e.description = "Successfully changed bancheck channel."
                e.add_field(name="Information:", value=infomessage, inline=False)
                e.set_footer(text="Channel ID: {}".format(channel.id))
                e.set_thumbnail(url="http://i.colt.ws/green-tick.png")
                return await ctx.send(embed=e)
                                  
        except discord.errors.Forbidden:
            await ctx.send(channel, 
                ":no_entry: **I'm not allowed to send embed links here.**")

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def toggle(self, ctx):
        """Toggle banchecks on new users on/off."""
        guild = ctx.message.guild
        if self.config.guild(guild).GUILD is None:
            return
        else:
            if await self.config.guild(guild).ENABLED():
                await self.config.guild(guild).ENABLED.set(False)
                await ctx.send("Bancheck is now enabled.")
            else:
                await self.config.guild(guild).ENABLED.set(True)
                await ctx.send("Bancheck is now disabled.")

    @bancheck.command(pass_context=True, name="search")
    async def _banlook(self, ctx, user:discord.Member=None):
        """Check if user is banned on bans.discordlist.com"""
        if not user:
            e = discord.Embed(title="No User/ID found. Did you forgot to mention one?", colour=discord.Colour.red())
            return await ctx.send(embed=e)
        checkID = user.id
        name = user
        avatar = user
        is_banned = await dBans.lookup(user_id=checkID)
        name = user
        avatar = user.avatar_url_as(format='png')
        if is_banned:
            try:
                infomessage = "This user has one or more registered bans which means he participated in an illegal activity, raiding or spamming of servers. Proceed with caution."
                e = discord.Embed(title="Ban's Found!", colour=discord.Colour.red())
                e.description = "For proof and more info go to http://bans.discordlist.net"
                e.add_field(name="Information:", value=infomessage, inline=False)
                e.set_author(name=name, icon_url=avatar)
                e.set_footer(text="User ID: {}".format(user.id))
                e.set_thumbnail(url=avatar)
                return await ctx.send(embed=e)
            except KeyError:
                return
        try:
            infomessage = "This user has no registered bans but this doesn't mean he is harmless!"
            e = discord.Embed(title="No Ban's Found.", colour=discord.Colour.green())
            e.description = "For more info goto http://bans.discordlist.net"
            e.add_field(name="Information:", value=infomessage, inline=False)
            e.set_author(name=name, icon_url=avatar)
            e.set_footer(text="User ID: {}".format(user.id))
            e.set_thumbnail(url=avatar)
            return await ctx.send(embed=e)
        except KeyError:
            return
        

    async def _banjoin(self, member):
        guild = member.guild
        enabled = await self.config.guild(guild).ENABLED()
        checkID = member.id
        is_banned = await dBans.lookup(user_id=checkID)
        channel_id = await self.config.guild(member.guild).channel()
        channel = self.bot.get_channel(channel_id)
        name = member
        avatar = member.avatar_url_as(format='png')
        if not member:
            return await print("A member has joined but no User/ID was found.")
        if member.bot:
            return await print("A member has joined but it seems the member is a BOT.")
        if enabled:
            return
        if is_banned:
            try:
                infomessage = "This user has one or more registered bans which means he participated in an illegal activity, raiding or spamming of servers. Proceed with caution."
                e = discord.Embed(title="Ban's Found!", colour=discord.Colour.red())
                e.description = "For proof and more info go to http://bans.discordlist.net"
                e.add_field(name="Information:", value=infomessage, inline=False)
                e.set_author(name=name, icon_url=avatar)
                e.set_footer(text="User ID: {}".format(member.id))
                e.set_thumbnail(url=avatar)
                return await channel.send(embed=e)
            except KeyError:
                return
        try:
            infomessage = "This user has no registered bans but this doesn't mean he is harmless!"
            e = discord.Embed(title="No Ban's Found.", colour=discord.Colour.green())
            e.description = "For more info goto http://bans.discordlist.net"
            e.add_field(name="Information:", value=infomessage, inline=False)
            e.set_author(name=name, icon_url=avatar)
            e.set_footer(text="User ID: {}".format(member.id))
            e.set_thumbnail(url=avatar)
            return await channel.send(embed=e)
        except KeyError:
            return
