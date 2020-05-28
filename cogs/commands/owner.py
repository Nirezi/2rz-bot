from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group()
    async def black_list(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"ブラックリストには以下のidが登録されてるよ！\n{self.bot.blacklist.keys()}")

    @black_list.command()
    async def add(self, ctx, key: str):
        await self.bot.blacklist.put(key, True)
        await ctx.send(f"{key}をブラックリストに追加しました")

    @black_list.command()
    async def remove(self, ctx, key: str):
        if key in self.bot.blacklist.keys():
            await ctx.send(f'{key}はまだブラックリストに登録されていません')
            return
        value = await self.bot.blacklist.remove(key)
        await ctx.send(f"{value}をブラックリストから削除しました")


def setup(bot):
    bot.add_cog(Owner(bot))
