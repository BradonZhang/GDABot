import discord
from discord.ext import commands
import asyncio
import random
from youtube_dl import YoutubeDL
from functools import partial

ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": f"downloads/Dive.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": True,#False,
    "quiet": False,#True,
    "no_warnings": False,#True,
    "default_search": "auto",
    "source_address": "0.0.0.0"  # ipv6 addresses cause issues sometimes
}
ffmpegopts = {
    "before_options": "-nostdin",
    "options": "-vn"
}
ytdl = YoutubeDL(ytdlopts)

class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.uh_counter = 0

    @commands.command(name="test")
    async def cmd_test(self, ctx):
        await ctx.send("Test!")

    @commands.command(name="alan")
    async def cmd_alan(self, ctx):
        await ctx.send("Alan Dai? More like Alan _Night_, **amirite???!?1?**")

    @commands.command(name="mercy")
    async def cmd_mercy(self, ctx):
        await ctx.send("Alan Dai? Heroes never dai! (Now promoted to Alan Live)")

    @commands.command(name="coinflip", aliases=["coin", "flip"])
    async def cmd_coin(self, ctx):
        if bool(random.getrandbits(1)): # Random True or False
            await ctx.send("Heads!")
        else:
            await ctx.send("Tails!")

    @commands.command(name="asldgkjf")
    async def cmd_asldgkjf(self, ctx):
        uh = "u" + "".join(["h" for i in range(self.uh_counter)])
        self.uh_counter += 1
        await ctx.send(uh[:2000])

    @commands.command(name="dive", hidden=True)
    async def cmd_dive(self, ctx):
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return
        vc = ctx.voice_client
        if vc:
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                return
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                return
        loop = self.bot.loop
        dive_url = "https://soundcloud.com/alan-dai-4/dive"
        to_run = partial(ytdl.extract_info, url=dive_url, download=True)
        try:
            data = await loop.run_in_executor(None, to_run)
        except:
            return
        if "entries" in data:
            data = data["entries"][0]
        source = ytdl.prepare_filename(data)
        def dc():
            coro = ctx.voice_client.disconnect()
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except:
                pass
        ctx.voice_client.play(discord.FFmpegPCMAudio(source), after=dc)
        # TODO: get disconnect to work

def setup(bot):
    bot.add_cog(Test(bot))
