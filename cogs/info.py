import discord
from discord.ext import commands
import time

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.start = time.time()

    @commands.command(name="ping")
    async def cmd_ping(self, ctx):
        e = discord.Embed(title="🏓 Pong!",
                          description=f"Bot latency: {round(self.bot.latency * 1000, 2)} ms")
        await ctx.send(embed=e)

    @commands.command(name="uptime")
    async def cmd_uptime(self, ctx):
        uptime = int(time.time() - self.start)
        s = uptime
        d = int(s / (24 * 60 * 60))
        s -= d * 24 * 60 * 60
        h = int(s / (60 * 60))
        s -= d * 60 * 60
        m = int(s / 60)
        s -= m * 60
        await ctx.send(f"The bot has been up for {d} days, {h} hours, {m} minutes, and {s} seconds.")

def setup(bot):
    bot.add_cog(Info(bot))
