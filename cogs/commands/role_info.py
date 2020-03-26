from datetime import datetime

import discord
from discord.ext import commands


class role_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role_info")
    async def _role_info(self, ctx, role: discord.Role = None):
        if role is None:
            await ctx.send("もしかして:idを指定していない")
        else:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            kazu = len(role.members)
            role_member = "Members:"
            for mem in role.members:
                role_member += f"{mem.name}#{mem.discriminator}、"
            embed_role = discord.Embed(
                title=f"-----**Role Info**-----\n**{role.name}({role.id})**",
                color=role.colour)
            if role.name == "@everyone":
                embed_role.add_field(name="Role Name", value="everyone")
            else:
                embed_role.add_field(name="Role Name", value=role.name)
            embed_role.add_field(name="Role ID", value=str(role.id))
            embed_role.add_field(name="Role at", value=role.guild)
            embed_role.add_field(name="Color", value=role.colour)
            embed_role.add_field(name="Count", value=kazu)
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
                    name="Members", value=role_member, inline=False)
            embed_role.set_footer(
                text=f'User ID：{ctx.author.id} Time：{time}',
                icon_url=ctx.guild.icon_url)  # チャンネル名,時刻,鯖のアイコンをセット
            await ctx.channel.send(embed=embed_role)

    @_role_info.error
    async def role_info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("roleを認識できませんでした。\nメンション、id、名前のいずれかの方法で指定してください")


def setup(bot):
    bot.add_cog(role_info(bot))
