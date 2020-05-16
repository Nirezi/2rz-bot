import asyncio
import json
import os
import sys
from datetime import datetime
from os.path import dirname, join

import discord
import psycopg2
import requests
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
        self.loop4.start()

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

    @tasks.loop(seconds=60)
    async def loop4(self):
        await self.bot.wait_until_ready()
        hm = datetime.now().strftime("%H:%M")
        if hm == "23:58":
            mcid_uuid_dic = {
                "shibatanienn_ts": "f63f13d9-ea1d-43f9-a0c7-46bb9445625d",
                "takosan_ykz": "4303b357-30ca-4209-a6c9-d96bafc60cf0",
                "chorocra": "438ed7bf-cbcf-40d9-a672-aacc2868e267",
                "ranzumu": "45578816-9dab-49fc-bef0-0525e0a57289",
                "kakkoiihito": "24eeb1a3-ed4a-444e-828c-5318122f4e4a",
                "nekorobi_0": "d6be1561-47c1-4e67-9829-2aca48f9be39"
            }

            ch = self.bot.get_channel(706322916060692571)
            msg = ""
            for mcid in mcid_uuid_dic.keys():
                uuid = mcid_uuid_dic[mcid]
                resp = requests.get(f'https://w4.minecraftserver.jp/api/ranking/player/{uuid}?types=break')
                data_json = json.loads(resp.text)
                data = data_json[0]["data"]["raw_data"]
                msg += f"{mcid}の整地量>>>{data}\n"
                await asyncio.sleep(5)
            await ch.send(msg)


def setup(bot):
    bot.add_cog(Loops(bot))
