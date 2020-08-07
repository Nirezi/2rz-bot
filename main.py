# coding: utf-8
import json
import os
import re
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

        self.birthday = Config('birthday.json')

        if not local:
            path = "/home/user/2rz-bot"
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
        async def checks(ctx):
            if self.blacklist.is_key(ctx.author.id):
                return False
            elif not ctx.channel.permissions_for(ctx.me).send_messages:
                return False
            return True

    async def on_ready(self):  # botが起動したら
        print(self.user.name)
        print(self.user.id)
        print(discord.__version__)
        print("--------")

    @staticmethod
    def get_mined_block(uuid: str) -> int:
        """整地鯖のapiからこれまでに掘ったブロック数を取得"""
        resp = requests.get(f'https://w4.minecraftserver.jp/api/ranking/player/{uuid}?types=break')
        data_json = json.loads(resp.text)
        data = data_json[0]["data"]["raw_data"]
        return int(data)

    def get_shared_count(self, user: discord.User) -> int:
        """ユーザとbotの共通のサーバーの数を取得"""
        return sum(g.get_member(user.id) is not None for g in self.guilds)

    async def quote(self, message):
        try:
            for url in re.findall(r"https://(?:ptb.|canary.)?discord(?:app)?.com/channels/[0-9]+/[0-9]+/[0-9]+", message.content):
                guild_id, channel_id, message_id = map(int, url.split("/")[-3:])
                guild = self.get_guild(guild_id)
                ch = guild.get_channel(channel_id)
                if ch is None:
                    return
                msg = await ch.fetch_message(message_id)

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
                    embed = discord.Embed(
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
                            embed = discord.Embed().set_image(url=attachment.url)
                            await message.channel.send(embed=embed)
                    for embed in msg.embeds:
                        embed = quote_reaction(msg, embed)
                        await message.channel.send(embed=embed)
                elif msg.system_content:
                    embed = discord.Embed(
                        description=f"{msg.system_content}\n\n:warning:これはシステムメッセージです。",
                        timestamp=msg.created_at)
                    embed.set_author(
                        name=msg.author, icon_url=msg.author.avatar_url)
                    embed.set_footer(
                        text=msg.channel.name,
                        icon_url=msg.guild.icon_url)
                    embed = quote_reaction(msg, embed)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send('メッセージIDは存在しますが、内容がありません')
        except discord.errors.NotFound:
            await message.channel.send("指定したメッセージが見つかりません")
        except ValueError as e:
            raise commands.CommandInvokeError(e)


if __name__ == "__main__":
    bot = MyBot()
    bot.run(token1)
