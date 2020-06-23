from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
import datetime
import discord
import asyncio
import os
from random import choice, randint
from enum import Enum


inv_settings = {"Channel": None, "toggleedit": False, "toggledelete": False, "toggleuser": False,
                "toggleroles": False,
                "togglevoice": False,
                "toggleban": False, "togglejoin": False, "toggleleave": False, "togglechannel": False,
                "toggleguild": False, "toggleunban": False,}

BaseCog = getattr(commands, "Cog", object)

class Actionlogs(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.direct = "data/actionlogset/settings.json"
        self.config = Config.get_conf(self, 2463123480)
        self.config.register_guild(**inv_settings)

    @checks.admin_or_permissions(administrator=True)
    @commands.group(name='actionlogtoggle', pass_context=True, no_pm=True)
    async def actionlogtoggles(self, ctx):
        """toggle which guild activity to log"""
        if await self.config.guild(ctx.message.guild).settings() == {}:
            await self.config.guild(ctx.message.guild).set(inv_settings)
        if ctx.invoked_subcommand is None:
            guild = ctx.message.guild
            
            await ctx.send_help()
            try:
                e = discord.Embed(title="Setting for {}".format(guild.name), colour=discord.Colour.blue())
                e.description = "actionlogs channel set to {}".format(self.bot.get_channel(id=await self.config.guild(guild).Channel()))
                e.add_field(name="Delete", value=str(await self.config.guild(guild).toggledelete()))
                e.add_field(name="Edit", value=str(await self.config.guild(guild).toggleedit()))
                e.add_field(name="Roles", value=str(await self.config.guild(guild).toggleroles()))
                e.add_field(name="User", value=str(await self.config.guild(guild).toggleuser()))
                e.add_field(name="Voice", value=str(await self.config.guild(guild).togglevoice()))
                e.add_field(name="Ban", value=str(await self.config.guild(guild).toggleban()))
                e.add_field(name="Join", value=str(await self.config.guild(guild).togglejoin()))
                e.add_field(name="Leave", value=str(await self.config.guild(guild).toggleleave()))
                e.add_field(name="Channel", value=str(await self.config.guild(guild).togglechannel()))
                e.add_field(name="guild", value=str(await self.config.guild(guild).toggleguild()))
                e.add_field(name="Unban", value=str(await self.config.guild(guild).toggleunban()))
                e.set_thumbnail(url=guild.icon_url)
                await ctx.send(embed=e)
            except KeyError:
                return

    @checks.admin_or_permissions(administrator=True)
    @commands.group(pass_context=True, no_pm=True)
    async def actionlogset(self, ctx):
        """Change actionlogs settings"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @actionlogset.command(name='channel', pass_context=True, no_pm=True)
    async def _channel(self, ctx):
        """Set the channel to send notifications too"""
        guild = ctx.message.guild
        if ctx.message.guild.me.permissions_in(ctx.message.channel).send_messages:
            if await self.config.guild(guild).Channel() is not None:
                await self.config.guild(guild).Channel.set(ctx.message.channel.id)
                await ctx.send("Channel changed.")
                return
            else:
                await self.config.guild(guild).Channel.set(ctx.message.channel.id)
                await ctx.send("I will now send toggled actionlogs notifications here")
        else:
            return

    @actionlogset.command(pass_context=True, no_pm=True)
    async def disable(self, ctx):
        """disables the actionlogs"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).Channel() is None:
            await ctx.send("guild not found, use actionlogset to set a channnel")
            return
        await self.config.guild(guild).Channel.set(None)
        
        await ctx.send("I will no longer send actionlogs notifications here")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def edit(self, ctx):
        """toggle notifications when a member edits theyre message"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleedit() == False:
            await self.config.guild(guild).toggleedit.set(True)
            
            await ctx.send("Edit messages enabled")
        elif await self.config.guild(guild).toggleedit() == True:
            await self.config.guild(guild).toggleedit.set(False)
            
            await ctx.send("Edit messages disabled")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        """toggles notofications when a member joins the guild."""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).togglejoin() == False:
            await self.config.guild(guild).togglejoin.set(True)
            
            await ctx.send("Enabled join logs.")
        elif await self.config.guild(guild).togglejoin() == True:
            await self.config.guild(guild).togglejoin.set(False)
            
            await ctx.send("Disabled join logs.")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def guild(self, ctx):
        """toggles notofications when the guild updates."""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleguild() == False:
            await self.config.guild(guild).toggleguild.set(True)
            
            await ctx.send("Enabled guild logs.")
        elif await self.config.guild(guild).toggleguild() == True:
            await self.config.guild(guild).toggleguild.set(False)
            
            await ctx.send("Disabled guild logs.")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def channel(self, ctx):
        """toggles channel update logging for the guild."""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).togglechannel() == False:
            await self.config.guild(guild).togglechannel.set(True)
            
            await ctx.send("Enabled channel logs.")
        elif await self.config.guild(guild).togglechannel() == True:
            await self.config.guild(guild).togglechannel.set(False)
            
            await ctx.send("Disabled channel logs.")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def leave(self, ctx):
        """toggles notofications when a member leaves the guild."""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleleave() == False:
            await self.config.guild(guild).toggleleave.set(True)
            
            await ctx.send("Enabled leave logs.")
        elif await self.config.guild(guild).toggleleave() == True:
            await self.config.guild(guild).toggleleave.set(False)
            
            await ctx.send("Disabled leave logs.")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def delete(self, ctx):
        """toggle notifications when a member delete theyre message"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggledelete() == False:
            await self.config.guild(guild).toggledelete.set(True)
            
            await ctx.send("Delete messages enabled")
        elif await self.config.guild(guild).toggledelete() == True:
            await self.config.guild(guild).toggledelete.set(False)
            
            await ctx.send("Delete messages disabled")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def user(self, ctx):
        """toggle notifications when a user changes his profile"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleuser() == False:
            await self.config.guild(guild).toggleuser.set(True)
            
            await ctx.send("User messages enabled")
        elif await self.config.guild(guild).toggleuser() == True:
            await self.config.guild(guild).toggleuser.set(False)
            
            await ctx.send("User messages disabled")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def roles(self, ctx):
        """toggle notifications when roles change"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleroles() == False:
            await self.config.guild(guild).toggleroles.set(True)
            await ctx.send("Role messages enabled")
        elif await self.config.guild(guild).toggleroles() == True:
            await self.config.guild(guild).toggleroles.set(False)
            await ctx.send("Role messages disabled")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def voice(self, ctx):
        """toggle notifications when voice status change"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).togglevoice() == False:
            await self.config.guild(guild).togglevoice.set(True)
            await ctx.send("Voice messages enabled")
        elif await self.config.guild(guild).togglevoice() == True:
            await self.config.guild(guild).togglevoice.set(False)
            await ctx.send("Voice messages disabled")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def ban(self, ctx):
        """toggle notifications when a user is banned"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleban() == False:
            await self.config.guild(guild).toggleban.set(True)
            
            await ctx.send("Ban messages enabled")
        elif await self.config.guild(guild).toggleban() == True:
            await self.config.guild(guild).toggleban.set(False)
            
            await ctx.send("Ban messages disabled")

    @actionlogtoggles.command(pass_context=True, no_pm=True)
    async def unban(self, ctx):
        """toggle notifications when a user is unbanned"""
        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleunban() == False:
            await self.config.guild(guild).toggleunban.set(True)
            
            await ctx.send("Ban messages enabled")
        elif await self.config.guild(guild).toggleunban() == True:
            await self.config.guild(guild).toggleunban.set(False)
            
            await ctx.send("Unban messages disabled")

    async def on_message_delete(self, message):
        guild = message.guild
        if await self.config.guild(guild).Channel() is None:
            return
        if await self.config.guild(guild).toggledelete() == False:
            return
        if message.author is message.author.bot:
            pass
        channel = await self.config.guild(guild).Channel()
        time = datetime.datetime.utcnow()
        cleanmsg = message.content
        for i in message.mentions:
            cleanmsg = cleanmsg.replace(i.mention, str(i))
        fmt = '%H:%M:%S'
        if channel is None:
            return
        else:
            name = message.author
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            infomessage = "A message by {}, was deleted in {}".format(message.author.mention, message.channel.mention)
            delmessage = discord.Embed(description=infomessage, colour=discord.Color.purple(), timestamp=time)
            delmessage.add_field(name="Message:", value=cleanmsg)
            delmessage.set_footer(text="User ID: {}".format(message.author.id), icon_url=message.author.avatar_url)
            delmessage.set_author(name=name + " - Deleted Message", url="http://i.imgur.com/fJpAFgN.png", icon_url=message.author.avatar_url)
            delmessage.set_thumbnail(url="http://i.imgur.com/fJpAFgN.png")
            try:
                await guild.get_channel(channel).send(embed=delmessage)
            except:
                pass


    async def on_message_edit(self, before, after):
        guild = before.guild
        if before.author.bot:
            return
        if await self.config.guild(guild).toggleedit() == False:
            return
        if before.content == after.content:
            return
        cleanbefore = before.content
        for i in before.mentions:
            cleanbefore = cleanbefore.replace(i.mention, str(i))
        cleanafter = after.content
        for i in after.mentions:
            cleanafter = cleanafter.replace(i.mention, str(i))
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        name = before.author
        name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
        infomessage = "A message by {}, was edited in {}".format(before.author.mention, before.channel.mention)
        delmessage = discord.Embed(description=infomessage, colour=discord.Color.blue(), timestamp=after.created_at)
        delmessage.add_field(name="Before Message:", value=cleanbefore, inline=False)
        delmessage.add_field(name="After Message:", value=cleanafter)
        delmessage.set_footer(text="User ID: {}".format(before.author.id), icon_url=before.author.avatar_url)
        delmessage.set_author(name=name + " - Edited Message", url="http://i.imgur.com/Q8SzUdG.png", icon_url=before.author.avatar_url)
        delmessage.set_thumbnail(url="https://i.colt.ws/edit-blue.png")
        try:
            await guild.get_channel(channel).send(embed=delmessage)
        except:
            pass


    async def on_member_join(self, member):
        guild = member.guild
        
        if await self.config.guild(guild).togglejoin() == False:
            return
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        users = len([e.name for e in guild.members])
        name = member
        joinmsg = discord.Embed(description=member.mention, colour=discord.Color.green(), timestamp=member.joined_at)
        infomessage = "Total Users: {}".format(users)
        joinmsg.add_field(name="Total Users:", value=str(users), inline=True)
        joinmsg.set_footer(text="User ID: {}".format(member.id), icon_url=member.avatar_url)
        joinmsg.set_author(name=name.display_name + " has joined the guild",url=member.avatar_url, icon_url=member.avatar_url)
        joinmsg.set_thumbnail(url=member.avatar_url)
        try:
            await guild.get_channel(channel).send(embed=joinmsg)
        except:
            pass


    async def on_member_remove(self, member):
        guild = member.guild

        if await self.config.guild(guild).toggleleave() == False:
            return
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = "%H:%M:%S"
        users = len([e.name for e in guild.members])
        name = member
        joinmsg = discord.Embed(description=member.mention, colour=discord.Color.red(), timestamp=time)
        infomessage = "Total Users: {}".format(users)
        joinmsg.add_field(name="Total Users:", value=str(users), inline=True)
        joinmsg.set_footer(text="User ID: {}".format(member.id), icon_url=member.avatar_url)
        joinmsg.set_author(name=name.display_name + " has left the guild",url=member.avatar_url, icon_url=member.avatar_url)
        joinmsg.set_thumbnail(url=member.avatar_url)
        try:
            await guild.get_channel(channel).send(embed=joinmsg)
        except:
            pass


    async def on_guild_channel_update(self, before, after):
        guild = before.guild
        if await self.config.guild(guild).togglechannel() == False:
            return  
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return   
        time = datetime.datetime.utcnow()
        fmt = "%H:%M:%S"
        msg = ""
        if before.name != after.name:
            fmt = "%H:%M:%S"
            name = discord.Embed(colour=discord.Color.blue(), timestamp=time)
            infomessage = "Channel name update. Before: **{}** After: **{}**.".format(
                before.name, after.name)
            name.add_field(name="Info:", value=infomessage, inline=False)
            name.set_author(name=time.strftime(fmt) + " - Channel Update")
            name.set_thumbnail(url="https://i.colt.ws/edit-blue.png")
            try:
                await guild.get_channel(channel).send(embed=name)
            except:
                pass

              
    async def on_guild_update(self, before, after):
        guild = before
        if await self.config.guild(guild).toggleguild() == False:
            return
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        if before.name != after.name:
            msg = ":globe_with_meridians: `{}` guild name update. Before: **{}** After: **{}**.".format(
                time.strftime(fmt), before.name, after.name)
        if before.region != after.region:
            msg = ":globe_with_meridians: `{}` guild region update. Before: **{}** After: **{}**.".format(
                time.strftime(fmt), before.region, after.region)
        await guild.get_channel(channel).send(msg)

    async def on_voice_state_update(self, member, before, after):
        try:
            guild = before.channel.guild
        except:
            guild = after.channel.guild

        if await self.config.guild(guild).togglevoice() == False:
            return
        if member.bot:
            return
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        if before.channel == after.channel:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        if before.channel is None:
            name = member
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            updmessage = discord.Embed(description=name, colour=discord.Color.blue(), timestamp=time)
            updmessage.add_field(name="User has joined voice channel:", value=after.channel)
            updmessage.set_footer(text="User ID: {}".format(member.id))
            updmessage.set_author(name=time.strftime(fmt) + " - Voice Channel Changed",
                                url="http://i.imgur.com/8gD34rt.png")
            updmessage.set_thumbnail(url="https://i.colt.ws/speaker-light-blue.png") # https://colt.ws/credits.txt
            try:
                return await guild.get_channel(channel).send(embed=updmessage)
            except:
                pass

        elif after.channel is None:
            name = member
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            updmessage = discord.Embed(description=name, colour=discord.Color.blue(), timestamp=time)
            updmessage.add_field(name="User has left voice channel:", value=before.channel)
            updmessage.set_footer(text="User ID: {}".format(member.id))
            updmessage.set_author(name=time.strftime(fmt) + " - Voice Channel Changed",
                                url="http://i.imgur.com/8gD34rt.png")
            updmessage.set_thumbnail(url="https://i.colt.ws/speaker-light-blue.png") # https://colt.ws/credits.txt
            try:
                return await guild.get_channel(channel).send(embed=updmessage)
            except:
                pass
        else:
            name = member
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            updmessage = discord.Embed(description=name, colour=discord.Color.blue(), timestamp=time)
            updmessage.add_field(name="Changed to voice channel:", value=after.channel)
            updmessage.set_footer(text="User ID: {}".format(member.id))
            updmessage.set_author(name=time.strftime(fmt) + " - Voice Channel Changed",
                                url="http://i.imgur.com/8gD34rt.png")
            updmessage.set_thumbnail(url="https://i.colt.ws/speaker-light-blue.png") # https://colt.ws/credits.txt
            try:
                await guild.get_channel(channel).send(embed=updmessage)
            except:
                pass


    async def on_member_update(self, before, after):
        guild = before.guild
        
        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        if not before.roles == after.roles and await self.config.guild(guild).toggleroles():
            name = after
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            role = discord.Embed(colour=discord.Color.orange(), timestamp=time)
            role.add_field(name="Roles Before:", value=" ,".join(role.name for role in before.roles), inline=False)
            role.add_field(name="Roles After:", value=" ,".join(role.name for role in after.roles), inline=False)
            role.set_footer(text="User ID: {}".format(after.id), icon_url=after.avatar_url)
            role.set_author(name=name + " - Updated Roles", icon_url=after.avatar_url)
            role.set_thumbnail(url="https://i.colt.ws/update-orange.png") # https://i.colt.ws/credits.txt
            try:
                await guild.get_channel(channel).send(embed=role)
            except:
                pass

        if not before.nick == after.nick and await self.config.guild(guild).toggleuser():
            name = before
            name = " ~ ".join((name.name, name.nick)) if name.nick else name.name
            infomessage = "{}'s nickname has changed".format(before.mention)
            updmessage = discord.Embed(description=infomessage, colour=discord.Color.blue(), timestamp=time)
            updmessage.add_field(name="Nickname Before:", value=before.nick)
            updmessage.add_field(name="Nickname After:", value=after.nick)
            updmessage.set_footer(text="User ID: {}".format(before.id), icon_url=after.avatar_url)
            updmessage.set_author(name=name + " - Nickname Changed", icon_url=after.avatar_url)
            updmessage.set_thumbnail(url="http://i.imgur.com/I5q71rj.png")
            try:
                await guild.get_channel(channel).send(embed=updmessage)
            except:
                pass

    async def on_member_ban(self, guild, member):

        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        name = member
        infomessage = "{} has been banned from the guild.".format(member.mention)
        banmessage = discord.Embed(description=infomessage, colour=discord.Color.red(), timestamp=time)
        banmessage.add_field(name="Info:", value=infomessage, inline=False)
        banmessage.set_footer(text="User ID: {}".format(member.id), icon_url=member.avatar_url)
        banmessage.set_author(name=name, icon_url=member.avatar_url)
        banmessage.set_thumbnail(url=member.avatar_url)
        try:
            await guild.get_channel(channel).send(embed=banmessage)
        except:
            await guild.get_channel(channel).send("How is embed actionlogs going to work when I don't have embed links permissions?")

    async def on_member_unban(self, guild, member):

        channel = await self.config.guild(guild).Channel()
        if channel is None:
            return
        time = datetime.datetime.utcnow()
        fmt = '%H:%M:%S'
        name = member
        infomessage = "{} has been unbanned from the guild.".format(member.mention)
        unbanmessage = discord.Embed(description=infomessage, colour=discord.Color.green(), timestamp=time)
        unbanmessage.add_field(name="Info:", value=infomessage, inline=False)
        unbanmessage.set_footer(text="User ID: {}".format(member.id), icon_url=member.avatar_url)
        unbanmessage.set_author(name=name, icon_url=member.avatar_url)
        unbanmessage.set_thumbnail(url=member.avatar_url)
        try:
            await guild.get_channel(channel).send(embed=unbanmessage)
        except:
            await guild.get_channel(channel).send("How is embed actionlogs going to work when I don't have embed links permissions?")

    @actionlogset.command(name='toggleall', pass_context=True, no_pm=True)
    async def toggleall(self, ctx):
        """Toggles all settings."""

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleedit() == False:
            await self.config.guild(guild).toggleedit.set(True)
            
            await ctx.send("Edit messages enabled")
        elif await self.config.guild(guild).toggleedit() == True:
            await self.config.guild(guild).toggleedit.set(False)
            
            await ctx.send("Edit messages disabled")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).togglejoin() == False:
            await self.config.guild(guild).togglejoin.set(True)
            
            await ctx.send("Enabled join logs.")
        elif await self.config.guild(guild).togglejoin() == True:
            await self.config.guild(guild).togglejoin.set(False)
            
            await ctx.send("Disabled join logs.")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleguild() == False:
            await self.config.guild(guild).toggleguild.set(True)
            
            await ctx.send("Enabled guild logs.")
        elif await self.config.guild(guild).toggleguild() == True:
            await self.config.guild(guild).toggleguild.set(False)
            
            await ctx.send("Disabled guild logs.")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).togglechannel() == False:
            await self.config.guild(guild).togglechannel.set(True)
            
            await ctx.send("Enabled channel logs.")
        elif await self.config.guild(guild).togglechannel() == True:
            await self.config.guild(guild).togglechannel.set(False)
            
            await ctx.send("Disabled channel logs.")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleleave() == False:
            await self.config.guild(guild).toggleleave.set(True)
            
            await ctx.send("Enabled leave logs.")
        elif await self.config.guild(guild).toggleleave() == True:
            await self.config.guild(guild).toggleleave.set(False)
            
            await ctx.send("Disabled leave logs.")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggledelete() == False:
            await self.config.guild(guild).toggledelete.set(True)
            
            await ctx.send("Delete messages enabled")
        elif await self.config.guild(guild).toggledelete() == True:
            await self.config.guild(guild).toggledelete.set(False)
            
            await ctx.send("Delete messages disabled")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleuser() == False:
            await self.config.guild(guild).toggleuser.set(True)
            
            await ctx.send("User messages enabled")
        elif await self.config.guild(guild).toggleuser() == True:
            await self.config.guild(guild).toggleuser.set(False)
            
            await ctx.send("User messages disabled")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleroles() == False:
            await self.config.guild(guild).toggleroles.set(True)
            await ctx.send("Role messages enabled")
        elif await self.config.guild(guild).toggleroles() == True:
            await self.config.guild(guild).toggleroles.set(False)
            await ctx.send("Role messages disabled")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).togglevoice() == False:
            await self.config.guild(guild).togglevoice.set(True)
            await ctx.send("Voice messages enabled")
        elif await self.config.guild(guild).togglevoice() == True:
            await self.config.guild(guild).togglevoice.set(False)
            await ctx.send("Voice messages disabled")

        guild = ctx.message.guild
        
        if await self.config.guild(guild).toggleban() == False:
            await self.config.guild(guild).toggleban.set(True)
            
            await ctx.send("Ban messages enabled")
        elif await self.config.guild(guild).toggleban() == True:
            await self.config.guild(guild).toggleban.set(False)
            
            await ctx.send("Ban messages disabled")

        if await self.config.guild(guild).toggleunban() == False:
            await self.config.guild(guild).toggleunban.set(True)
            
            await ctx.send("Unban messages enabled")
        elif await self.config.guild(guild).toggleunban() == True:
            await self.config.guild(guild).toggleunban.set(False)
            
            await ctx.send("Unban messages disabled")
