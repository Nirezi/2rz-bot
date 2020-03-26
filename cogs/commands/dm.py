from discord.ext import commands


class dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dm")
    async def _dm(self, ctx):
        list = ["な", "に", "か", "よ", "う", "か", "な", "？"]
        try:
            for msg in list:
                await ctx.author.send(msg)
        except Exception:
            await ctx.send(f"{ctx.author.mention}あれ？dmが送れないみたい")


def setup(bot):
    bot.add_cog(dm(bot))
