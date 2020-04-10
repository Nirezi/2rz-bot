import asyncio
import os
from datetime import datetime

import discord
import psycopg2
from discord.ext import commands, tasks
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

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

options = webdriver.ChromeOptions()
oprion = ["--disable-gpu", '--headless', '--log-level=3']
for op in oprion:
    options.add_argument(op)
driver = webdriver.Chrome(options=options)


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop2.start()
        self.loop3.start()
        self.date_upload.start()

    @tasks.loop(seconds=60)
    async def loop2(self):
        client = self.bot
        await client.wait_until_ready()
        hm = datetime.now().strftime("%H:%M")
        if hm == "00:00":
            channel = client.get_channel(627867724541853716)
            await channel.send("日付変更をお知らせします")

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

    @tasks.loop(minutes=10)
    async def date_upload(self):
        await self.bot.wait_until_ready()
        ch = self.bot.get_channel(646010668134170645)
        await ch.send("情報の取得を開始します")
        driver = webdriver.Chrome(options=options)

        for i in range(3):
            driver.get(
                "https://w4.minecraftserver.jp/#page=1&type=break&duration=daily")
            WebDriverWait(
                driver, 20).until(
                ec.presence_of_all_elements_located)
            source_html = driver.find_elements_by_xpath(
                '//*[@id="ranking-container"]/div/div/table/tbody')

            if len(source_html) != 0:
                await ch.send("取得完了")
                data = source_html[0]
                break
            else:
                await ch.send("再試行")
                await asyncio.sleep(5)

        await ch.send("関数実行完了")
        if len(data.text) == 0:
            await ch.send("return")
            return
        cur.execute("INSERT INTO daily_ranking values (%s, %s)",
                    (datetime.now(), data.text))
        await ch.send("dbに保存")
        db.commit()
        await ch.send("コミット")
        driver.close()


def setup(bot):
    bot.add_cog(Loops(bot))
