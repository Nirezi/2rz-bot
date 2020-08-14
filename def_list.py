import os
import random
import re

import bs4
import discord
import psycopg2
import requests

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
            await message.channel.send('requests.exceptions.HTTPError')
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
        await bot.wait_for("reaction_add", check=check)
        await msg.edit(embed=embed2)
