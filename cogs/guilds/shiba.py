import random
import re
import sys

import bs4
import discord
import requests
from discord.ext import commands

sys.path.append('../')


class Shiba(commands.Cog, name="shiba"):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        if ctx.guild.id == 615394790669811732:
            return True
        return False

    @commands.command(hidden=True)
    async def join_event(self, ctx):
        role = ctx.guild.get_role(762326681250824243)
        if role not in ctx.author.roles:
            await ctx.author.add_roles(role)
            await ctx.send(f"I added a role {role.name}")
        else:
            await ctx.send("You have already have the role")

    @commands.Cog.listener()
    async def on_message(self, message):
        """しばさんのサーバでのメッセージ"""
        if message.author.bot:  # botのメッセージなら無視する
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.content.startswith("!"):
            return

        client = self.bot
        server = message.guild.id
        mcs = message.channel.send

        mcid_role = discord.utils.get(
            message.guild.roles,
            id=615396751590948884)  # mcid申請済み

        if server == 615394790669811732 or server == 628182826914676758:  # たこ柴
            if message.channel.id == 615396581407064065:
                await mcidcheck(message, 648163940995432478, client, mcid_role)

            if message.content == "/tuuti":
                role = discord.utils.get(
                    message.guild.roles, id=661895702250520595)
                if role in message.author.roles:
                    await message.author.remove_roles(role)
                    await mcs("役職を剥奪しました")
                else:
                    await message.author.add_roles(role)
                    await mcs("役職を付与しました")

            if message.content == "/ch":
                link_ch = "整地鯖で遊んだり、ハイピでワイワイしたりしてます！良ければチャンネル登録してください！\nhttps://www.youtube.com/channel/UCUt79daiPlVvkeIjCBRvMtQ"
                await mcs(link_ch)

            if message.content == "/riku":
                riku = "https://twitter.com/takoshiba_riku"
                await mcs(riku)

            if message.content == "/tako":
                tako = "透き通るようなイケメンボイス、たこさんのTwitter\nhttps://twitter.com/Tako_san256"
                await mcs(tako)

            if message.content == "/shiba":
                shiba = "声帯バグってる男の娘、柴さんのTwitter\nhttps://twitter.com/shibatanienn13"
                await mcs(shiba)

            if message.content == "/studio":
                studio = "タコ柴の、公式ツイッターアカウントです\nhttps://twitter.com/tako_shiba_256"
                await mcs(studio)

            if message.content == "/iroha":
                iroha = "いろはさんのツイッターです\nhttps://twitter.com/irohachan_246"
                await mcs(iroha)

            if message.content == "たこさんはイケボ":
                await mcs("それな")

            if message.content == "たこさんは":
                await mcs("イケボ！")

            otoko = ["シバさんは", "しばさんは", "柴さんは"]
            if message.content in otoko:
                await mcs("男の娘")

            rikkun = ["りくさんは", "りくは", "りっくんは"]
            if message.content in rikkun:
                await mcs("ベリーかわいい")

            if message.content == "2レジは":
                await mcs("スタジオ専属の技術者だよ！")

            if message.content.startswith("/member") or message.content.startswith("/notmem-2rz"):  # これよりスタジオ限定
                try:
                    if message.content.startswith("/member") and not message.content == "/members":
                        if discord.utils.get(message.author.roles, id=632518980908744709) or\
                           discord.utils.get(message.author.roles, id=635770787760046081):
                            mem_id = int(message.content[7:])
                            role = discord.utils.get(message.guild.roles, id=632518980908744709)
                            user = message.guild.get_member(mem_id)
                            await user.add_roles(role)
                            await message.channel.send("役職をつけたよ!")
                        else:
                            await mcs("権限がありません")

                    if message.content.startswith("/notmem-2rz"):
                        if discord.utils.get(message.author.roles, id=635770787760046081):
                            mem_id = int(message.content[11:])
                            role = discord.utils.get(message.guild.mem_roles, id=632518980908744709)
                            user = message.guild.get_member(mem_id)
                            await user.remove_roles(role)
                            await message.channel.send("役職をはく奪しました")
                        else:
                            await mcs("権限がありません")

                except ValueError:
                    await mcs("idを指定してください")

            if message.content == "/notmember":
                if discord.utils.get(message.author.roles, id=632518980908744709):
                    role = discord.utils.get(message.guild.roles, id=632518980908744709)
                    await message.author.remove_roles(role)
                    await mcs(f"bye bye {message.author.name}さん、、")
                else:
                    await mcs("あなたはメンバーではありません")

            if message.content == "/tuuti-mem":
                if discord.utils.get(message.author.roles, id=632518980908744709):
                    if not discord.utils.get(message.author.roles, id=637264209012457502):
                        role = discord.utils.get(message.guild.roles, id=637264209012457502)
                        await message.author.add_roles(role)  # role付与
                        await mcs("通知用の役職をつけたよ！")
                    else:
                        role = discord.utils.get(message.guild.roles, id=637264209012457502)
                        await message.author.remove_roles(role)  # role剥奪
                        await mcs("通知用の役職を剥奪したよ、、")
                else:
                    await mcs("あなたはメンバーではありません")


async def mcidcheck(message, log_channel_id, client, role1, role2=None):
    mcid = message.content.replace('\\', '')
    p = re.compile(r'^[a-zA-Z0-9_]+$')
    if p.fullmatch(message.content):
        mcid = mcid.lower()
        url = f"https://w4.minecraftserver.jp/player/{mcid}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            td = soup.td
            if f'{mcid}' in f'{td}':
                emoji = ['👍', '🙆']
                await message.author.add_roles(role1)
                if role2 is not None:
                    await message.author.add_roles(role2)
                await message.add_reaction(random.choice(emoji))
                color = [
                    0x3efd73,
                    0xfb407c,
                    0xf3f915,
                    0xc60000,
                    0xed8f10,
                    0xeacf13,
                    0x9d9d9d,
                    0xebb652,
                    0x4259fb,
                    0x1e90ff]
                embed_mcid = discord.Embed(
                    description=f'{message.author.display_name}のMCIDの報告を確認したよ！',
                    color=random.choice(color))
                embed_mcid.add_field(name="MCID", value=mcid)
                embed_mcid.set_author(
                    name=message.author,
                    icon_url=message.author.avatar_url,
                )  # ユーザー名+ID,アバターをセット
                channel = client.get_channel(log_channel_id)
                await channel.send(embed=embed_mcid)
            else:
                embed = discord.Embed(
                    description=f'{message.author} さん。\n入力されたMCIDは実在しないか、又はまだ一度も整地鯖にログインしていません。\n\
                                                続けて間違った入力を行うと規定によりBANの対象になることがあります。', color=0xff0000)
                await message.channel.send(embed=embed)
        except requests.exceptions.HTTPError:
            await message.channel.send('requests.exceptions.HTTPError')
    else:
        embed = discord.Embed(
            description=f"{message.author}さん。\nMCIDに使用できない文字が含まれています'\n続けて間違った入力を行うと規定によりBANの対象になることがあります。",
            color=0xff0000)
        await message.channel.send(embed=embed)


def setup(bot):
    """cogを追加する"""
    bot.add_cog(Shiba(bot))
