import asyncio
import sys

import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート

from def_list import quote

# from datetime import datetime


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
        
        shiba_server = [
            615394790669811732,
            628182826914676758]  # しばさんのさばリスト
        # now = datetime.now()
        mcs = message.channel.send
        client = self.bot
        ni_men = "<@544774774405201923>"
        server = message.guild.id

        list = ["おはよう", "HI", "へっぉ", "ハロー", "HELLO"]  # 挨拶のリスト
        if message.content.upper() in list:
            msg = (f"おはようございます！{message.author}さん")
            await mcs(msg)

        list = ["こんにちは", "こんちは"]
        if message.content in list:
            await mcs("こんちは～")

        list = ["こんばんは"]
        if message.content in list:
            await mcs("ばんは～")

        list = ["おやすみ", "寝ます", "寝る", "ねる"]
        if message.content in list:
            await mcs("おやすみー")

        list = [":tada:", "ただ", "おめ", "おめでとう"]
        if message.content in list:
            await mcs(":tada:")

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
                if kakunin_kekka.content == "yes":
                    await mcs("報告ありがとうございます")
                    log_channel = client.get_channel(650654121405317120)
                    await log_channel.send(f"{ni_men}新しいレポートです", embed=report_em)

                elif kakunin_kekka.content == "no":
                    await mcs("もう一度最初からやり直してください")
                    return
                else:
                    await mcs("話聞いてた???")
                    return

        if client.user in message.mentions:  # メンションの感知
            if server in shiba_server:  # 柴鯖だったら
                msg = f"{mention}呼んだ？\nヘルプは /help　です。"
                await mcs(msg)
            else:  # それ以外だったら
                msg = f"{mention}呼んだ？\nヘルプは /help です。"
                await mcs(msg)

        if "https://discordapp.com/channels/" in message.content and "@" not in message.content:
            await quote(message, client)


def setup(bot):
    bot.add_cog(message(bot))
