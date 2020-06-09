import asyncio

import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート

from def_list import quote

# from datetime import datetime


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mention = message.author.mention

        if message.author.bot:  # botのメッセージなら無視する
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.content.startswith("!"):
            return

        # now = datetime.now()
        mcs = message.channel.send
        client = self.bot

        if message.channel.id == 666202941455335424:  # デバック鯖での機能
            await mcs(f"<#{message.content}>")
            await message.delete()

        if client.user in message.mentions:  # メンションの感知
            if message.guild is None:
                prefix = "/"
            else:
                prefix = self.bot.prefixes.get(message.guild.id, "/")
            msg = f"{mention}呼んだ？\nヘルプは {prefix}helpです。"
            await mcs(msg)

        if "https://discordapp.com/channels/" in message.content and "@" not in message.content:
            if str(message.guild.id) in self.bot.settings.keys('not_quote'):
                return
            await quote(message, client)


def setup(bot):
    bot.add_cog(Message(bot))
