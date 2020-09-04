import discord
from discord.ext import commands


class SimpleCommands(commands.Cog):
    """引数がなく、単体で実行できるコマンド"""
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.content == ctx.prefix + ctx.invoked_with

    @commands.command()
    async def dm(self, ctx):
        """dmに凸する"""
        msg_list = ["な", "に", "か", "よ", "う", "か", "な", "？"]
        try:
            for msg in msg_list:
                await ctx.author.send(msg)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}さてはdmが送れない設定にしてるな？")

    @commands.command()
    async def invite(self, ctx):
        """招待リンクの送信"""
        embed = discord.Embed(title="botの招待リンクを表示します。ぜひ導入してね！",
                              description=f"[招待リンク]({self.bot.invite_url})")
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """botが生きているか確認"""
        await ctx.send(f"pong!\n{self.bot.latency * 1000}ms")


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
