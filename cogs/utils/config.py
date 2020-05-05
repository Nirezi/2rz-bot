import json
import asyncio


class Config:
    def __init__(self, name):
        self.name = name
        self.loop = asyncio.get_event_loop()
        self.lock = asyncio.Lock()
        self.file = {}
        self.load_file()

    def _dump(self):
        with open(self.name, 'w', encoding='utf-8') as tmp:
            json.dump(self.file.copy(), self.name, ensure_ascii=True, indent=4, separators=(',', ':'))

    def load_file(self):
        try:
            with open(self.name, 'r') as f:
                self.file = json.load(f)
        except FileNotFoundError:
            pass

    async def save(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self._dump)

    async def set_guild_prefix(self, guild_id, prefix):
        self.file[str(guild_id)] = prefix
        await self.save()

    async def put(self, key, value):
        self.file[str(key)] = value
        await self.save()

    async def remove(self, key):
        del self.file[str(key)]
        await self.save()

    def get(self, key, *args):
        return self.file.get(key, *args)

