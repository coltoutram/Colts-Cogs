import discord
from discord.ext import commands
import aiohttp
import re
import os
from redbot.core import checks
from __main__ import send_cmd_help
#from .utils.dataIO import dataIO
from redbot.core import Config

URL = "https://bans.discordlist.net/api"
DEFAULT = {
"toggle" : True,
"channel" : None,
"ban" : False} # will add another day

class BanList():

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/bancheck/settings.json')

    async def save_settings(self):
        dataIO.save_json('data/bancheck/settings.json', self.settings)

    async def _check_files_(self, ctx):
        guild = ctx.message.guild
        if guild.id not in self.settings:
            self.settings[guild.id] = DEFAULT
            await self.save_settings()


    def embed_maker(self, title, color, description, avatar):
        embed=discord.Embed(title=title, color=color, description=description)
        embed.set_thumbnail(url=avatar)
        return embed

    def payload(self, user):
        passthis = {
        "token": "X9i69SJRQf",
        "userid": user,
        "version": 3}
        return passthis
   
    def cleanurl(self, tag):
        re1='.*?'
        re2='((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(tag)
        if m:
            theurl=m.group(1)
            return theurl

    async def lookup(self, user):
        resp = await aiohttp.post(URL, data=self.payload(user))
        final = await resp.json()
        resp.close()
        return final

    @checks.admin_or_permissions(manager_server=True)
    @commands.group(pass_context=True)
    async def bancheck(self, ctx):
        """Check new users against a ban list."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def channel(self, ctx, channel:discord.Channel=None):
        """Set the channel you want members to welcomed in"""
        await self._check_files_(ctx)
        if channel is None:
            channel = ctx.message.channel
        self.settings[ctx.message.guild.id]["channel"] = channel.id
        await self.save_settings()
        channel =  self.bot.get_channel(self.settings[ctx.message.guild.id]["channel"])
        try:
            await self.bot.send_message(channel,
                embed=self.embed_maker(None ,0x008000,
                    ':white_check_mark: **I will send all ban check notices here.**', avatar=self.bot.user.avatar_url))
        except discord.errors.Forbidden:
            await self.bot.send_message(channel, 
                ":no_entry: **I'm not allowed to send embeds here.**")

    @checks.admin_or_permissions(manager_server=True)
    @bancheck.command(pass_context=True)
    async def toggle(self, ctx):
        """Toggle ban checks on/off"""
        await self._check_files_(ctx)
        guild = ctx.message.guild.id
        toggle = self.settings[guild]['toggle']
        if toggle:
            self.settings[guild]['toggle'] = False
            await self.save_settings()
            return await ctx.send("Ban checks disabled.")
        else:
            self.settings[guild]['toggle'] = True
            await self.save_settings()
            return await ctx.send('Ban checks enabled.')


    @bancheck.command(pass_context=True, name="search")
    async def _banlook(self, ctx, user=None):
        """Check if user is on the discordlists ban list."""
        await self._check_files_(ctx)
        if not user:
            user = ctx.message.author.id
        
        avatar = discord.utils.get(ctx.message.guild.members, id=user).avatar_url

        try:
            final = await self.lookup(user)
        except ValueError:
            return await ctx.send(embed=self.embed_maker("No ban found", 0x008000, None, avatar))
        name = (final[1].replace("<Aspect>", ""))
        userid = final[2]
        reason = final[3]
        proof = self.cleanurl(final[4])
        niceurl = "[Click Here]({})".format(proof)

        description = (
            """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                name, userid, reason, niceurl))

        await ctx.send(embed=self.embed_maker("Ban Found", ctx.message.author.color, description, avatar))


    async def _banjoin(self, member):
        
        guild = member.guild
        toggle = self.settings[guild.id]['toggle']
        if not toggle:
            return
        channel = self.bot.get_channel(self.settings[guild.id]['channel'])
        try:
            final = await self.lookup(member)
        except ValueError:
            await self.bot.send_message(channel, embed=self.embed_maker(
                "No ban found",
                0x008000,
                '**Name:** {}\n**ID: **{}'.format(member.display_name, member.id),
                member.avatar_url))
            return
        name = (final[1].replace("<Aspect>", ""))
        userid = final[2]
        reason = final[3]
        proof = self.cleanurl(final[4])
        niceurl = "[Click Here]({})".format(proof)

        description = (
            """**Name:** {}\n**ID:** {}\n**Reason:** {}\n**Proof:** {}""".format(
                name, userid, reason, niceurl))

        await self.bot.send_message(channel,
            embed=self.embed_maker("Ban Found", 0xff0000, description, member.avatar_url))

def check_folder():
    if not os.path.exists('data/bancheck'):
        os.makedirs('data/bancheck')

def check_files():
    if not os.path.exists("data/bancheck/settings.json"):
        print("Creating empty settings.json...")
        data = {}
        dataIO.save_json("data/bancheck/settings.json", data)

def setup(bot):
    n = BanList(bot)
    bot.add_listener(n._banjoin,"on_member_join")
    bot.add_cog(n)
