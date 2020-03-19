import math
import sys

import discord
from discord.ext import commands

from help_def import hyojun_help

sys.path.append("../")


class send_help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def _help(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):  # dmだったらreturn
            return

        react_list = [
            "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",  # 1
            "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",  # 2
            "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",  # 3
            "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",  # 4
            "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",  # 5
            "\N{BLACK LEFT-POINTING TRIANGLE}",  # 戻る
            "\N{BLACK RIGHT-POINTING TRIANGLE}",  # 進む
            "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}"]  # stop
        sen = "-------"

        help_kazu = len(hyojun_help)  # ヘルプの数を出す
        n = math.ceil(help_kazu / 5)  # 5で割って何ページになるか測定.小数点は繰り上げ

        embed = discord.Embed(
            title=f"標準のhelp 1/{n}",
            description="")
        for i in range(5):
            embed.add_field(
                name=hyojun_help[i]["name"],
                value=f'{hyojun_help[i]["value"]}\n{sen}',
                inline=False)

        msg = await ctx.send(embed=embed)

        for react in react_list:
            await msg.add_reaction(react)  # リアクション付与


def setup(bot):
    bot.add_cog(send_help(bot))
