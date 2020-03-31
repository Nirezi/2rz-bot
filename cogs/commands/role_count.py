import discord
from discord.ext import commands


class role_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role_count")
    async def _role_count(self, ctx, role: discord.Role):
        ninzuu = len(role.members)  # lenでrole,,の数を取得
        if role.name != "@everyone":
            await ctx.send(f"`{role.name}`は**{ninzuu}**人います")
        else:
            await ctx.send(f"この鯖には**{ninzuu}人**のユーザーがいます")

    @_role_count.error
    async def role_count_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("引数が不足しています\n第一引数として役職をメンション、id、名前で渡してください")
        if isinstance(error, commands.BadArgument):
            await ctx.send("不正な引数です")


def setup(bot):
    bot.add_cog(role_count(bot))
