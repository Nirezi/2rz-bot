import sys

import discord
from discord.ext import commands

from citycodes_dic import citycodes_dic
from def_list import wait_for_react

sys.path.append("../")


def does_not_have_args(ctx):
    return ctx.message.content == ctx.prefix + ctx.invoked_with


class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(does_not_have_args)
    async def support(self, ctx):
        """サポートサーバーへのリンクを表示"""
        embed = discord.Embed(title="本botのサポートはこちらです",
                              description="[公式サーバ](https://discord.gg/bQWsu3Z)")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(does_not_have_args)
    async def place(self, ctx):
        """/weatherコマンドで参照できる地点を表示"""
        place_str = ""
        for place in citycodes_dic.keys():
            place_str += f"{place}、"

        embed = discord.Embed(title="天気がわかる地点はこちらです", description=place_str)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(does_not_have_args)
    async def myrole(self, ctx):
        """コマンドの実行者が持っているroleを表示"""
        roles_name = ""
        for role in ctx.author.roles[1:]:
            roles_name += f"{role.name}、"
        role_count = len(ctx.author.roles[1:])

        embed = discord.Embed(title="", description=f"あなたは{role_count}個のroleを持っています\n詳細を表示するにはリアクションを押してください")
        msg = await ctx.send(embed=embed)
        embed2 = discord.Embed(title="あなたのroleは以下の通りです", description=roles_name)

        await wait_for_react(self.bot, ctx, msg, embed2)

    @commands.command()
    @commands.check(does_not_have_args)
    async def roles(self, ctx):
        """実行したサーバーにあるroleを表示"""
        roles_name = ""
        for role in ctx.guild.roles[1:]:
            roles_name += f"{role.name}、"
        role_count = len(ctx.guild.roles[1:])

        embed = discord.Embed(title="", description=f"この鯖には{role_count}個のroleがあります。\n詳細を表示する場合はリアクションを押してください")
        msg = await ctx.send(embed=embed)
        embed2 = discord.Embed(title="この鯖のroleは以下の通りです", description=roles_name)

        await wait_for_react(self.bot, ctx, msg, embed2)

    @commands.command()
    @commands.check(does_not_have_args)
    async def guilds(self, ctx):
        """botが入っているサーバを表示"""
        guilds_name = ""
        for guild in self.bot.guilds:
            guilds_name += f"{guild.name}、"
        guild_count = len(self.bot.guilds)

        embed = discord.Embed(title="", description=f"このbotは{guild_count}個の鯖にはいっています\n詳細を表示するにはリアクションを押してください")
        msg = await ctx.send(embed=embed)
        embed2 = discord.Embed(title="このbotは以下の鯖に入っています", description=f"{guilds_name}\n以上{guild_count}サーバです")

        await wait_for_react(self.bot, ctx, msg, embed2)

    @commands.command()
    @commands.check(does_not_have_args)
    async def dm(self, ctx):
        """dmに凸する"""
        msg_list = ["な", "に", "か", "よ", "う", "か", "な", "？"]
        try:
            for msg in msg_list:
                await ctx.author.send(msg)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}さてはdmが送れない設定にしてるな？")

    @commands.command()
    @commands.check(does_not_have_args)
    async def invite(self, ctx):
        """招待リンクの送信"""
        msg = "botの招待リンクを表示します。ぜひ導入してね！\n"
        msg += \
            "https://discordapp.com/api/oauth2/authorize?client_id=627143285906866187&permissions=1074097216&scope=bot"
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(SimpleCommands(bot))
