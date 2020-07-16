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
    @commands.bot_has_permissions(add_reactions=True, manage_messages=True)
    async def _help(self, ctx):
        """ヘルプを送信"""
        if isinstance(ctx.channel, discord.DMChannel):  # dmだったらreturn
            return

        def page_setup(page: int) -> discord.Embed:
            """ページ数に対応したhelp内容をセット"""
            help_embed = discord.Embed(title=f"標準のhelp {page}/{max_page}", description="")
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

        react_list = [
            "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",  # 1
            "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",  # 2
            "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",  # 3
            "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",  # 4
            "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",  # 5
            "\N{BLACK LEFT-POINTING TRIANGLE}",  # 戻る
            "\N{BLACK RIGHT-POINTING TRIANGLE}",  # 進む
            "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}"]  # stop

        num_list = ["\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
                    "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
                    "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
                    "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
                    "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}"]

        sen = "-------"
        no_img = "https://cdn.discordapp.com/attachments/688401587823050787/688401606512869376/YhyUGSJ0vEEZnh33jDHaqhYiB6f5erABoMcJu2bdv-mwkS08Syf29Kefr50kdGcpVjADOjNLgzFiZYJ_Nn6FGmmTMSWWAG78cPWG.png"

        help_count = len(hyojun_help)  # ヘルプの数を出す
        max_page = math.ceil(help_count / 5)  # 5で割って何ページになるか測定.小数点は繰り上げ

        page = 1
        msg = await ctx.send(embed=page_setup(page))

        for react in react_list:
            await msg.add_reaction(react)  # リアクション付与

        def check(reaction, user):
            if reaction.message.id != msg.id:
                return False
            elif ctx.author.bot or user != ctx.author:
                return False
            elif str(reaction.emoji) in react_list:
                return reaction, user
            else:
                return False

        while not self.bot.is_closed():
            try:
                react, user = await self.bot.wait_for("reaction_add", check=check, timeout=300)
            except asyncio.TimeoutError:
                await ctx.message.clear_reactions()
                break
            else:
                emoji = str(react.emoji)
                await msg.remove_reaction(emoji, user)
                if emoji in react_list[:5]:  # 数字のリアクションが付いたら
                    embed = page_setup(page)
                    num = 5 * page - 5 + react_list.index(emoji)
                    if num > help_count:
                        await ctx.send("範囲外のリアクションが押されました", delete_after=3.0)
                        continue
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
                        if page == 1:
                            page = max_page
                        else:
                            page -= 1

                    if emoji == u"\u25B6":  # 進むリアクションだったら
                        if page == max_page:
                            page = 1
                        else:
                            page += 1

                    await msg.edit(embed=page_setup(page))

                if emoji == "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}":  # 削除のリアクションだったら
                    await msg.delete()


def setup(bot):
    bot.add_cog(ManageHelp(bot))
