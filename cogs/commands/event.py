from discord.ext import commands
import discord


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        elif ctx.guild.id == 621326525521723414:
            return True
        else:
            return False

    @commands.command(name="join")
    @commands.has_role(672006791474708490)
    async def _join(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=629828134820380682)
        if role in ctx.author.roles:
            return await ctx.send("(´・ω・｀)もう参加してるじゃん")
        await ctx.author.add_roles(role)
        await ctx.send("役職を付与しました！発表をお楽しみに！")


def setup(bot):
    bot.add_cog(Event(bot))
