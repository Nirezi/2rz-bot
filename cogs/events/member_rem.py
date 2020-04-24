from discord.ext import commands


class MemberRem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        client = self.bot
        if member.guild.id == 621326525521723414:  # 2rezi
            channel = client.get_channel(625288084648361993)  # 参加時のメッセージ用
            msg = f"{member}さん、さようなら、、、:sob:"
            await channel.send(msg)

        if member.guild.id == 562820886323789835:
            channel = client.get_channel(681423204811800609)
            await channel.send(f"{member}が退出しました")

        if member.guild.id == 675314750783094806:
            ch = client.get_channel(675346242762702848)
            await ch.send(f"{member}が退出しました")

        if member.guild.id == 700880842309894175:  # 2レジbot公式サーバ
            ch = client.get_channel(700880842309894178)
            await ch.send(f"{member}さん、さようなら:sob:")


def setup(bot):
    bot.add_cog(MemberRem(bot))
