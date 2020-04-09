import sys

import discord
from discord.ext import commands
import os
import psycopg2
from datetime import datetime

sys.path.append("../")

try:
    import tokens
    local = True
except ModuleNotFoundError:
    local = False

if local:
    SQLpath = tokens.PostgreSQL
else:
    SQLpath = os.environ["postgre"]
db = psycopg2.connect(SQLpath)
cur = db.cursor()


class DailyRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=10)
    async def daily_ranking(self, ctx, ranking: int = None):
        if ranking is not None:
            page = int(ranking / 20) + 1
            if ranking % 20 == 0 and not ranking == 20:
                page -= 1
        else:
            page = 1

        if page > 1:
            await ctx.send(f"確認できるのは20位までです。その順位は↓のリンクを参照してください\nhttps://w4.minecraftserver.jp/#page={page}&type=break&duration=daily")
            return
        send_msg = await ctx.send("情報を取得しています")

        cur.execute("SELECT * from daily_ranking ORDER BY date ASC LIMIT 1;")
        data = cur.fetchone()

        data_day = cur.execute("DAY(%s);", (data[0],))
        now_day = datetime.now().day
        if data_day != now_day:
            await ctx.send("今日のランキングはまだ更新されていません")
            return

        if ranking is None:
            await send_msg.edit(content="情報の取得が終わりました")
            await ctx.send(f"```\n{data[1]}\n```\n{data[0]}時点の情報です")
        else:
            try:
                list = data[1].split("\n")
                if ranking % 20 == 0:  # 20の倍数だったときに取得できないバグが有るためゴリ押し
                    mcid, n = list[77], list[78]
                else:
                    pos_index = list.index(f"{ranking}位")
                    mcid = list[pos_index + 1]
                    n = list[pos_index + 2]
                    embed = discord.Embed(
                        title=f"{ranking}位\nmcid: {mcid}", description=f"{n}\n{data[0]}時点の情報です")
                    embed.set_thumbnail(
                        url=f"http://avatar.minecraft.jp/{mcid}/minecraft/m.png")
                    await send_msg.edit(content="情報の取得が終わりました")
                    await ctx.send(embed=embed)
            except ValueError:
                await ctx.send("その順位の人はまだ存在しません")


def setup(bot):
    bot.add_cog(DailyRanking(bot))
