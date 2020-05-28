from discord.ext import commands
import discord


class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.message_id == 715522131760513096:
            role = discord.utils.get(guild.roles, id=715522634775003137)
            await member.add_roles(role)


def setup(bot):
    bot.add_cog(Reaction(bot))
