from __future__ import annotations

from core import Bot
from aiofiles import open as op

import typing, json


class Database:
    def __init__(self, bot: Bot):
        self.bot = bot

    def clear(self) -> dict:
        self.bot._internal_db = {}
        return {}

    def put(self, key: str, value: typing.Any) -> None:
        self.bot._internal_db[key] = value

    def get(self, key: str) -> typing.Any:
        try:
            return self.bot._internal_db[key]
        except KeyError:
            return None

    def delete(self, key: str) -> None:
        try:
            del self.bot._internal_db[key]
        except KeyError:
            return None

    async def read(self) -> dict:
        async with op('utils/db.json', mode='r') as f:
            data = json.loads(await f.read())
        return data

    async def load(self) -> None:
        data = await self.read()
        self.put('data', data)

    async def load_prefix(self) -> None:
        data = await self.read()
        for temp in data:
            self.put(temp['guild_id'], temp['prefix'])

    async def load_channels(self) -> None:
        data = await self.read()
        for temp in data:
            if temp['247']:
                self.bot._24_7.add(temp['247'])
            if temp['specific']:
                self.bot._specific.add(temp['specific'])

    async def load_all(self) -> None:
        await self.load_channels()
        await self.load_prefix()

    async def update_prefix(self, guild_id: int, prefix: str) -> None:
        async with op(r'utils/db.json', mode='r') as f:
            data = json.loads(await f.read())

        for temp in data:
            print(temp['guild_id'])
            if temp['guild_id'] == guild_id:
                temp['prefix'] = prefix
                self.put(guild_id, prefix)

        json_obj = json.dumps(data, indent=4)

        async with op(r'utils/db.json', mode='w+') as f:
            await f.write(json_obj)

    async def on_join(self, guild_id: int):
        post = {
            'guild_id': guild_id,
            'prefix': ">>",
            '247': None,
            'specific': None
        }
        async with op(r'utils/db.json', mode='r') as f:
            data = json.loads(await f.read())
        data.append(post)

        json_obj = json.dumps(data, indent=4)

        async with op(r'utils/db.json', mode='w+') as f:
            data = f.write(json_obj)

    async def update_247(self, guild_id: int, channel: int) -> None:
        async with op(r'utils/db.json', mode='r') as f:
            data = json.loads(await f.read())

        for temp in data:
            print(temp['guild_id'])
            if temp['guild_id'] == guild_id:
                temp['247'] = channel
                self._24_7.add(channel)

        json_obj = json.dumps(data, indent=4)

        async with op(r'utils/db.json', mode='w+') as f:
            await f.write(json_obj)

    async def update_specific(self, guild_id: int, channel: int) -> None:
        async with op(r'utils/db.json', mode='r') as f:
            data = json.loads(await f.read())

        for temp in data:
            print(temp['guild_id'])
            if temp['guild_id'] == guild_id:
                temp['channel'] = channel
                self._specific.add(channel)

        json_obj = json.dumps(data, indent=4)

        async with op(r'utils/db.json', mode='w+') as f:
            await f.write(json_obj)
