import re

import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート


class Message(commands.Cog, name="message"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # botのメッセージなら無視する
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.content.startswith("!"):
            return

        if re.findall(r"https://(?:ptb.|canary.)?discord(?:app)?.com/channels/[0-9]+/[0-9]+/[0-9]+", message.content) and ("@" not in message.content):
            if str(message.guild.id) in self.bot.settings.keys('not_quote'):
                return
            await self.bot.quote(message)


def setup(bot):
    bot.add_cog(Message(bot))
