from discord.ext import commands
import asyncio


class timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["stimer", "mtimer", "htimer"])
    async def _timer(self, ctx, time: float, content=None):
        zikan = f"{ctx.author.mention}時間です"
        hu = "数字が負の値です"

        if ctx.invoked_with == "stimer":
            bairitu, tanni = 1, "秒"

        if ctx.invoked_with == "mtimer":
            bairitu, tanni = 60, "分"

        if ctx.invoked_with == "htimer":
            bairitu, tanni = 3600, "時間"

        if time > 0:
            await ctx.setimed(f"{time}{tanni}後にメッセージを送ります。")
            await asyncio.sleep(time * bairitu)

            if content is not None:
                m = f"{zikan}\n{content}"
                if len(m) > 2000:
                    m = f"{zikan}、が文字数が2000文字を超えたため、内容を送信できませんでした。\n"
                    m += f"{ctx.message.jump_url} メッセージのurlを送信します"
                else:
                    await ctx.send(m)
            else:
                await ctx.send(zikan)
        else:
            await ctx.send(hu)

    @_timer.error
    async def timer_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            suuzi = "時間の指定は数字でお願いします"
            await ctx.send(suuzi)


def setup(bot):
    bot.add_cog(timer(bot))
