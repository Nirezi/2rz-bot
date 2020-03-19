import discord

from discord.ext import commands


class bot_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bot_info")
    async def _bot_info(self, ctx):
        client = self.bot

        kazu = len(client.guilds)
        guild_name = ""
        for guild in client.guilds:
            guild_name += f"{guild.name}、"
        guild = f"このbotは{guild_name}以上{kazu}個のサーバに入っています"

        role_name = ""
        for role in ctx.guild.me.roles[1:]:
            role_name += f"{role.name}、"
        role_kazu = len(ctx.guild.me.roles[1:])
        botRole = f"このbotは{role_name}以上{role_kazu}個のroleを持っています"

        em_bot = discord.Embed(
            title=f"Hi! I'm{client.user}!",
            description="powered by discord.py\ndisneyresidents#8709 made me!")
        em_bot.set_thumbnail(url=client.user.avatar_url)  # ユーザーアバターをセット
        em_bot.add_field(name="Name", value=f"{client.user}")
        em_bot.add_field(name="ID", value=client.user.id)
        em_bot.add_field(name="Guilds", value=guild, inline=False)
        em_bot.add_field(name="Roles", value=botRole, inline=False)

        await ctx.send(embed=em_bot)


def setup(bot):
    bot.add_cog(bot_info(bot))
