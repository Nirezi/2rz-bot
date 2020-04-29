import asyncio
import os
import random
import re
from datetime import datetime

import bs4
import discord
import psycopg2
import requests
from discord import Embed
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

client = discord.Client()


async def quote(message, client):
    mcs = message.channel.send
    guilds = [guild.id for guild in client.guilds]
    try:
        for url in message.content.split('https://discordapp.com/channels/')[1:]:
            guild_id = int(url[0:18])
            if guild_id in guilds:
                try:
                    guild_id = int(url[0:18])
                    channel_id = int(url[19:37])
                    message_id = int(url[38:56])
                    guild = client.get_guild(guild_id)
                    ch = guild.get_channel(int(channel_id))
                    msg = await ch.fetch_message(int(message_id))

                    def quote_reaction(msg, embed):
                        if msg.reactions:
                            reaction_send = ''
                            for reaction in msg.reactions:
                                emoji = reaction.emoji
                                count = str(reaction.count)
                                reaction_send = f'{reaction_send}{emoji}{count} '
                            embed.add_field(
                                name='reaction', value=reaction_send, inline=False)
                        return embed

                    if msg.embeds or msg.content or msg.attachments:
                        embed = Embed(
                            description=msg.content,
                            timestamp=msg.created_at)
                        embed.set_author(
                            name=msg.author, icon_url=msg.author.avatar_url)
                        embed.set_footer(
                            text=msg.channel.name,
                            icon_url=msg.guild.icon_url)
                        if msg.attachments:
                            embed.set_image(url=msg.attachments[0].url)
                        embed = quote_reaction(msg, embed)
                        if msg.content or msg.attachments:
                            await message.channel.send(embed=embed)
                        if len(msg.attachments) >= 2:
                            for attachment in msg.attachments[1:]:
                                embed = Embed().set_image(url=attachment.url)
                                await message.channel.send(embed=embed)
                        for embed in msg.embeds:
                            embed = quote_reaction(msg, embed)
                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send('メッセージIDは存在しますが、内容がありません')
                except discord.errors.NotFound:
                    await message.channel.send("指定したメッセージが見つかりません")
            else:
                await mcs("この機能は、このbotがいるサーバーのメッセージにのみ使えます")
    except ValueError:
        pass


async def mcidcheck(message, log_channel_id, client, role1, role2=None):
    mcid = message.content.replace('\\', '')
    p = re.compile(r'^[a-zA-Z0-9_]+$')
    if p.fullmatch(message.content):
        mcid = mcid.lower()
        url = f"https://w4.minecraftserver.jp/player/{mcid}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            td = soup.td
            if f'{mcid}' in f'{td}':
                emoji = ['👍', '🙆']
                await message.author.add_roles(role1)
                if role2 is not None:
                    await message.author.add_roles(role2)
                await message.add_reaction(random.choice(emoji))
                color = [
                    0x3efd73,
                    0xfb407c,
                    0xf3f915,
                    0xc60000,
                    0xed8f10,
                    0xeacf13,
                    0x9d9d9d,
                    0xebb652,
                    0x4259fb,
                    0x1e90ff]
                embed_mcid = discord.Embed(
                    description=f'{message.author.display_name}のMCIDの報告を確認したよ！',
                    color=random.choice(color))
                embed_mcid.add_field(name="MCID", value=mcid)
                embed_mcid.set_author(
                    name=message.author,
                    icon_url=message.author.avatar_url,
                )  # ユーザー名+ID,アバターをセット
                channel = client.get_channel(log_channel_id)
                await channel.send(embed=embed_mcid)
            else:
                embed = discord.Embed(
                    description=f'{message.author} さん。\n入力されたMCIDは実在しないか、又はまだ一度も整地鯖にログインしていません。\n\
                                                続けて間違った入力を行うと規定によりBANの対象になることがあります。', color=0xff0000)
                await message.channel.send(embed=embed)
        except requests.exceptions.HTTPError:
            await message.channel.send(f'requests.exceptions.HTTPError')
    else:
        embed = discord.Embed(
            description=f"{message.author}さん。\nMCIDに使用できない文字が含まれています'\n続けて間違った入力を行うと規定によりBANの対象になることがあります。",
            color=0xff0000)
        await message.channel.send(embed=embed)


async def wait_for_react(bot, ctx, msg, embed2):
    await msg.add_reaction(u"\u25B6")

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if reaction.message.id != msg.id:
            return 0
        if emoji == u"\u25B6":
            if user != ctx.author:
                return 0
            else:
                return emoji, user

    while not bot.is_closed():
        reaction, user = await bot.wait_for("reaction_add", check=check)
        await msg.edit(embed=embed2)


async def data_upload(self):
    options = webdriver.ChromeOptions()
    option = ["--disable-gpu", '--headless', '--log-level=3']
    for op in option:
        options.add_argument(op)
    driver = webdriver.Chrome(options=options)
    ch = self.bot.get_channel(646010668134170645)
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
            data = source_html[0]
            break
        else:
            await asyncio.sleep(5)

    if len(data.text) == 0:
        await ch.send("return")
        return
    cur.execute("SELECT date FROM daily_ranking ORDER BY date DESC;")
    cur.execute("DELETE FROM daily_ranking WHERE date = %s", (cur.fetchone()[0],))
    cur.execute("INSERT INTO daily_ranking values (%s, %s)",
                (datetime.now(), data.text))
    db.commit()
    driver.close()
