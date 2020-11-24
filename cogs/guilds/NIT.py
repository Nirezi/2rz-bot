import discord
from discord.ext import commands


class NIT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.channel.id == 776641961854763058:
            if message.content.startswith(("#", "//", "--")):
                return
            category = self.bot.get_channel(776641214681841686)
            ch = await message.guild.create_text_channel(name=message.content, category=category)
            embed = discord.Embed(description=f"{message.author.mention}->{ch.mention}を作成しました")
            await message.channel.send(embed=embed)

        if message.channel.category_id:
            if message.channel.category_id == 776641214681841686:
                await message.channel.edit(position=0)


def setup(bot):
    bot.add_cog(NIT(bot))
