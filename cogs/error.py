import discord
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errors = {
            "purge": "You may not purge messages without the `Manage Messages` permission.",
            "roleoption": "You must have the `Manage Roles` permission to use roleoption."
        }

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if not isinstance(error, commands.errors.CheckFailure):
            raise error
        if ctx.command.name in self.errors:
            text = f"{ctx.author.mention} {self.errors[ctx.command.name]}"
            await ctx.send(text)

def setup(bot):
    bot.add_cog(Error(bot))
