import sys

import discord
from discord.ext import commands

from citycodes_dic import citycodes_dic
from def_list import wait_for_react

sys.path.append("../")


class SimpleCommands(commands.Cog):
    """引数がなく、単体で実行できるコマンド"""
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.content == ctx.prefix + ctx.invoked_with

    @commands.command()
    async def place(self, ctx):
        """/weatherコマンドで参照できる地点を表示"""
        place_str = ""
        for place in citycodes_dic.keys():
            place_str += f"{place}、"

        embed = discord.Embed(title="天気がわかる地点はこちらです", description=place_str)
        await ctx.send(embed=embed)

    @commands.command()
    async def myrole(self, ctx):
        """コマンドの実行者が持っているroleを表示"""
        if (count := len(ctx.author.roles[1:])) == 0:
            await ctx.send("おっと、まだroleを持っていないみたいですね？")
        else:
            roles_name = "、".join(r.name for r in ctx.author.roles[1:])

            embed = discord.Embed(title="", description=f"あなたは{count}個のroleを持っています\n詳細を表示するにはリアクションを押してください")
            msg = await ctx.send(embed=embed)
            embed2 = discord.Embed(title="あなたのroleは以下の通りです", description=roles_name)

            await wait_for_react(self.bot, ctx, msg, embed2)

    @commands.command()
    async def dm(self, ctx):
        """dmに凸する"""
        msg_list = ["な", "に", "か", "よ", "う", "か", "な", "？"]
        try:
            for msg in msg_list:
                await ctx.author.send(msg)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}さてはdmが送れない設定にしてるな？")

    @commands.command()
    async def members(self, ctx):
        """実行したサーバーのユーザーを表示"""
        members_name = ""
        for member in ctx.guild.members:
            members_name += member.name
        mem_count = len(ctx.guild.members)

        embed = discord.Embed(title="", description=f"この鯖には{mem_count}人のユーザーがいます\n詳細を表示するにはリアクションを押してください")
        msg = await ctx.send(embed=embed)
        embed2 = discord.Embed(title="この鯖のメンバーは以下の通りです", description=members_name)

        await wait_for_react(self.bot, ctx, msg, embed2)

    @commands.command()
    async def invite(self, ctx):
        """招待リンクの送信"""
        embed = discord.Embed(title="botの招待リンクを表示します。ぜひ導入してね！",
                              description=f"[招待リンク]({self.bot.invite_url})")
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """botが生きているか確認"""
        await ctx.send("pong!")


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
