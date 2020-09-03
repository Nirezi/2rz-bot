from discord.ext import commands


class OU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild.id != 675314750783094806:
            return
        if message.channel.id == 750997955145629796:
            reacts = ["\U0001f44d", "\U0001f44e"]
            for react in reacts:
                await message.add_reaction(react)


def setup(bot):
    bot.add_cog(OU(bot))
