import discord
from discord.ext import commands


class maguro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # client = self.bot
        mcs = message.channel.send
        mention = message.author.mention

        if message.author.bot:  # botのメッセージなら無視する
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.content.startswith("!"):
            return

        if message.guild.id == 610309046851076121:  # マグロ610309046851076121:
            if message.content == "/join":  # role付与
                if message.channel.id == 634295841729019904:  # コマンド用
                    role = discord.utils.get(
                        message.guild.roles, id=610430547109347339)  # 参加者
                    role2 = discord.utils.get(
                        message.guild.roles, id=665853511740948500)  # 新規
                    await message.author.remove_roles(role2)
                    await message.author.add_roles(role)  # role付与
                    msg = ("役職を付与しました")
                    await mcs(msg)
                else:
                    msg = f"{mention}ここで実行しないでください！"
                    await mcs(msg)


def setup(bot):
    bot.add_cog(maguro(bot))
