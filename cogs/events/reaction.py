from discord.ext import commands
import discord


class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)

        if payload.message_id == 715522131760513096:
            role = discord.utils.get(guild.roles, id=715522634775003137)
            await member.add_roles(role)

        if payload.message_id == 717281211172651108:
            reaction = str(payload.emoji)
            # await msg.remove_reaction(reaction, member)
            react_list = [
                "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
                "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
                "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
                "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
                "\N{REGIONAL INDICATOR SYMBOL LETTER C}"
            ]

            role_id_list = [
                715121037888716841,
                715161954112503849,
                715162738174853140,
                715162741295284315,
                715163255865081916
            ]

            if [role.name for role in member.roles[1:] if role.id in role_id_list]:
                return await channel.send("あなたは既にroleを持っています", delete_after=4.0)

            if reaction not in react_list:
                return

            n = react_list.index(reaction)
            role = discord.utils.get(guild.roles, id=role_id_list[n])
            await member.add_roles(role)
            embed = discord.Embed(title="", description=f"{member.mention}, {role.mention}を付与しました")
            await channel.send(embed=embed, delete_after=4.0)


def setup(bot):
    bot.add_cog(Reaction(bot))
