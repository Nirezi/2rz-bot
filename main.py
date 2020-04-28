# coding: utf-8
import asyncio
import os
import traceback
from os.path import dirname, join

import discord
import psycopg2
from discord.ext import commands
from dotenv import load_dotenv

loop = asyncio.new_event_loop()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

try:
    import tokens
    token1 = tokens.token2
    local = True
except ModuleNotFoundError:
    token1 = os.environ["token1"]
    local = False

if not local:
    SQLpath = os.environ["DATABASE_URL"]
else:
    SQLpath = tokens.PostgreSQL

db = psycopg2.connect(SQLpath)
cur = db.cursor()


def _prefix_callable(bot, msg):
    base = []
    if msg.guild is None:
        base.append('/')
    else:
        cur.execute("select prefix from prefixes WHERE guild_id = %s;", (msg.guild.id,))
        if len(cur.fetchall()) == 0:
            base.append("/")
        else:
            cur.execute("select * from prefixes where guild_id = %s;", (msg.guild.id,))
            for row in cur.fetchall():
                base.append(str(row[1]))
    return base


class MyBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=_prefix_callable, **options)
        self.local = local

        self.remove_command("help")
        self.load_extension('jishaku')
        for cog in os.listdir("./cogs/events"):
            if cog.endswith('.py'):
                try:
                    self.load_extension(f'cogs.events.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

        for cog in os.listdir("./cogs/guilds"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.guilds.{cog[:-3]}")
                except Exception:
                    traceback.print_exc()

        for cog in os.listdir("./cogs/commands"):
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
    mybot = MyBot(loop=loop)
    bot_task = loop.create_task(mybot.start(token1))
    loop.run_until_complete(bot_task)
    loop.close()
