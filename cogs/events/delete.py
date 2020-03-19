from discord.ext import commands
from datetime import datetime
import discord
from discord import Embed


class delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        now = datetime.now()
        time = now.strftime("%Y/%m/%d %H:%M:%S")
        client = self.bot
        if message.author.bot:  # botは無視する
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.guild.id == 621326525521723414:  # 2rzサバなら
            embed = Embed(
                description=f'**Deleted in <#{message.channel.id}>**\n\n{message.content}\n\n',
                color=0xff0000)  # 発言内容をdescriptionにセット
            embed.set_author(
                name=message.author,
                icon_url=message.author.avatar_url,
            )  # ユーザー名+ID,アバターをセット
            embed.set_footer(
                text=f'User ID：{message.author.id} Time：{time}',
                icon_url=message.guild.icon_url,
            )  # チャンネル名,時刻,鯖のアイコンをセット
            channel = client.get_channel(640587255332732938)  # ログ用のch
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(delete(bot))
