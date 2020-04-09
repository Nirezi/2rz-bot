import sys

import discord
from discord.ext import commands
import os
import psycopg2

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
        if ranking is None:
            await send_msg.edit(content="情報の取得が終わりました")
            await ctx.send(f"```\n{data[1]}\n```")
        else:
            list = data[1].split("\n")
            if ranking % 20 == 0:  # 20の倍数だったときに取得できないバグが有るためゴリ押し
                mcid, n = list[77], list[78]
            else:
                pos_index = list.index(f"{ranking}位")
                mcid = list[pos_index + 1]
                n = list[pos_index + 2]
                embed = discord.Embed(
                    title=f"{ranking}位\nmcid: {mcid}", description=n)
                embed.set_thumbnail(
                    url=f"http://avatar.minecraft.jp/{mcid}/minecraft/m.png")
                await send_msg.edit(content="情報の取得が終わりました")
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DailyRanking(bot))
