import asyncio
import math
import sys

import discord
from discord.ext import commands

from help_def import hyojun_help

sys.path.append("../")


class ManageHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def _help(self, ctx):
        """ヘルプを送信"""
        if isinstance(ctx.channel, discord.DMChannel):  # dmだったらreturn
            return

        react_list = [
            "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",  # 1
            "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",  # 2
            "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",  # 3
            "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",  # 4
            "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",  # 5
            "\N{BLACK LEFT-POINTING TRIANGLE}",  # 戻る
            "\N{BLACK RIGHT-POINTING TRIANGLE}",  # 進む
            "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}"]  # stop
        sen = "-------"

        help_count = len(hyojun_help)  # ヘルプの数を出す
        n = math.ceil(help_count / 5)  # 5で割って何ページになるか測定.小数点は繰り上げ

        embed = discord.Embed(
            title=f"標準のhelp 1/{n}",
            description="")
        for i in range(5):
            embed.add_field(
                name=hyojun_help[i]["name"],
                value=f'{hyojun_help[i]["value"]}\n{sen}',
                inline=False)

        msg = await ctx.send(embed=embed)

        for react in react_list:
            await msg.add_reaction(react)  # リアクション付与

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)  # チャンネル取得
        msg = await channel.fetch_message(payload.message_id)  # リアクションの付いたメッセージ取得
        user = self.bot.get_user(payload.user_id)  # リアクションをつけたメッセージ取得

        if msg.author != self.bot.user:  # 2レジbotのメッセージにつかなかったか
            return

        if user.bot:
            return

        if not msg.embeds:
            return

        if msg.embeds:
            if msg.embeds[0].title == "":
                return

            if not msg.embeds[0].title.startswith("標準のhelp"):
                return

        if isinstance(msg.channel, discord.DMChannel):  # dmだったら
            return

        embed = msg.embeds[0]
        _list = embed.title.split()
        now_page = int(_list[1].split("/")[0])
        help_name = _list[0]
        no_img = "https://cdn.discordapp.com/attachments/688401587823050787/688401606512869376/YhyUGSJ0vEEZnh33jDHaqhYiB6f5erABoMcJu2bdv-mwkS08Syf29Kefr50kdGcpVjADOjNLgzFiZYJ_Nn6FGmmTMSWWAG78cPWG.png"

        count = len(hyojun_help)
        max_page = math.ceil(count / 5)  # 5で割って繰り上げ

        def page_setup(page):
            """ページ数に対応したhelp内容をセット"""
            help_embed = discord.Embed(title=f"{help_name} {page}/{max_page}", description="")
            for i in range(5):
                n = 5 * page - 5 + i
                try:
                    help_embed.add_field(
                        name=hyojun_help[n]["name"],
                        value=f'{hyojun_help[n]["value"]}\n{sen}',
                        inline=False)
                except IndexError:
                    break
            return help_embed

        sen = "-------"
        emoji = str(payload.emoji)  # ここから本処理
        try:
            await msg.remove_reaction(emoji, user)  # リアクション削除
        except discord.Forbidden:
            await channel.send("botにリアクション管理の権限がないためリアクションを削除できませんでした\nサーバー管理者まで問い合わせてください")

        react_list = ["\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}"]
        if emoji in react_list:  # 数字のリアクションが付いたら
            embed = page_setup(now_page)
            num = 5 * now_page - 5 + react_list.index(emoji)
            if num > count:
                index_error_msg = await channel.send("範囲外のリアクションが押されました")
                await asyncio.sleep(5)
                await index_error_msg.delete()
                return
            embed.add_field(
                name="Info",
                value=hyojun_help[num]["info"])
            if hyojun_help[num]["image"] == "None":  # コマンドの画像を追加
                embed.set_image(url=no_img)
            else:
                embed.set_image(url=hyojun_help[num]["image"])

            await msg.edit(embed=embed)

        if emoji == u"\u25C0" or emoji == u"\u25B6":  # 進むか戻るリアクションだったら
            if emoji == u"\u25C0":  # 戻るリアクションだったら
                if now_page == 1:
                    next_page = max_page
                else:
                    next_page = now_page - 1

            if emoji == u"\u25B6":  # 進むリアクションだったら
                if now_page == max_page:
                    next_page = 1
                else:
                    next_page = now_page + 1

            embed = page_setup(next_page)
            await msg.edit(embed=embed)

        if emoji == "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}":  # 削除のリアクションだったら
            await msg.delete()


def setup(bot):
    bot.add_cog(ManageHelp(bot))
