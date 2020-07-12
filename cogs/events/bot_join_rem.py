from discord.ext import commands


class BotJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # guildまたはguild ownerがブラックリストに登録されていたらサーバから抜ける
        if self.bot.blacklist.is_key(guild.id) or self.bot.blacklist.is_key(guild.owner.id):
            await guild.leave()
            return

        channel = self.bot.get_channel(658685450805968906)
        msg = f"{self.bot.user}が{guild.name}に参加しました"
        await channel.send(msg)

        msg = f"{self.bot.user}を{guild.name}に導入していただきありがとうございます！！\n" \
              f"{self.bot.get_user(self.bot.owner_id)}制作のbotです\n" \
              f"ヘルプは/helpから確認してください\n"\
              "本botはcustom prefixに対応しています`/prefix change 新しいprefix`で設定できます" \
              "他のbotとprefixがかぶってしまう場合は是非ご利用ください(サーバ管理の権限が必要です)" \
              f"サポートサーバへの参加をお願いします！\n{self.bot.guild_invite_url}"

        if guild.system_channel is not None:
            try:
                return await guild.system_channel.send(msg)
            except Exception:
                pass

        for channel in guild.text_channels:
            try:
                return await channel.send(msg)
            except Exception:
                continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(658685450805968906)
        msg = f"{self.bot.user}が{guild.name}から抜けました"
        await channel.send(msg)


def setup(bot):
    bot.add_cog(BotJoinLeave(bot))
