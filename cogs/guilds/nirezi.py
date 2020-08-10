import random
import re
import sys

import bs4
import discord
import requests
from discord.ext import commands  # Bot Commands Frameworkのインポート

# from datetime import datetime

sys.path.append('../')


class Nirezi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        # local = self.bot.local
        mcs = message.channel.send
        mention = message.author.mention
        # now = datetime.now()
        # time = now.strftime("%Y/%m/%d %H:%M:%S")

        if message.author.bot:  # botのメッセージなら無視する
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.content.startswith("!"):
            return

        if message.guild.id == 621326525521723414:  # 2レジ鯖

            # unnei_ca = [621334345579364372, 621326525521723418, 649193418492215306]  # お知らせ、はじめに、logs
            # unnei_ch = [621330963938410496, 625591106989588480, 643040530921553940]  # 運営用、運営用コマンド、やることリスト
            # testyou = [627867724541853716, 632944517934481409]
            # log_ch = client.get_channel(640587255332732938)  # log用ch

            if message.channel.id == 663636102145507330:  # mcチャットのとこは弾く
                return

            if message.channel.id == 621328380620701736:  # mcid申請のch
                mcid_a = f'{message.content}'.replace('\\', '')
                p = re.compile(r'^[a-zA-Z0-9_]+$')
                if p.fullmatch(message.content):
                    mcid = mcid_a.lower()
                    url = f"https://w4.minecraftserver.jp/player/{mcid}"
                    try:
                        res = requests.get(url)
                        res.raise_for_status()
                        soup = bs4.BeautifulSoup(res.text, "html.parser")
                        td = soup.td
                        if f'{mcid}' in f'{td}':
                            mcid_log_ch = client.get_channel(660809650027102209)
                            async for msg in mcid_log_ch.history():
                                mcid_log = msg.content[19:]
                                if mcid_log == mcid_a:
                                    faild = discord.Embed(description=f"{message.author}さん\n{mcid_a}はすでに報告されています、もしこれがバグなら2レジまで報告してください",
                                                          color=0xff0000)
                                    await mcs(embed=faild)
                                    return
                            role = discord.utils.get(message.guild.roles, id=672006791474708490)
                            rinnzi = discord.utils.get(message.guild.roles, id=660825080602820618)
                            emoji = ['👍', '🙆']
                            await message.author.add_roles(role)
                            await message.author.add_roles(rinnzi)
                            await message.add_reaction(random.choice(emoji))
                            color = [0x3efd73, 0xfb407c, 0xf3f915, 0xc60000, 0xed8f10, 0xeacf13, 0x9d9d9d, 0xebb652, 0x4259fb, 0x1e90ff]
                            embed_mcid = discord.Embed(description=f'{message.author.display_name}のMCIDの報告を確認したよ！',
                                                       color=random.choice(color))
                            embed_mcid.add_field(name="MCID", value=mcid_a)
                            embed_mcid.set_author(name=message.author, icon_url=message.author.avatar_url, )  # ユーザー名+ID,アバターをセット
                            channel = client.get_channel(646691005030203410)
                            await channel.send(embed=embed_mcid)
                            await mcid_log_ch.send(f"{message.author.id} {mcid_a}")
                        else:
                            embed = discord.Embed(
                                description=f'{message.author} さん。\n入力されたMCIDは実在しないか、又はまだ一度も整地鯖にログインしていません。\n続けて間違った入力を行うと規定によりBANの対象になることがあります。',
                                color=0xff0000)
                            await message.channel.send(embed=embed)
                    except requests.exceptions.HTTPError:
                        await message.channel.send('requests.exceptions.HTTPError')
                else:
                    embed = discord.Embed(
                        description="MCIDに使用できない文字が含まれています'\n続けて間違った入力を行うと規定によりBANの対象になることがあります。",
                        color=0xff0000)
                    await message.channel.send(embed=embed)

            if message.content.startswith("/mcid"):
                id = int(message.content[5:])
                user = client.get_user(id)
                mcid_reported = f"{user}さんのmcid\n"
                kazu = 0
                mcid_log_ch = client.get_channel(660809650027102209)
                if user is not None:
                    flag = False
                    async for msg in mcid_log_ch.history():
                        mcid_log = await mcid_log_ch.fetch_message(msg.id)
                        if mcid_log.content.startswith(str(id)):
                            mcid_log2 = mcid_log.content[19:]
                            mcid_reported += f"{mcid_log2}\n"
                            kazu += 1
                            flag = True
                    if not flag:
                        await mcs(f"{user}さんはまだmcidを報告していません")
                    else:
                        await mcs(f"{mcid_reported}以上{kazu}個のmcidが報告されています")
                else:
                    await mcs("その方はこのサーバーにいません")

            if message.content == "/join":
                if message.channel.id == 672010326077734922:
                    role = discord.utils.get(message.guild.roles, id=621329653763932160)
                    await message.author.add_roles(role)
                    await mcs(f"{mention}役職を付与しました")
                else:
                    await mcs("ここで実行しないでください！！")

            if "discord.gg" in message.content:
                list = [621326525521723418, 621334345579364372, 621330415348613160, 621330763089969152, 649193418492215306]
                if message.channel.id == 621328600972525578 or message.channel.category_id in list:
                    pass
                else:
                    await message.delete()
                    await mcs(f"{mention}\n指定されたチャンネル以外で招待リンクを貼る行為は禁止されています")
                    await mcs("削除しました")

            if message.channel.id == 658686103276093440:  # dm用のチャンネル
                user_id = message.content[:18]
                user = client.get_user(int(user_id))
                content = message.content[18:]
                await user.send(content)

            if message.content == "/delmsg":  # メッセージ削除
                if discord.utils.get(message.author.roles, id=621326896554311700):  # 2rz以外弾く
                    await message.channel.purge()
                else:
                    await mcs("何様のつもり？")

            if message.content.startswith("/delmsg"):
                kazu = len(message.content[7:])
                if discord.utils.get(message.author.roles, id=621326896554311700):
                    if kazu >= 1:
                        await message.channel.purge(limit=kazu)

            if message.content == "/test":
                await mcs("say hello!")

                def check(m):
                    return m.content == "hello" and m.channel == message.channel

                msg = await client.wait_for("message", check=check)
                await mcs("hello!")


def setup(bot):
    bot.add_cog(Nirezi(bot))
