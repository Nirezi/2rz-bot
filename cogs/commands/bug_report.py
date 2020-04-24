from discord.ext import commands
import asyncio
import discord


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bug_report(self, ctx):
        anser_list = []
        msg_list = []
        msg = await ctx.send("バグ等の報告ですね。各項目10分以内に送信してください")
        msg_list.append(msg)

        koumoku_list = ["その現象はどのサーバで発生していますか？",
                        "その現象は何をすると発生しますか？\n例)/avatar コマンドを使うと",
                        "具体的にどのような現象ですか？",
                        "それ以外に伝えておきたいことはありますか？(なければ「なし」で構いません)"]
        for koumoku in koumoku_list:
            send_msg = await ctx.send(koumoku)
            msg_list.append(send_msg)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                anser = await self.bot.wait_for("message", timeout=600, check=check)
            except asyncio.TimeoutError:
                await ctx.send("タイムアウトしました。はじめからやり直してください")
                return
            else:
                anser_list.append(anser.content)
                msg_list.append(anser)

        report_em = discord.Embed(
            description=f'**New Report in {ctx.channel.mention}**\n\n',
            color=0xff0000)  # 発言内容をdescriptionにセット
        report_em.add_field(name="発生場所", value=anser_list[0])
        report_em.add_field(name="何をすると", value=anser_list[1])
        report_em.add_field(name="具体的な現象", value=anser_list[2])
        report_em.add_field(name="備考", value=anser_list[3])
        await ctx.send("これでよろしいでしょうか？\nyesかnoで答えてください", embed=report_em)

        try:
            kakunin_kekka = await self.bot.wait_for("message", timeout=600, check=check)
        except asyncio.TimeoutError:
            await ctx.send("タイムアウトしました。もう一度最初からやり直してください")
            return
        else:
            kakunin = kakunin_kekka.content.lower()
            if kakunin == "yes":
                embed = discord.Emebed(
                    title="報告ありがとうございます",
                    description="公式サーバの方では進捗を確認できます。\n[公式サーバ](https://discord.gg/bQWsu3Z)")
                await ctx.send(embed=embed)
                log_channel = self.bot.get_channel(650654121405317120)
                await log_channel.send("<@544774774405201923>新しいレポートです", embed=report_em)
            elif kakunin == "no":
                await ctx.send("もう一度最初からやり直してください")
            else:
                await ctx.send("話聞いてた???")

            for msg in msg_list:
                try:
                    await msg.delete()
                except discord.Forbidden:
                    break


def setup(bot):
    bot.add_cog(Report(bot))
