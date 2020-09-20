from discord.ext import commands


class Prefix(commands.Cog):
    """
    prefixの管理をするコマンド
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_subcommand=True)
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx):
        """"""
        await ctx.send(f"{ctx.prefix}prefix [change, default]")

    @commands.guild_only()
    @prefix.command()
    async def change(self, ctx, new_prefix=None):
        """prefixを任意の文字に変更する"""
        if new_prefix is None:
            return await ctx.send('変更後のprefixが入力されてないよ！')

        await self.bot.prefixes.put(ctx.guild.id, new_prefix)
        await ctx.send(f"prefixを`{ctx.prefix}`から`{new_prefix}`に変更したよ！")

    @commands.guild_only()
    @prefix.command()
    async def default(self, ctx):
        """prefixをデフォルトのもの`/`に変更する"""
        if ctx.prefix == "/":
            return await ctx.send("prefixはもうデフォルトだよ！")
        await self.bot.prefixes.remove(ctx.guild.id)
        await ctx.send("prefixをデフォルトの`/`に変更したよ！")


def setup(bot):
    bot.add_cog(Prefix(bot))
