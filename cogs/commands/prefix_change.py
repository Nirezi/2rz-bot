from discord.ext import commands

try:
    import tokens
    local = True
except ModuleNotFoundError:
    local = False


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.prefix}prefix [change, default, show]")

    @prefix.command()
    async def change(self, ctx, new_prefix):
        if ctx.guild.id not in self.bot.prefixes.keys():
            await self.bot.prefixes.put(ctx.guild.id, new_prefix)
            await ctx.send(f"prefixが`/`から`{new_prefix}`に変更されました")
        else:
            await self.bot.prefixes.put(ctx.guild.id, new_prefix)
            await ctx.send(f"prefixが`{ctx.prefix}`から`{new_prefix}`に変更されました")

    @prefix.command()
    async def default(self, ctx):
        await self.bot.prefixes.remove(ctx.guild.id)
        await ctx.send("prefixがデフォルトの`/`に変更されました")


def setup(bot):
    bot.add_cog(Prefix(bot))
