from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True, invoke_without_command=True)
    async def prefix(self, ctx):
        await ctx.send(f"{ctx.prefix}prefix [change, default]")

    @commands.guild_only()
    @prefix.command()
    async def change(self, ctx, new_prefix=None):
        if new_prefix is None:
            return await ctx.send('変更後のprefixが入力されてないよ！')

        await self.bot.prefixes.put(ctx.guild.id, new_prefix)
        await ctx.send(f"prefixを`{ctx.prefix}`から`{new_prefix}`に変更したよ！")

    @commands.guild_only()
    @prefix.command()
    async def default(self, ctx):
        await self.bot.prefixes.remove(ctx.guild.id)
        await ctx.send("prefixをデフォルトの`/`に変更したよ！")


def setup(bot):
    bot.add_cog(Prefix(bot))
