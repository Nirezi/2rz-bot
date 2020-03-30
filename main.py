import asyncio
import os
import traceback

import discord
import psycopg2
from discord.ext import commands

# loop = asyncio.new_event_loop()

try:
    import tokens
    token1 = tokens.token1
    local = True
except ModuleNotFoundError:
    token1 = os.environ["token1"]
    local = False

if not local:
    SQLpath = os.environ["postgre"]
else:
    SQLpath = tokens.PostgreSQL

db = psycopg2.connect(SQLpath)
cur = db.cursor()
cur.execute("select * from prefixes")
cant_connect_db = False


def _prefix_callable(bot, msg):
    base = []
    if msg.guild is None:
        base.append('/')
    else:
        try:
            cur.execute("select prefix from prefixes WHERE guild_id = %s", (msg.guild.id,))
            if len(cur.fetchall()) == 0:
                base.append("/")
            else:
                cur.execute("select * from prefixes where guild_id = %s", (msg.guild.id,))
                for row in cur.fetchall():
                    base.append(str(row[1]))
        except Exception:
            base.append("/")
            global cant_connect_db
            cant_connect_db = True
    return base


class mybot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, local=local)

        self.remove_command("help")
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
        print(bot.user.name)
        print(bot.user.id)
        print(discord.__version__)
        print("--------")

        if cant_connect_db:
            ch = self.get_channel(639121643901288500)
            await ch.send("<@544774774405201923>/nPostgreSQLへの接続に失敗しました。一時的にprefixを`/`に設定しています")

        while not self.is_closed():
            kazu = len(list(self.get_all_members()))
            await self.change_presence(activity=discord.Game(f"{kazu}人を監視中"))
            await asyncio.sleep(10)
            guild_kazu = str(len(self.guilds))
            await self.change_presence(activity=discord.Game(f"{guild_kazu}サーバー"))
            await asyncio.sleep(10)
            await self.change_presence(activity=discord.Game("/help"))
            await asyncio.sleep(10)


if __name__ == "__main__":
    # bot = bot(command_prefix = "/",loop = loop)
    # bot_task = loop.create_task(bot.start(token1))
    # loop.run_until_complete(bot_task)
    # loop.close()
    bot = mybot()
    bot.load_extension('jishaku')
    bot.run(token1)
