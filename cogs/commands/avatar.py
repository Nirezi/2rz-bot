from discord.ext import commands
import discord


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
            embed = discord.Embed(title=f"{user}", description="")
            embed.set_image(url=user.avatar_url)
            await ctx.send(embed=embed)
        elif guild is not None:
            if len(guild.icon_url) == 0:
                await ctx.send("標準のアイコンだから表示できないや！")
            else:
                embed = discord.Embed(title=f"{guild}", description="")
                embed.set_image(url=guild.icon_url)
                await ctx.send(embed=embed)
        else:
            await ctx.send("404 NotFound\nあれ？ちょっと僕には見つけられそうにないや、、")

    @_avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("もしかして:idが数字じゃない")


def setup(bot):
    bot.add_cog(avatar(bot))
