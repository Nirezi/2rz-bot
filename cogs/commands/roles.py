import sys

import discord
from discord.ext import commands

from def_list import wait_for_react

sys.path.append('../')


class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        def does_not_have_args(ctx):
            return ctx.message.content == ctx.prefix + ctx.invoked_with

        if does_not_have_args(ctx):
            role_list = [role.name for role in ctx.guild.roles[1:]]
            role_kazu = len(ctx.guild.roles[1:])

            embed = discord.Embed(title="", description=f"この鯖には{role_kazu}個のroleがあります\n詳細を表示する場合リアクションを押してください")
            msg = await ctx.send(embed=embed)
            embed2 = discord.Embed(title="この鯖のroleは以下の通りです", description=str(role_list))

            await wait_for_react(self.bot, ctx, msg, embed2)


def setup(bot):
    bot.add_cog(roles(bot))
