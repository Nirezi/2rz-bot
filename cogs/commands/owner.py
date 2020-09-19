from discord.ext import commands
import subprocess
from subprocess import PIPE


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group(invoke_without_command=True)
    async def black_list(self, ctx):
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

    @commands.command(aliases=["sh"])
    async def shell(self, ctx, *, content):
        proc = subprocess.run(content, shell=True, stdout=PIPE, stderr=PIPE, encoding="utf-8")
        await ctx.send(f"[ReturnCode]{proc.returncode}\n"
                       f"[stdout]{proc.stdout}\n"
                       f"[stderr]{proc.stderr}")


def setup(bot):
    bot.add_cog(Owner(bot))
