import discord
from discord.ext import commands
import asyncio


class CheckPermission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["check_per", "cp"])
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    async def check_permission(self, ctx, member: discord.Member, scope, *selected_perm):
        """
        指定されたユーザーの指定されたチャンネルでの権限を確認するコマンド
        権限を確認できるチャンネルはメッセージの送信者が閲覧できるチャンネルのみ
        必要権限等は特になし
        """
        if len(selected_perm) != 0:
            perm_list = []
            for perm in selected_perm:
                if perm not in dir(discord.Permissions):
                    await ctx.send(f'{perm}は権限として正しくないため除外されます')
                else:
                    perm_list.append(perm)

            if len(perm_list) == 0:
                raise commands.BadArgument
        else:
            perm_list = [
                'manage_channels',  # チャンネル管理
                'add_reactions',  # リアクション付与
                'read_messages',  # メッセージを読む(チャンネルの閲覧と同義)
                'send_messages',  # メッセージの送信
                'send_tts_messages',  # tssメッセージ(送信されたメッセージが読み上げられる)の送信
                'manage_messages',  # メッセージ管理
                'attach_files',  # ファイルの添付
                'read_message_history',  # メッセージ履歴の閲覧
                'mention_everyone',  # everyone, here, 全ロールにメンション
                'use_external_emojis',  # 外部絵文字の使用
            ]
            if member.bot:
                perm_list.append('embed_links')  # 指定されたユーザーがbotならリンクの埋め込みの権限も確認

        async def manage_embed(mem, ch, num=0, before_msg=None):
            """チャンネルとメンバーに応じたembedを送信・編集する関数"""
            permission = ch[num].permissions_for(mem)

            msg = ""
            for perm in perm_list:
                arg = "\U00002705" if getattr(permission, perm) else "\U0000274c"
                msg += f"**{perm}:{arg}**\n"  # 権限がTrueなら:white_check_mark: Falseなら:x:リアクションを追加
            embed = discord.Embed(title=ch[num].name, description=msg)

            if before_msg is None:  # 初回ならメッセージを送信、二回目以降ならメッセージを編集
                m = await ctx.send(embed=embed)
                return m
            await before_msg.edit(embed=embed)
            return

        # 権限を確認するチャンネルの範囲を指定
        if scope == "guild":
            channels = ctx.guild.text_channels
        elif scope == "category":
            channels = ctx.channel.category.text_channels
        elif scope == "here":
            return await manage_embed(member, [ctx.channel])
        else:
            await ctx.send("引数`scope`は`guild`, `category`, `here`のいずれかである必要があります")
            return

        react_list = [
            "\U000023ee\U0000fe0f",  # 左矢印*2
            "\U000025c0\U0000fe0f",  # 左矢印
            "\U000025b6\U0000fe0f",  # 右矢印
            "\U000023ed\U0000fe0f"  # 右矢印*2
        ]

        for channel in channels:
            author_perm = channel.permissions_for(ctx.author)
            if not author_perm.read_messages:
                channels.remove(channel)  # authorが閲覧できないチャンネルは除外
            else:
                continue

        send_msg = await manage_embed(member, channels)
        for react in react_list:
            await send_msg.add_reaction(react)  # リアクション付与

        def check(react, user):
            emoji = str(react.emoji)
            if emoji in react_list and user == ctx.author:
                return emoji, user
            return 0

        num = 0
        while not self.bot.is_closed():
            try:
                emoji, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                await send_msg.clear_reactions()  # タイムアウトしたらリアクションを全削除
                return
            else:
                await send_msg.remove_reaction(emoji, user)  # 付与されたリアクションの削除
                index = react_list.index(str(emoji))
                # 付与されたリアクションに応じてページ移動
                if index == 0:
                    num = 0
                elif index == 1:
                    num -= 1
                elif index == 2:
                    num += 1
                else:
                    num = len(channels) - 1

                if num <= -1 or len(channels) <= num:
                    msg = await ctx.send('範囲外です')  # エラーメッセージ
                    await msg.delete()
                    continue

                await manage_embed(member, channels, num, send_msg)

    @check_permission.error
    async def error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('不正な引数です')


def setup(bot):
    bot.add_cog(CheckPermission(bot))
