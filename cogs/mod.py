import discord
from discord.ext import commands
import perms

class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.check(perms.can_manage_messages)
    async def cmd_purge(self, ctx, count=1):
        try:
            count = int(count)
        except ValueError:
            count = 1
        if count <= 0 and count > 100:
            text = f"{ctx.author.mention} You may only purge between 1 and 100 messages."
            await ctx.send(text)
            return
        await ctx.channel.purge(limit=count + 1) # +1 to delete the command message
        s = "s"
        if count == 1:
            s = ""
        await ctx.send(f"**Successfully deleted {count} message{s}.**", delete_after=3.0)

def setup(bot):
    bot.add_cog(Mod(bot))
