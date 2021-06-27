import discord
from discord.ext import commands

def get_perms(ctx):
    return ctx.author.permissions_in(ctx.channel)

def is_admin(ctx):
    return get_perms(ctx).administrator

def can_manage_messages(ctx):
    return get_perms(ctx).manage_messages

def can_manage_roles(ctx):
    return get_perms(ctx).manage_roles
