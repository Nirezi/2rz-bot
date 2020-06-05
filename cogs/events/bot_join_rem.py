from discord.ext import commands


class BotJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # guildまたはguild ownerがブラックリストに登録されていたらサーバから抜ける
        if guild.id in self.bot.blacklist.keys() or guild.owner.id in self.bot.blacklist.keys():
            await guild.leave()
            return

        client = self.bot
        channel = client.get_channel(658685450805968906)
        msg = f"{client.user}が{guild.name}に参加しました"
        await channel.send(msg)

        msg = f"{client.user}を{guild.name}に導入していただきありがとうございます！！\n" \
              f"disneyresidents#8709制作のbotです\n" \
              f"ヘルプは/helpから確認してください\n"\
              "本botはcustom prefixに対応しています`/prefix change new_prefix`で設定できます" \
              "https://discord.gg/bQWsu3Z 本botのサポートサーバはこちらです、入ってくれると喜びます()"

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
    bot.add_cog(BotJoinLeave(bot))
