import sys

import discord
from discord.ext import commands

from def_list import wait_for_react

sys.path.append('../')


class members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def members(self, ctx):
        def does_not_have_args(ctx):
            return ctx.message.content == ctx.prefix + ctx.invoked_with
        
        if does_not_have_args(ctx):
            members = [mem.name for mem in ctx.guild.members]
            mem_kazu = len(ctx.guild.members)

            embed = discord.Embed(title="", description=f"この鯖には{mem_kazu}人のユーザーがいます\n詳細を表示するにはリアクションを押してください")
            msg = await ctx.send(embed=embed)
            embed2 = discord.Embed(title="この鯖のメンバーは以下の通りです", description=str(members))

            await wait_for_react(self.bot, ctx, msg, embed2)


def setup(bot):
    bot.add_cog(members(bot))
