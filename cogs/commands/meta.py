import asyncio
import datetime

import discord
from discord.ext import commands


class Meta(commands.Cog):
    """
    discordの情報などを表示するコマンド
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bot_info")
    async def _bot_info(self, ctx):
        """
        botに関する情報を表示します
        """
        async with ctx.channel.typing():

            role_count = len(ctx.guild.me.roles[1:])
            role_name = "、".join(role.name for role in ctx.guild.me.roles[1:])
            bot_role = f"{role_name}\nSum:{role_count}"
            if role_count == 0:
                bot_role = "まだ1つもroleを持っていません"
            elif role_count >= 10:
                bot_role = f"Sum:{role_count}"

            text = 0
            voice = 0
            for g in self.bot.guilds:
                for ch in g.channels:
                    if isinstance(ch, discord.TextChannel):
                        text += 1
                    elif isinstance(ch, discord.VoiceChannel):
                        voice += 1
            bot = 0
            user = 0
            for m in self.bot.get_all_members():
                if m.bot:
                    bot += 1
                else:
                    user += 1

            created_at_JST = self.bot.user.created_at + datetime.timedelta(hours=9)
            owner = self.bot.get_user(544774774405201923)

            embed = discord.Embed(
                title=f"Hi! I'm {self.bot.user}!",
                description=f"powered by discord.py\n{str(owner)} made me!\n"
                            f"[Support Server]({self.bot.guild_invite_url})",
                url=self.bot.invite_url)
            embed.set_thumbnail(url=self.bot.user.avatar_url)  # ユーザーアバターをセット
            embed.add_field(name="Name", value=self.bot.user)
            embed.add_field(name="ID", value=self.bot.user.id)
            embed.add_field(name="Create_at", value=created_at_JST.strftime("%Y %m/%d %H:%M(JST)"))
            embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)}(Shared: {self.bot.get_shared_count(ctx.author)})")
            embed.add_field(name="Roles", value=bot_role)
            embed.add_field(name="Channels", value=f"total:{text + voice}\ntext:{text}\nvoice:{voice}")
            embed.add_field(name="Users", value=f"total:{user + bot}\nuser:{user}\nbot:{bot}")

        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def _avatar(self, ctx, id: int = None):
        """
        ユーザー又はサーバーのアイコンを表示します。
        引数としてユーザーもしくはサーバーのidを渡してください。
        """
        if id is None:
            await ctx.send("idを指定してね！")
            return

        user = self.bot.get_user(id)
        guild = self.bot.get_guild(id)

        if user is not None:
            embed = discord.Embed(title=f"{user}", description="")
            embed.set_image(url=user.avatar_url)
            await ctx.send(embed=embed)
        elif guild is not None:
            if len(guild.icon_url) == 0:
                await ctx.send("おっと、このサーバーでは表示できないみたいです。")
            else:
                embed = discord.Embed(title=f"{guild}", description="")
                embed.set_image(url=guild.icon_url)
                await ctx.send(embed=embed)
        else:
            await ctx.send("404 NotFound\nおっと、そのidは表示できないみたいです。")

    @_avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("もしかして:idが数字じゃない")

    @commands.command(aliases=["check_per", "cp"])
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def check_permission(self, ctx, member: discord.Member, scope, *selected_perm):
        """
        指定されたチャンネルでのユーザーの権限を表示します。
        第1引数に表示するユーザーのid, メンション, 名前。
        第2引数に権限を確認する場所(guild, category, hereのいずれか)
        第3引数に確認する権限を指定することも出来ます。(指定しなくても動きます)
        """
        if len(selected_perm) != 0:
            perm_list = []
            for perm in selected_perm:
                if perm not in dir(discord.Permissions):
                    await ctx.send(f'{perm}は権限として正しくないため除外されます')
                else:
                    perm_list.append(perm)

            if len(perm_list) == 0:
                raise commands.BadArgument("正しくない権限が渡されました。")
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
                'embed_links'  # リンク埋め込みの権限
            ]

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
    bot.add_cog(Meta(bot))
