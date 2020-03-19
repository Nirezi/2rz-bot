import discord
from discord.ext import commands


class role_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role_count")
    async def _role_count(self, ctx, role: discord.Role):
        ninzuu = len(role.members)  # lenでrole,,の数を取得

        if role.name != "@everyone":
            await ctx.send(f"__{role.name}__は**{ninzuu}**人います")
        else:
            await ctx.send(f"この鯖には**{ninzuu}人**のユーザーがいます")

    @_role_count.error
    async def role_count_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("roleを認識できませんでした。\nメンション、id、名前のいずれかの方法で指定してください")


def setup(bot):
    bot.add_cog(role_count(bot))
