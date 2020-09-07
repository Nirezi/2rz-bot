from discord.ext import commands


class ReZero(commands.Cog, name="rezero"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.guild.id != 718784794422411354:
            return

        if message.attachments:
            images = [await image.to_file() for image in message.attachments]
            ch = self.bot.get_channel(718792795300692001)
            if message.channel == ch:
                return
            await ch.send(files=images)


def setup(bot):
    bot.add_cog(ReZero(bot))
