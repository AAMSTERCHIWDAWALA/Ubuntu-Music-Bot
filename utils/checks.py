from __future__ import annotations

from discord.ext import commands
from core import Context

async def check_permissions(ctx: Context, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(
        getattr(resolved, name, None) == value
        for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def pred(ctx: Context):
        return await check_permissions(ctx, perms, check=check)

    return commands.check(pred)


async def check_guild_permissions(ctx: Context, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions
    return check(
        getattr(resolved, name, None) == value
        for name, value in perms.items())


def dj_or_permissions(**perms):
    perms['manage_channels'] = True

    async def predicate(ctx: Context):
        has_perms = await check_guild_permissions(ctx, perms, check=any)
        if has_perms:
            return True
        else:
          return False
    return commands.check(predicate)


def admin_or_permissions(**perms):
    perms['administrator'] = True

    async def predicate(ctx: Context):
        return await check_guild_permissions(ctx, perms, check=any)

    return commands.check(predicate)
