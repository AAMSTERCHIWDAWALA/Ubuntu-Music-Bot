from __future__ import annotations

import discord
from discord.ext import commands

import aiohttp, jishaku, os

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

from .Context import Context
from utils.db import Database


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            intent=discord.Intents.all(),
            status=discord.Status.dnd,
            strip_after_prefix=True,
            case_insensitive=True,
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name="RickRoll"),
        )
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self._seen_messages = 0
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.load_extension('jishaku')
        self.load_extension('cogs')
        self._internal_db = {}
        self._24_7 = set()
        self._specific = set()
        self.db = Database(self)

    async def on_ready(self):
        await self.db.load_all()
        if not hasattr(self, 'uptime'):
            self.uptime = discord.utils.utcnow()

        if self._24_7:
            for channel in self._24_7:
                vc = self.get_channel(channel)
                if not vc:
                    pass
                else:
                    try:
                        await vc.connect()
                    except Exception:
                        pass

        print(f'Ready: {self.user} (ID: {self.user.id})')

    def run(self):
        super().run(os.environ['TOKEN'], reconnect=True)

    async def process_commands(self, message: discord.Message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is None:
            # ignore if no command found
            return

        if self._specific:
          for channel in self._specific:
            ch = self.get_channel(channel)
            if not ch:
                return
            return await ctx.reply(
                f'{ctx.author.mention} `{ctx.command.qualified_name}` is being disabled in **#{ctx.channel.name}** by the staff!',
                delete_after=10.0)
            

        await self.invoke(ctx)

    async def on_message(self, message: discord.Message):
        self._seen_messages += 1

        if not message.guild:
            # to prevent the usage of command in DMs
            return

        await self.process_commands(message)

    async def get_prefix(self, message: discord.Message) -> str:
        """Dynamic prefixing"""
        if not self._internal_db:
            return commands.when_mentioned_or('>>')(self, message)
        else:
            try:
                prefix = self._internal_db[message.guild.id]
                return commands.when_mentioned_or(prefix)(self, message)
            except KeyError:
                return commands.when_mentioned_or('>>')(self, message)

    async def send_raw(self, channel_id: int, content: str, **kwargs):
        await self.http.send_message(channel_id, content, **kwargs)

    async def on_command_error(self, ctx: Context, error):
        """Error Handling"""
        if hasattr(ctx.command, 'on_error'): return

        # get the original exception
        error = getattr(error, 'original', error)

        ignore = (commands.CommandNotFound, discord.errors.NotFound,
                  discord.Forbidden)

        if isinstance(error, ignore): return

        await ctx.send(
            f"{ctx.author.mention} something not right: Error at {ctx.command.name}\n```py\n{error}```"
        )
