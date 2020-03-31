from discord.ext import commands


class bot_join_rem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        client = self.bot
        channel = client.get_channel(658685450805968906)
        msg = f"{client.user}が{guild.name}に参加しました"
        await channel.send(msg)

        msg = f"{client.user}を導入していただきありがとうございます！！\n"
        msg += "disneyresidents#8709制作のbotです!\n"
        msg += "ヘルプは/helpで確認できます！\n"
        msg += "本botはcustom prefixに対応しています！/prefix change new_prefixで設定できます"

        for channel in guild.text_channels:
            try:
                await channel.send(msg)
                break
            except Exception:
                continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        client = self.bot
        channel = client.get_channel(658685450805968906)
        msg = f"{client.user}が{guild.name}からbanまたはkickされました"
        await channel.send(msg)


def setup(bot):
    bot.add_cog(bot_join_rem(bot))
