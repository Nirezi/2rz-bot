import asyncio
import os
import sys

import discord
import psycopg2
from discord.ext import commands  # Bot Commands Frameworkのインポート

from def_list import quote

# from datetime import datetime


try:
    import tokens
    local = True
except ModuleNotFoundError:
    local = False

if local:
    SQLpath = tokens.PostgreSQL
else:
    SQLpath = os.environ["postgre"]


sys.path.append('../')


class message(commands.Cog):
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
        ni_men = "<@544774774405201923>"

        if message.channel.id == 666202941455335424:  # デバック鯖での機能
            await mcs(f"<#{message.content}>")
            await message.delete()

        koumoku_list = ["その現象はどのサーバで発生していますか？",
                        "その現象は何をすると発生しますか？\n例)/avatar コマンドを使うと",
                        "具体的にどのような現象ですか？",
                        "それ以外に伝えておきたいことはありますか？(なければ「なし」で構いません)"]
        if message.content == "/bug_report":  # reportコマンド
            await mcs("バグ等の報告ですね。各項目10分以内に送信してください")

            kaitou_list = []
            for koumoku in koumoku_list:
                await mcs(koumoku)

                def check(m):
                    return m.author == message.author and m.channel == message.channel

                try:
                    kaitou = await client.wait_for("message", timeout=600, check=check)
                except asyncio.TimeoutError:
                    await mcs("タイムアウトしました。もう一度最初からやり直してください")
                    return
                else:
                    kaitou_list.append(kaitou.content)

            report_em = discord.Embed(
                description=f'**New Report in {message.channel.mention}**\n\n',
                color=0xff0000)  # 発言内容をdescriptionにセット
            report_em.add_field(name="発生場所", value=kaitou_list[0])
            report_em.add_field(name="何をすると", value=kaitou_list[1])
            report_em.add_field(name="具体的な現象", value=kaitou_list[2])
            report_em.add_field(name="備考", value=kaitou_list[3])
            await mcs("これでよろしいでしょうか？\nyesかnoで答えてください", embed=report_em)

            def kakunin(m):
                return m.author == message.author and m.channel == message.channel

            try:
                kakunin_kekka = await client.wait_for("message", timeout=600, check=kakunin)
            except asyncio.TimeoutError:
                await mcs("タイムアウトしました。もう一度最初からやり直してください")
                return
            else:
                kakunin = kakunin_kekka.content.lowner()
                if kakunin == "yes":
                    await mcs("報告ありがとうございます")
                    log_channel = client.get_channel(650654121405317120)
                    await log_channel.send(f"{ni_men}新しいレポートです", embed=report_em)

                elif kakunin == "no":
                    await mcs("もう一度最初からやり直してください")
                    return
                else:
                    await mcs("話聞いてた???")
                    return

        if client.user in message.mentions:  # メンションの感知
            prefix = ""
            if message.guild is None:
                prefix = "/"
            else:
                db = psycopg2.connect(SQLpath)
                cur = db.cursor()
                cur.execute("select * from prefixes where guild_id = %s", (message.guild.id,))
                for row in cur.fetchall():
                    prefix = row[1]
            msg = f"{mention}呼んだ？\nヘルプは {prefix}helpです。"
            await mcs(msg)

        if "https://discordapp.com/channels/" in message.content and "@" not in message.content:
            await quote(message, client)


def setup(bot):
    bot.add_cog(message(bot))
