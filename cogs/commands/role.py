from datetime import datetime

import discord
from discord.ext import commands


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role_info")
    async def _role_info(self, ctx, role: discord.Role):
        time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        kazu = len(role.members)
        member = "、".join(str(m) for m in role.members[:11])
        embed_role = discord.Embed(
            title="-----**Role Info**-----",
            color=role.colour)

        embed_role.add_field(name="Name", value=role.name)
        embed_role.add_field(name="ID", value=str(role.id))
        embed_role.add_field(name="Guild", value=role.guild)
        embed_role.add_field(name="Color", value=role.colour)
        embed_role.add_field(name="Count", value=str(kazu))
        embed_role.add_field(name="Position", value=role.position)
        embed_role.add_field(name="Hoist", value=role.hoist)
        embed_role.add_field(name="Mentionable", value=role.mentionable)
        embed_role.add_field(name="Managed", value=role.managed)
        if kazu == 0:
            embed_role.add_field(
                name="Members", value="None", inline=False)
        elif role.name == "@everyone":
            embed_role.add_field(
                name="Members", value="everyone", inline=False)
        else:
            embed_role.add_field(
                name="Members", value=member, inline=False)
        embed_role.set_footer(
            text=f'User ID：{ctx.author.id} Time：{time}',
            icon_url=ctx.guild.icon_url)  # チャンネル名,時刻,鯖のアイコンをセット
        await ctx.send(embed=embed_role)

    @_role_info.error
    async def role_info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("おっと、引数が足りませんね？参照したいroleのid, 名前, メンションのいずれかを渡してください")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("おっと？roleが見つかりませんね？引数を確認してみてください")

    @commands.command(name="role_count")
    async def _role_count(self, ctx, role: discord.Role):
        ninzuu = len(role.members)  # lenでroleの数を取得
        if role.name != "@everyone":
            await ctx.send(f"`{role.name}`は**{ninzuu}**人います")
        else:
            await ctx.send(f"この鯖には**{ninzuu}人**のユーザーがいます")

    @_role_count.error
    async def role_count_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("おっと、引数が足りませんね？参照したいroleのid, 名前, メンションのいずれかを渡してください")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("おっと？roleが見つかりませんね？引数を確認してみてください")


def setup(bot):
    bot.add_cog(Role(bot))
