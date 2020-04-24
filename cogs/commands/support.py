from discord.ext import commands
import discord


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        def does_not_have_args(ctx):
            return ctx.message.content == ctx.prefix + ctx.invoked_with

        if not does_not_have_args(ctx):
            return

        embed = discord.Embed(title="本botのサポートはこちらです",
                              description="[公式サーバ](https://discord.gg/bQWsu3Z)")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Support(bot))
