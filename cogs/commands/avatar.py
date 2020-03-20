from discord.ext import commands


class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar")
    async def _avatar(self, ctx, id: int = None):
        bot = self.bot

        if id is None:
            await ctx.send("idを指定してね！")
            return

        user = bot.get_user(id)
        guild = bot.get_guild(id)

        if user is not None:
            await ctx.send(f"{user}さんのアイコン\n{user.avatar_url}")
        elif guild is not None:
            await ctx.send(f"{guild}のアイコン\n{guild.icon_url}")
        else:
            await ctx.send("404 NotFound\nもしかして:idが間違っている")

    @_avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("もしかして:idが数字じゃない")


def setup(bot):
    bot.add_cog(avatar(bot))
