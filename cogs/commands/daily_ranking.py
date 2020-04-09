import asyncio

import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class DailyRanking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=10)
    async def daily_ranking(self, ctx, ranking: int = None):
        send_msg = await ctx.send("情報を取得しています、、、")
        if ranking is None:
            page = 1
        else:
            page = int(ranking / 20) + 1
            if ranking < 21:
                pass
                # pos = ranking % 20 + 1
            else:
                pass
                # pos = ranking + 1

        options = webdriver.ChromeOptions()
        oprion = ["--disable-gpu", '--headless', '--log-level=3']
        for op in oprion:
            options.add_argument(op)
        driver = webdriver.Chrome(options=options)

        async def search(self, page):
            for i in range(3):
                driver.get(
                    f"https://w4.minecraftserver.jp/#page={page}&type=break&duration=daily")
                WebDriverWait(
                    driver, 20).until(
                    ec.presence_of_all_elements_located)
                source_html = driver.find_elements_by_xpath(
                    '//*[@id="ranking-container"]/div/div/table/tbody')
                
                if len(source_html) != 0:
                    return source_html
                    break
                else:
                    await asyncio.sleep(5)

        source_html = await search(self, page)
        if len(source_html[0].text) == 0:
            await ctx.send("日間ランキングはまだ更新されていません")

        try:
            if ranking is None:
                msg = f"```\n{source_html[0].text}\n```"
                await send_msg.edit(content="情報の取得が終わりました")
                await ctx.send(msg)
            else:
                list = source_html[0].text.split("\n")
                if ranking % 20 == 0:  # 20の倍数だったときに取得できないバグが有るためゴリ押し
                    mcid, n = list[77], list[78]
                else:
                    pos_index = list.index(f"{ranking}位")
                    mcid = list[pos_index + 1]
                    n = list[pos_index + 2]
                embed = discord.Embed(title=f"{ranking}位\nmcid: {mcid}", description=n)
                embed.set_thumbnail(
                    url=f"http://avatar.minecraft.jp/{mcid}/minecraft/m.png")
                await send_msg.edit(content="情報の取得が終わりました")
                await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("渡された順位のユーザーがまだ存在しません。これがバグだと思う場合2rzまで問い合わせてください")

        driver.quit()


def setup(bot):
    bot.add_cog(DailyRanking(bot))
