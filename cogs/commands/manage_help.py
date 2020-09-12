import asyncio

import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_aliase(command: commands.core.Command) -> str:
        if not command.aliases:
            raise TypeError("command passed don't have aliase")
        aliases = " | ".join(command.aliases)
        return f"[{aliases}]"

    @staticmethod
    def get_subcommand(parent: commands.core.Group) -> str:
        if not isinstance(parent, commands.core.Group):
            raise TypeError("didn't passed commands.Group")
        subcommands = "/".join(c.name for c in parent.commands)
        return subcommands

    @commands.command(name="help")
    @commands.bot_has_permissions(add_reactions=True, manage_messages=True)
    async def _help(self, ctx, cmd=None):
        """ヘルプを送信"""
        if cmd is not None:
            command = self.bot.get_command(cmd)
            if command is None:
                return await ctx.send(f"おっと、`{cmd}`は見つかりません！")

        cog_dic = dict(self.bot.cogs).copy()
        cog_dic.pop("Jishaku")
        cogs = [v for k, v in cog_dic.items() if v.qualified_name[0].isupper()]
        max_page = len(cogs)

        count = 0
        for cog in cogs:
            for cmd in cog.get_commands():
                if isinstance(cmd, commands.core.Group):
                    count += len(cmd.commands)
                else:
                    count += 1

        def page_setup(page: int) -> discord.Embed:
            """ページ数に対応したhelp内容をセット"""
            page -= 1
            embed = discord.Embed(title=f"Page {page+1}/{max_page} ({count} commands)",
                                  description=f"より詳細なヘルプは[公式サーバ]({self.bot.guild_invite_url})まで!")
            cog = cogs[page]
            embed.add_field(name=cog.qualified_name, value=cog.description)

            for cmd in cog.get_commands():
                if cmd.hidden or not cmd.enabled:
                    continue
                if cmd.aliases:
                    embed.add_field(name=f"{cmd.name} {self.get_aliase(cmd)}", value=cmd.help, inline=False)
                else:
                    embed.add_field(name=f"{cmd.name}", value=cmd.help, inline=False)
            return embed

        react_list = [
            u"\u25C0",  # 戻る
            u"\u25B6",  # 進む
            "\U0001f522",  # 1234
            "\U00002139\U0000fe0f",  # インフォメーションマーク
            "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}"  # stop
        ]

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
                return True
            else:
                return False

        while not self.bot.is_closed():
            try:
                react, user = await self.bot.wait_for("reaction_add", check=check, timeout=300)
            except asyncio.TimeoutError:
                await ctx.message.clear_reactions()
                break
            else:
                try:
                    emoji = str(react.emoji)
                    await msg.remove_reaction(emoji, user)
                    if emoji == u"\u25C0" or emoji == u"\u25B6":  # 進むか戻る
                        if emoji == u"\u25C0":  # 戻る
                            if page == 1:
                                page = max_page
                            else:
                                page -= 1

                        if emoji == u"\u25B6":  # 進む
                            if page == max_page:
                                page = 1
                            else:
                                page += 1

                        await msg.edit(embed=page_setup(page))

                    if emoji == "\U0001f522":  # 1234
                        def check_msg(m):
                            return m.author == ctx.author and m.channel == ctx.channel

                        await ctx.send("移動したいページ数を送信してください！", delete_after=30)
                        try:
                            m = await self.bot.wait_for("message", check=check_msg, timeout=30)
                            next_page = int(m.content)
                            await m.delete()
                        except asyncio.TimeoutError:
                            await msg.clear_reactions()
                            break
                        except TypeError:
                            await ctx.send("おっと、ページ数が整数じゃないみたいです", delete_after=5)
                            continue
                        else:
                            if not(1 <= next_page <= max_page):
                                await ctx.send(f"おっと、{next_page}ページはありません！", delete_after=5)
                                continue
                            page = next_page
                            await msg.edit(embed=page_setup(page))

                    if emoji == "\U00002139\U0000fe0f":  # iマーク
                        embed = discord.Embed(title="インフォメーション")
                        embed.add_field(name="各種リアクションのヘルプ",
                                        value=f"{react_list[0]}:一つ前のページに戻ります。最初のページで使用すると最後のページに移動します。\n\n"
                                              f"{react_list[1]}:一つ後ろのページに移動します。最後のページで使用すると最初のページに移動します。\n\n"
                                              f"{react_list[2]}:botのメッセージの後に、移動したいページを送信するとそのページに移動できます。\n\n"
                                              f"{react_list[3]}:このヘルプを表示します。10秒後に元のヘルプに自動的に戻ります。\n\n"
                                              f"{react_list[4]}:メッセージを削除します\n")
                        await msg.edit(embed=embed)
                        await asyncio.sleep(10)
                        await msg.edit(embed=page_setup(page))

                    if emoji == "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}":  # ■
                        await msg.delete()
                        break

                except IndexError:
                    await ctx.send("範囲外のリアクションが押されました", delete_after=3.0)
                    continue


def setup(bot):
    bot.add_cog(Help(bot))
