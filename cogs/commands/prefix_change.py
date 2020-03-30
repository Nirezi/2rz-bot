import os

import psycopg2
from discord.ext import commands

try:
    import tokens
    local = True
except ModuleNotFoundError:
    local = False

if local:
    SQLpath = tokens.PostgreSQL
else:
    SQLpath = os.environ["postgre"]
db = psycopg2.connect(SQLpath)
cur = db.cursor()


class prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.prefix}prefix [change, default, show]")

    @prefix.command()
    async def change(self, ctx, new_prefix):
        cur.execute("select * from prefixes WHERE guild_id = %s", (ctx.guild.id,))
        kazu = len(cur.fetchall())
        if kazu == 0:
            cur.execute("INSERT INTO prefixes values (%s, %s)", (ctx.guild.id, new_prefix))
            await ctx.send(f"prefixが`/`から`{new_prefix}`に変更されました")
        else:
            cur.execute("DELETE FROM prefixes WHERE guild_id = %s", (ctx.guild.id,))
            cur.execute("INSERT INTO prefixes values (%s, %s)", (ctx.guild.id, new_prefix))
            await ctx.send(f"prefixが`{ctx.prefix}`から`{new_prefix}`に変更されました")
        db.commit()

    @prefix.command()
    async def default(self, ctx):
        cur.execute("DELETE FROM prefixes WHERE guild_id = %s", (ctx.guild.id,))
        cur.execute("INSERT INTO prefixes values (%s, '/')", (ctx.guild.id,))
        db.commit()
        await ctx.send("prefixがデフォルトの`/`に変更されました")

    @prefix.command()
    async def show(self, ctx):
        cur.execute("select * from prefixes WHERE guild_id = %s", (ctx.guild.id,))
        kazu = len(cur.fetchall())
        if kazu == 0:
            await ctx.send(f"{ctx.guild.name}でのprefixは`/`です")
        else:
            cur.execute(
                "select * from prefixes WHERE guild_id = %s", (ctx.guild.id,))
            pre = ""
            for row in cur.fetchall():
                pre += row[1]
            await ctx.send(f"{ctx.guild.name}でのprefixは`{pre}`です")


def setup(bot):
    bot.add_cog(prefix(bot))
