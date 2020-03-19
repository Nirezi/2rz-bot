from discord.ext import commands


class bot_join_rem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        client = self.bot
        channel = client.get_channel(658685450805968906)
        ni_men = "<@544774774405201923>"
        msg = f"{client.user}が{guild.name}に参加しました"
        await channel.send(msg)

        msg = f"{client.user}を導入していただきありがとうございます！！\n\
              {ni_men}制作のbotです\n\
              <#662524364469567528>の利用規約は読みましたか？\n\
              読んでいない、もしくは見れない場合は https://discord.gg/n3QXg6H のサーバに入ってください！！\n\
              管理者の方はこの利用規約についてこのサーバのメンバーに周知させてください\
              **__このbotに過度に負荷をかける行為は遠慮していただきますようお願いします__**"
        for channel in guild.text_channels:
            try:
                await channel.send(msg)
                break
            except BaseException:
                continue

        invites = await guild.invites()
        dm = client.get_user(544774774405201923)
        try:
            await dm.send(f"{invites[0]}\n{guild.name}に{client.user}が参加しました")
        except IndexError:
            await dm.send(f"{client.user}が{guild.name}に参加しましたが、招待リンクが存在しませんでした")
            channel = guild.text_channels[0]
            create_invite = await channel.create_invite(reason="botの作成者用。一回限り",
                                                        max_uses=1)
            await dm.send(f"{create_invite}\nので作成しました")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        client = self.bot
        channel = client.get_channel(658685450805968906)
        msg = f"{client.user}が{guild.name}からbanまたはkickされました"
        await channel.send(msg)


def setup(bot):
    bot.add_cog(bot_join_rem(bot))
