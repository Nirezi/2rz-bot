import asyncio

import discord
from discord.ext import commands


class BotHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_aliase(command: commands.core.Command) -> str:
        if not command.aliases:
            return ""
        aliases = " | ".join(command.aliases)
        return f"[{aliases}]"

    @staticmethod
    def get_subcommand(parent: commands.core.Group) -> str:
        if not isinstance(parent, commands.core.Group):
            raise TypeError("didn't passed commands.Group")
        subcommands = "/".join(c.name for c in parent.commands)
        return subcommands

    def command_not_found(self, string):
        return f"おっと、{string}というコマンドはありません！"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group):
            return f"おっと、{string}というサブコマンドはありません！"
        return f"{command.name}にサブコマンドはありません！"

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True)
        all_commands = {}
        for cmd in entries:
            if cmd.cog is None:
                continue
            elif cmd.cog.qualified_name == "Jishaku":
                continue
            try:
                all_commands[cmd.cog].append(cmd)
            except KeyError:
                all_commands[cmd.cog] = [cmd]

        max_page = len(all_commands.keys())
        count = 0
        for _commands in all_commands.items():
            count += len(_commands)
        page = 1

        def page_setup(cog: commands.Cog) -> discord.Embed:
            """ページ数に対応したhelp内容をセット"""
            embed = discord.Embed(title=f"Page {page}/{max_page} ({count} commands)",
                                  description=f"より詳細なヘルプは[公式サーバ]({bot.guild_invite_url})まで!")
            embed.add_field(name=f"{cog.qualified_name} commands", value=cog.description)
            for cmd in all_commands[cog]:
                embed.add_field(name=f"{cmd.name} {self.get_aliase(cmd)}", value=cmd.short_doc, inline=False)
            return embed

        react_list = [
            u"\u25C0",  # 戻る
            u"\u25B6",  # 進む
            "\U0001f522",  # 1234
            "\U00002139\U0000fe0f",  # インフォメーションマーク
            "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}"  # stop
        ]

        msg = await self.context.send(embed=page_setup(list(all_commands.keys())[page - 1]))
        for react in react_list:
            await msg.add_reaction(react)  # リアクション付与

        def check(reaction, user):
            if reaction.message.id != msg.id:
                return False
            if self.context.author.bot or user != self.context.author:
                return False
            if str(reaction.emoji) in react_list:
                return True
            return False

        while not bot.is_closed():
            try:
                react, user = await bot.wait_for("reaction_add", check=check, timeout=300)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
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
                        await msg.edit(embed=page_setup(list(all_commands.keys())[page - 1]))
                    if emoji == "\U0001f522":  # 1234
                        await self.context.send("移動したいページ数を送信してください！", delete_after=30)
                        try:
                            m = await bot.wait_for("message", check=lambda m: m.author == self.context.author, timeout=30)
                            next_page = int(m.content)
                            await m.delete()
                        except asyncio.TimeoutError:
                            await msg.clear_reactions()
                            break
                        except ValueError:
                            await self.context.send("おっと、ページ数が整数じゃないみたいです", delete_after=5)
                            continue
                        else:
                            if not(1 <= next_page <= max_page):
                                await self.context.send(f"おっと、{next_page}ページはありません！", delete_after=5)
                                continue
                            page = next_page
                            await msg.edit(embed=page_setup(list(all_commands.keys())[page - 1]))
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
                        await msg.edit(embed=page_setup(list(all_commands.keys())[page - 1]))
                    if emoji == "\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}":  # ■
                        await msg.delete()
                        break
                except IndexError:
                    await self.context.send("範囲外のリアクションが押されました", delete_after=3.0)
                    continue

    async def send_cog_help(self, cog):
        pass

    async def send_command_help(self, command):
        pass

    async def send_group_help(self, group):
        pass


def setup(bot):
    pass
