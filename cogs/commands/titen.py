import sys

import discord
from discord.ext import commands

from citycodes_dic import citycodes_dic

sys.path.append('../')


class titen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="titen")
    async def _titen(self, ctx):
        titen_str = ""
        for titen in citycodes_dic.keys():
            titen_str += f"{titen}、"

        embed = discord.Embed(title="天気がわかる地点はこちらです", description=titen_str)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(titen(bot))
