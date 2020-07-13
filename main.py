# coding: utf-8
import asyncio
import json
import os
import traceback
from os.path import dirname, join
import random


import discord
import psycopg2
import requests
from discord.ext import commands
from dotenv import load_dotenv

from cogs.utils.config import Config

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

try:
    import tokens
    token1 = tokens.token1
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


if local:
    SQLpath = tokens.PostgreSQL
else:
    SQLpath = os.environ["DATABASE_URL"]
db = psycopg2.connect(SQLpath)
cur = db.cursor()


class MyBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=_prefix_callable, **options)
        self.local = local
        self.guild_invite_url = "https://discord.gg/bQWsu3Z"
        self.invite_url = "https://discord.com/oauth2/authorize?client_id=627143285906866187&permissions=268823638&scope=bot"
        self.donate_form = "https://disneyresidents.fanbox.cc/posts"

        # guild_id: prefix
        self.prefixes = Config('prefixes.json')

        # user_id or guild_id to True
        self.blacklist = Config('blacklist.json')

        # guild_id: True
        self.no_ad = Config('no_ad.json')

        # message_id: reaction: role
        self.role_panel_data = Config('role_panel_data.json')

        # setting: guild_id: True
        self.settings = Config('settings.json')

        if not local:
            path = "/home/user/2rezi-bot"
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

        @self.after_invoke
        async def send_ad(ctx):
            if ctx.guild is None:
                return
            if str(ctx.guild.id) in self.no_ad.keys():
                return
            num = random.randint(0, 19)
            if num == 0:
                msg = f"{self.user.name}を使ってくれてありがとうございます！\n" \
                      f"ここで少し宣伝させてください！\n" \
                      f"{self.user.name}の導入や公式サーバへの参加をお願いします！(寄付も募っています)\n" \
                      f"[公式サーバ]({self.guild_invite_url})\n[招待リンク]({self.invite_url})\n[寄付フォーム]({self.donate_form})\n" \
                      f"＊500円以上の寄付でこの広告はでてこなくなります。(公式サーバでは表示されません)"
                embed = discord.Embed(title="", description=msg)
                await ctx.send(embed=embed)

        @self.check
        async def check_blacklist(ctx):
            return ctx.author.id not in self.blacklist.keys()

    @staticmethod
    def get_mined_block(uuid: str) -> int:
        resp = requests.get(f'https://w4.minecraftserver.jp/api/ranking/player/{uuid}?types=break')
        data_json = json.loads(resp.text)
        data = data_json[0]["data"]["raw_data"]
        return int(data)

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

    @staticmethod
    def get_mined_block(uuid: str) -> int:
        """整地鯖のapiからこれまでに掘ったブロック数を取得"""
        resp = requests.get(f'https://w4.minecraftserver.jp/api/ranking/player/{uuid}?types=break')
        data_json = json.loads(resp.text)
        data = data_json[0]["data"]["raw_data"]
        return int(data)

    def get_shard_count(self, user: discord.User) -> int:
        """ユーザとbotの共通のサーバーの数を取得"""
        return sum(g.get_member(user.id) is not None for g in self.guilds)


if __name__ == "__main__":
    bot = MyBot()
    bot.run(token1)

