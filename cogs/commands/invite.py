from discord.ext import commands


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        msg = "botの招待リンクを表示します。ぜひ導入してね！\n"
        msg += "https://discordapp.com/api/oauth2/authorize?client_id=627143285906866187&permissions=8&scope=bot"
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Invite(bot))
