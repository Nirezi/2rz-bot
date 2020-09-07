from discord.ext import commands
from datetime import datetime
import discord
from discord import Embed


class Edit(commands.Cog, name="edit"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        now = datetime.now()
        time = now.strftime("%Y/%m/%d %H:%M:%S")
        client = self.bot
        if before.author.bot:  # botは無視する
            return

        if "http" in before.content:  # urlの展開がedit判定になるため無視
            return

        if isinstance(before.channel, discord.DMChannel):
            return

        if before.guild.id == 621326525521723414:  # 2rz鯖
            channel = client.get_channel(640587255332732938)  # ログ用のch
            embed = Embed(
                description=f'**Edited in <#{before.channel.id}>**\n\n**before**\n{before.content}\n\n**after**\n{after.content}\n\n',
                color=0x1e90ff)  # 発言内容をdescriptionにセット
            embed.set_author(
                name=before.author,
                icon_url=before.author.avatar_url,
            )  # ユーザー名+ID,アバターをセット
            embed.set_footer(
                text=f'User ID：{before.author.id} Time：{time}',
                icon_url=before.guild.icon_url,
            )  # チャンネル名,時刻,鯖のアイコンをセット
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Edit(bot))
