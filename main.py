# coding: utf-8
import asyncio
import os
import traceback
from os.path import dirname, join

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.utils.config import Config

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

try:
    import tokens
    token1 = tokens.token2
    local = True
except ModuleNotFoundError:
    token1 = os.environ["token1"]
    local = False


def _prefix_callable(bot, msg):
    base = []
    if msg.guild is None:
        base.append('/')
    else:
        base.append(bot.prefixes.get(msg.guild.id, '/'))
    return base


class MyBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=_prefix_callable, **options)
        self.local = local

        self.prefixes = Config('prefixes.json')

        if not local:
            path = "/home/user/bot-cog"
        else:
            path = "."

        self.remove_command("help")
        self.load_extension('jishaku')
        for cog in os.listdir(f"{path}/cogs/events"):
            if cog.endswith('.py'):
                try:
                    self.load_extension(f'cogs.events.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

        for cog in os.listdir(f"{path}/cogs/guilds"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.guilds.{cog[:-3]}")
                except Exception:
                    traceback.print_exc()

        for cog in os.listdir(f"{path}/cogs/commands"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.commands.{cog[:-3]}")
                except Exception:
                    traceback.print_exc()

    async def on_ready(self):  # botが起動したら
        print(self.user.name)
        print(self.user.id)
        print(discord.__version__)
        print("--------")

        while not self.is_closed():
            count = len(list(self.get_all_members()))
            await self.change_presence(activity=discord.Game(f"{count}人を監視中"))
            await asyncio.sleep(10)
            guild_count = str(len(self.guilds))
            await self.change_presence(activity=discord.Game(f"{guild_count}サーバー"))
            await asyncio.sleep(10)
            await self.change_presence(activity=discord.Game("カスタムprefixを実装"))
            await asyncio.sleep(10)


if __name__ == "__main__":
    bot = MyBot()
    bot.run(token1)

