from __future__ import annotations

from core import Bot

from .music import Music
from .meta import Meta
from .config import Config

def setup(bot: Bot):
    bot.add_cog(Music(bot))
    bot.add_cog(Meta(bot))
    bot.add_cog(Config(bot))