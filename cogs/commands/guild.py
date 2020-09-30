import asyncio

import discord
from discord.ext import commands


class Guild(commands.Cog):
    """
    サーバーに関係するコマンド
    """

    def __init__(self, bot):
        self.bot = bot
        self.reacts = [
            "\N{BLACK LEFT-POINTING TRIANGLE}",  # 戻る
            "\N{BLACK RIGHT-POINTING TRIANGLE}"  # 進む
        ]

    def cog_check(self, ctx):
        if not ctx.guild:
            return False
        return True

    async def check_page(self, ctx, msg: discord.Message, page: int, max_page: int) -> int:
        def check(reaction, user):
            if user.bot or user.id != ctx.author.id:
                return
            elif reaction.message.id != msg.id:
                return False
            elif str(reaction.emoji) in self.reacts:
                return True
            else:
                return False

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=300)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            return -1
        else:
            emoji = str(reaction.emoji)
            if emoji == self.reacts[0]:
                if page == 0:
                    return max_page
                return page - 1
            else:
                if page == max_page:
                    return 0
                return page + 1

    @commands.command()
    async def myrole(self, ctx):
        """コマンドの実行者が持っているroleを表示する"""
        if (count := len(ctx.author.roles[1:])) == 0:
            await ctx.send("おっと、まだroleを持っていないみたいですね")
        else:
            if count >= 20:
                roles = "、".join(r.name for r in ctx.author.roles[1:22])
                embed = discord.Embed(title="roleは以下の通りです!(1ページ目)", description=roles)
                msg = await ctx.send(embed=embed)
                for react in self.reacts:
                    await msg.add_reaction(react)
                page = 0
                max_page = -(-len(ctx.author.roles[1:]) // 20)

                while not self.bot.is_closed():
                    page = await self.check_page(ctx, msg, page, max_page)
                    if page == -1:
                        break
                    roles = "、".join(r.name for r in ctx.author.roles[1 + 20 * page: page * 20 + 22])
                    embed = discord.Embed(title=f"roleは以下の通りです!({page}ページ目)", description=roles)
                    await msg.edit(embed=embed)
            else:
                roles = "、".join(r.name for r in ctx.author.roles[1:])

                embed = discord.Embed(title="roleは以下の通りです！", description=f"{roles}\nSum:{count}")
                await ctx.send(embed=embed)

    @commands.command()
    async def members(self, ctx):
        """実行したサーバーのユーザーを表示する"""
        if (count := len(ctx.guild.members)) >= 100:
            members = "、".join(r.name for r in ctx.guild.members[:101])
            embed = discord.Embed(title="メンバーは以下の通りです!(1ページ目)", description=members)
            msg = await ctx.send(embed=embed)
            for react in self.reacts:
                await msg.add_reaction(react)
            page = 0
            max_page = -(-len(ctx.guild.roles) // 20)

            while not self.bot.is_closed():
                page = await self.check_page(ctx, msg, page, max_page)
                if page == -1:
                    break
                members = "、".join(m.name for m in ctx.guild.members[:page * 100 + 101])
                embed = discord.Embed(title=f"メンバーは以下の通りです!({page}ページ目)", description=members)
                await msg.edit(embed=embed)
        else:
            members = "、".join(m.name for m in ctx.guild.members)

            embed = discord.Embed(title="メンバーは以下の通りです！", description=f"{members}\nSum:{count}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Guild(bot))
