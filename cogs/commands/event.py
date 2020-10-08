import random

import discord
from discord.ext import commands


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        if ctx.guild.id == 621326525521723414:
            return True
        return False

    @commands.command(name="join", hidden=True)
    @commands.has_role(672006791474708490)
    async def _join(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=629828134820380682)
        if role in ctx.author.roles:
            return await ctx.send("(´・ω・｀)もう参加してるじゃん")
        await ctx.author.add_roles(role)
        await ctx.send("役職を付与しました！発表をお楽しみに！")

    @commands.command(hidden=True)
    @commands.has_role(621326896554311700)
    async def choice(self, ctx):
        async with ctx.typing():
            role = discord.utils.get(ctx.guild.roles, id=629828134820380682)
            winner_role = discord.utils.get(ctx.guild.roles, id=746988608728072293)
            winners = random.sample(role.members, 16)
            embed = discord.Embed(title="当選発表！")
            text = ""
            for i, user in enumerate(winners):
                if i == 0:
                    text += "2st(1)\n"
                elif i == 1:
                    text += "1st(1)\n"
                elif i == 2:
                    text += "32(2)\n"
                elif i == 4:
                    text += "16(4)\n"
                elif i == 8:
                    text += "8(8)\n"
                text += f"{user.mention}\n"
                await user.add_roles(winner_role)
            else:
                text += "参加賞\nその他の方"
            embed.add_field(name="当選者", value=text)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Event(bot))
