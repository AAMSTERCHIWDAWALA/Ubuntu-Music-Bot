from __future__ import annotations

import discord
from discord.ext import commands

from core import Cog, Bot, Context


class Config(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_join(self, guild: discord.Guild):
        """To put SQL Values"""
        if not guild: return
        await self.bot.db.on_join(guild.id)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        self.bot._24_7.discard(channel.id)
        self.bot._specific.discard(channel.id)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx: Context, *, prefix: str):
        """To set the prefix of the bot"""
        await self.bot.db.update_prefix(ctx.guild.id, prefix)
        await ctx.send(f"{ctx.author.mention} prefix for server **{ctx.guild.name}** is set to **{prefix}**")

    @commands.command(name='247', aliases=['24/7'])
    @commands.has_permissions(manage_guild=True)
    async def _247(self, ctx: Context, *, channel: discord.VoiceChannel=None):
        """To set 24/7 VC channel"""
        await self.bot.db.update_247(ctx.guild.id, channel.id if channel else None)
        await ctx.send(f"{ctx.author.mention} 24/7 channel is being set to **{channel.mention if channel else None}**")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setchannel(self, ctx: Context, *, channel: discord.TextChannel=None):
        """To set the one specific VC channel for the bot. If set so, the bot won't join any other channel"""
        await self.bot.db.update_specific(ctx.guild.id, channel.id if channel else None)
        await ctx.send(f"{ctx.author.mention} all commands will now work in **{channel.mention if channel else None}**")