from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == 662503350633365515:
            ch_dic = {
                669850293407842305: 669850327599546389,
                669850376341815347: 669850400039370762
            }
            if before.channel is None:
                if after.channel.id not in ch_dic.keys():
                    return
                ch = self.bot.get_channel(ch_dic[after.channel.id])
                await ch.send(f"{member}が{after.channel}に参加しました")
            if after.channel is None:
                if before.channel.id not in ch_dic.keys():
                    return
                ch = self.bot.get_channel(ch_dic[before.channel.id])
                await ch.send(f"{member}が{before.channel}にから離脱しました")

            #if after.channel and before.channel:
            #    if after.channel.id not in ch_dic.keys():
            #        return
            #    after_ch = self.bot.get_channel(ch_dic[after.channel.id])
            #    before_ch = self.bot.get_channel(ch_dic[before.channel.id])
            #    await after_ch.send(f"{member}が{before.channel}から{after.channel}に移動してきました")
            #    await before_ch.send(f"{member}が{before.channel}から{after.channel}に移動しました")


def setup(bot):
    bot.add_cog(Voice(bot))
