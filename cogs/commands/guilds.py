import sys

import discord
from discord.ext import commands

from def_list import wait_for_react

sys.path.append('../')


class guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guilds(self, ctx):
        def does_not_have_args(ctx):
            return ctx.message.content == ctx.prefix + ctx.invoked_with

        if does_not_have_args(ctx):
            guild = [saba.name for saba in self.bot.guilds]
            kazu = len(self.bot.guilds)
    
            embed = discord.Embed(title="", description=f"このbotは{kazu}個の鯖にはいっています\n詳細を表示するにはリアクションを押してください")
            embed2 = discord.Embed(title="このbotは以下の鯖に入っています", description=f"{guild}\n以上{kazu}サーバです")
            msg = await ctx.send(embed=embed)

            await wait_for_react(self.bot, ctx, msg, embed2)


def setup(bot):
    bot.add_cog(guilds(bot))
