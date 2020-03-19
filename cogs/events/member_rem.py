from discord.ext import commands


class member_rem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        client = self.bot
        if member.guild.id == 621326525521723414:  # 2rezi
            channel = client.get_channel(625288084648361993)  # 参加時のメッセージ用
            msg = f"{member}さん、さようなら、、、:sob:"
            await channel.send(msg)

        if member.guild.id == 684397318602096662:  # 民主主義
            channel = client.get_channel(686862095760883723)
            await channel.send(f"{member}さんが退出しました")


def setup(bot):
    bot.add_cog(member_rem(bot))
