import discord
from discord.ext import commands
import json
import constants
import perms

class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roleoption", aliases=["roleopt", "roleadd", "addrole"])
    @commands.check(perms.can_manage_roles)
    async def cmd_roleoption(self, ctx, *, arg):
        mentions = ctx.message.role_mentions
        if len(mentions) == 0:
            await ctx.send(f"{ctx.author.mention} You must mention the role you want to poll!")
            return
        role = mentions[0]
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass
        if arg.strip() == role.mention:
            arg = f"React ✅ to this message to be added to {role.mention}!"
        message = await ctx.send(arg)
        await message.add_reaction("✅")
        constants.role_messages[str(message.id)] = role.id
        with open("data/roles.json", "w") as f:
            json.dump(constants.role_messages, f, indent=4)

def setup(bot):
    bot.add_cog(Roles(bot))
