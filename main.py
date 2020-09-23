# coding: utf-8
import json
import os
import re
import traceback
from os.path import dirname, join

import discord
import requests
import sentry_sdk
from discord.ext import commands
from dotenv import load_dotenv

# from cogs.commands.manage_help import BotHelp
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
    sentry_sdk.init(os.environ["sentry_url"], traces_sample_rate=1.0)


def _prefix_callable(bot, msg: discord.Message):
    base = [f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]
    if msg.guild is None:
        base.append('/')
    else:
        base.append(bot.prefixes.get(msg.guild.id, '/'))
    return base


class MyBot(commands.Bot):
    def __init__(self, **options):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        super().__init__(command_prefix=_prefix_callable, allowed_mentions=allowed_mentions, **options)
        self.local = local
        self.guild_invite_url = "https://discord.gg/bQWsu3Z"
        self.invite_url = "https://discord.com/oauth2/authorize?client_id=627143285906866187&permissions=268823638&scope=bot"
        self.donate_form = "https://disneyresidents.fanbox.cc/posts"

        # guild_id: prefix
        self.prefixes = Config('prefixes.json')

        # user_id or guild_id to True
        self.blacklist = Config('blacklist.json')

        # message_id: reaction: role
        self.role_panel_data = Config('role_panel_data.json')

        # setting: guild_id: True
        self.settings = Config('settings.json')

        if not local:
            path = "/home/user/2rz-bot"
        else:
            path = "."

        self.remove_command("help")
        self.load_extension('jishaku')
        dirs = ["commands", "events", "guilds"]
        for dire in dirs:
            for cog in os.listdir(f"{path}/cogs/{dire}"):
                if cog.endswith('.py'):
                    try:
                        self.load_extension(f'cogs.{dire}.{cog[:-3]}')
                    except Exception:
                        traceback.print_exc()

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
                channel_id, message_id = map(int, url.split("/")[-2:])
                ch = self.get_channel(channel_id)
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
