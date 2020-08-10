import sys

import discord
from discord.ext import commands

sys.path.append('../')


class ohatsu_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mcs = message.channel.send
        # mention = message.author.mention

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.guild.id == 612401848787140656:  # 082
            if message.channel.id == 622737485721763842:  # コマンド用
                list = ["/build", "/ohatsu", "/mine"]  # 役職のlist
                if message.content in list:
                    if message.content == "/build":  # 建築
                        role = discord.utils.get(message.guild.roles, id=622733795769974784)  # 建築
                        if discord.utils.get(message.author.roles, id=622733795769974784):
                            await message.author.remove_roles(role)
                            await mcs(f"{role.name}を剥奪しました")
                        else:
                            await message.author.add_roles(role)
                            await mcs(f"{role.name}を付与しました")

                    if message.content == "/ohatsu":  # お初支援
                        role = discord.utils.get(message.guild.roles, id=622740283062353960)
                        if discord.utils.get(message.author.roles, id=622740283062353960):
                            await message.author.remove_roles(role)
                            await mcs(f"{role.name}を剥奪しました")
                        else:
                            await message.author.add_roles(role)
                            await mcs(f"{role.name}を付与しました")

                    if message.content == "/mine":  # 採掘支援
                        role = discord.utils.get(message.guild.roles, id=622733571731488769)
                        if discord.utils.get(message.author.roles, id=622733571731488769):
                            await message.author.remove_roles(role)
                            await mcs(f"{role.name}を剥奪しました")
                        else:
                            await message.author.add_roles(role)
                            await mcs(f"{role.name}を付与しました")

            if message.content == "/delmsg_admin":  # メッセージ削除
                if discord.utils.get(message.author.roles, id=612402582379298817):
                    await message.channel.purge()
                else:
                    await mcs("who are you?")


def setup(bot):
    bot.add_cog(ohatsu_msg(bot))
