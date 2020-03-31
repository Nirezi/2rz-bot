import math
import sys

from discord.ext import commands

from help_def import hyojun_help
import discord

sys.path.append("../")


class raw_reaction_add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)  # チャンネル取得
        msg = await channel.fetch_message(payload.message_id)  # リアクションの付いたメッセージ取得
        user = self.bot.get_user(payload.user_id)  # リアクションをつけたメッセージ取得

        if msg.author != self.bot.user:  # 2レジbotのメッセージに付いたか
            return

        if user.bot:
            return

        if not msg.embeds:
            return

        if msg.embeds:
            if not msg.embeds[0].title.startswith("標準のhelp"):
                return

        if isinstance(msg.channel, discord.DMChannel):  # dmだったら
            return

        embed = msg.embeds[0]
        list = embed.title.split()
        page = int(list[1].split("/")[0])
        help_name = list[0]
        no_img = "https://cdn.discordapp.com/attachments/688401587823050787/688401606512869376/YhyUGSJ0vEEZnh33jDHaqhYiB6f5erABoMcJu2bdv-mwkS08Syf29Kefr50kdGcpVjADOjNLgzFiZYJ_Nn6FGmmTMSWWAG78cPWG.png"

        kazu = len(hyojun_help)
        max_page = math.ceil(kazu / 5)  # 5で割って繰り上げ

        sen = "-------"
        emoji = str(payload.emoji)  # ここから本処理
        await msg.remove_reaction(emoji, user)  # リアクション削除
        react_list = ["\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
                      "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}"]
        if emoji in react_list:  # 数字のリアクションが付いたら
            embed = discord.Embed(title=f"{help_name} {page}/{max_page}", description="")
            for i in range(5):
                n = 5 * page - 5 + i
                if n > kazu:  # nがヘルプの数より多くなったら
                    break
                embed.add_field(
                    name=hyojun_help[n]["name"],
                    value=f'{hyojun_help[n]["value"]}\n{sen}',
                    inline=False)
            num = 5 * page - 5 + react_list.index(emoji)
            embed.add_field(
                name="Info",
                value=hyojun_help[num]["info"])
            if hyojun_help[num]["image"] == "None":  # コマンドの画像を追加
                embed.set_image(url=no_img)
            else:
                embed.set_image(url=hyojun_help[num]["image"])

            await msg.edit(embed=embed)

        if emoji == u"\u25C0" or emoji == u"\u25B6":  # 進むか戻るリアクションだったら
            if emoji == u"\u25C0":  # 進むリアクションだったら
                if page == 1:
                    next_page = max_page
                else:
                    next_page = page - 1

            if emoji == u"\u25B6":  # 戻るリアクションだったら
                if page == max_page:
                    next_page = 1
                else:
                    next_page = page + 1

            embed = discord.Embed(title=f"{help_name} {next_page}/{max_page}", description="")
            for i in range(5):
                n = 5 * next_page - 5 + i
                if n > kazu:  # nがヘルプの数より多くなったら
                    break
                embed.add_field(
                    name=hyojun_help[n]["name"],
                    value=f'{hyojun_help[n]["value"]}\n{sen}',
                    inline=False)
            await msg.edit(embed=embed)

        if emoji == "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}":  # 削除のリアクションだったら
            await msg.delete()


def setup(bot):
    bot.add_cog(raw_reaction_add(bot))
