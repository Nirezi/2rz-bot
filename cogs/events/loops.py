import asyncio
import os
import sys
from datetime import datetime
from os.path import dirname, join

import discord
import psycopg2
from discord.ext import commands, tasks
from dotenv import load_dotenv

from def_list import data_upload

sys.path.append("../")

try:
    import tokens
    local = True
except ModuleNotFoundError:
    local = False

if local:
    SQLpath = tokens.PostgreSQL
else:
    SQLpath = os.environ["DATABASE_URL"]
db = psycopg2.connect(SQLpath)
cur = db.cursor()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop2.start()
        self.loop3.start()

    @tasks.loop(seconds=60)
    async def loop2(self):
        client = self.bot
        await client.wait_until_ready()
        hm = datetime.now().strftime("%H:%M")
        if hm == "23:58":
            await data_upload(self)
            await asyncio.sleep(5)
            cur.execute("SELECT ranking_data FROM daily_ranking ORDER BY date DESC;")
            ch = self.bot.get_channel(698486078503649280)
            data = cur.fetchone()
            await ch.send(f"```{data[0]}```")

    @tasks.loop(seconds=60)
    async def loop3(self):
        hm = datetime.now().strftime("%H:%M")
        client = self.bot
        await client.wait_until_ready()
        if hm == "19:00":
            guild = client.get_guild(610309046851076121)
            role = discord.utils.get(guild.roles, id=665853511740948500)  # 新規
            channel = client.get_channel(665854731180310528)
            kazu = len(role.members)
            if kazu == 0:
                await channel.send("おっと、始めにを読んでない人はいないみたいです")
            else:
                await channel.send(f"{role.mention}\n{kazu}人の人がまだ<#630402461395451913>を読んでないみたいですね")


def setup(bot):
    bot.add_cog(Loops(bot))
