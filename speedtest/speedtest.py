from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
import discord
import asyncio
import re
import os
import subprocess
import datetime

try:
    import speedtest
    module_avail = True
except ImportError:
    module_avail = False

BaseCog = getattr(commands, "Cog", object)

class Speedtest(BaseCog):
    """Speedtest for your bot's server"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 24341100993)
        self.direct = "data/speedtest/settings.json"
        self.users = {}
        self.messages = {}

    def speed_test(self):
        return str(subprocess.check_output(['speedtest-cli'], stderr=subprocess.STDOUT))

    @commands.command(no_pm=False)
    @checks.is_owner()
    async def speedtest(self, ctx):
        try:
            channel = ctx.message.channel
            author = ctx.message.author
            user = author
            now = datetime.datetime.now()
            message12 = await ctx.send(" :stopwatch: **Running speedtest. This may take a while!** :stopwatch:")
            DOWNLOAD_RE = re.compile(r"Download: ([\d.]+) .bit")
            UPLOAD_RE = re.compile(r"Upload: ([\d.]+) .bit")
            PING_RE = re.compile(r"([\d.]+) ms")
            speedtest_result = await self.bot.loop.run_in_executor(None, self.speed_test)
            download = float(DOWNLOAD_RE.search(speedtest_result).group(1))
            upload = float(UPLOAD_RE.search(speedtest_result).group(1))
            ping = float(PING_RE.search(speedtest_result).group(1))
            message = 'Your speedtest results are:'
            message_down = '**{}** mbps'.format(download)
            message_up = '**{}** mbps'.format(upload)
            message_ping = '**{}** ms'.format(ping)
            colour = 0x45FF00
            embed = discord.Embed(colour=colour, description=message)
            embed.title = 'Speedtest Results'
            embed.add_field(name='Download', value=message_down)
            embed.add_field(name=' Upload', value=message_up)
            embed.add_field(name=' Ping', value=message_ping)
            embed.set_footer(text= now.strftime("%Y-%m-%d %H:%M"))
            await ctx.send(embed=embed)
        except KeyError:
            print("An error occured")

    if module_avail == False:
        ctx.send("You currently don't have speedtest-cli installed, you need to run `pip install speedtest-cli`");
        raise RuntimeError("You need to run `pip3 install speedtest-cli`")
