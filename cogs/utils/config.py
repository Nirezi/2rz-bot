import json
import asyncio


class Config:
    def __init__(self, name):
        self.name = name
        self.loop = asyncio.get_event_loop()
        self.lock = asyncio.Lock()
        self._file = {}
        self.load_file()

    async def _dump(self):
        with open(self.name, 'w', encoding='utf-8') as f:
            json.dump(self._file.copy(), f, ensure_ascii=True, separators=(',', ':'))

    def load_file(self):
        try:
            with open(self.name, 'r') as f:
                self._file = json.load(f)
        except Exception:
            pass

    async def put(self, key: str, value, sub_key: str = None):
        if sub_key is None:
            self._file[key] = value
            await self._dump()
        else:
            self._file[key][sub_key] = value
            await self._dump()

    async def remove(self, key: str, sub_key: str = None):
        if sub_key is None:
            value = self._file.pop(key)
            await self._dump()
            return value
        else:
            value = self._file[key].pop(sub_key)
            await self._dump()
            return value

    def get(self, key, *args):
        return self._file.get(str(key), *args)

    def keys(self):
        return self._file.keys()

