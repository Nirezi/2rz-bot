from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord


class member_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild.id
        client = self.bot
        if server == 610309046851076121:  # マグロ
            if member.id == 453874448035086337:  # けろとり
                await member.guild.kick(member)  # キック
            else:
                channel = client.get_channel(627555580013314049)  # 参加時のメッセージ用
                role = discord.utils.get(member.guild.roles, id=665853511740948500)  # 新規
                await member.add_roles(role)
                await channel.send(f"いらっしゃい!{member.mention}さん！ :tada:\n<#630402461395451913>を読んでください！")

        if server == 621326525521723414:  # 2rezi
            channel = client.get_channel(625288084648361993)  # 参加時のメッセージ用
            welcome = f"2レジ鯖へようこそ！{member.mention}さん :tada:\n"
            welcome += "<#672010326077734922>でコマンドを入力してください！\n"
            welcome += "整地鯖やってる人はmcidも<#621328380620701736>でお願いします"
            # mcid申請のch
            await channel.send(welcome)

        if server == 615394790669811732:  # タコ柴
            channel = client.get_channel(615394790669811734)  # join
            welcome = f"{member.guild.name}へようこそ！{member}さん:tada:"
            await channel.send(welcome)

        if server == 551006363698855946:  # ホワイト
            channel = client.get_channel(551006739991101441)
            msg = f"ホワイト鯖へようこそ！{member.mention}さん:tada:\n<#561329340311404554>を読んで楽しく過ごしましょう！"
            await channel.send(msg)

        if server == 684397318602096662:  # 民主主義
            channel = client.get_channel(686862095760883723)
            await channel.send(f"ようこそ{member}さん！")


def setup(bot):
    bot.add_cog(member_join(bot))
