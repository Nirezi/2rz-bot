from discord.ext import commands
import asyncio
import re


class AddEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(self, ctx, name):
        if not len(name) >= 2 and len(name) <= 32:
            await ctx.send("絵文字の名前が短すぎるか長過ぎます\n2文字以上32文字以内で指定してください")
            return

        p = re.compile(r'([a-z0-9_]+')
        if not p.fullmatch(name):
            await ctx.send("絵文字の名前として使用できない文字が使われています\n絵文字には英数字とアンダーバーのみが使えます")

        async def setup_emoji(self, ctx, img, emoji_name):
            """カスタム絵文字を追加する関数"""
            if len(await img.read()) >= 25600:
                await ctx.send("サイズが絵文字に使用可能なサイズを超えています。どこかで圧縮してきてください()")
            else:
                emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=await img.read())
            await asyncio.sleep(2)
            await ctx.send(f"絵文字を追加しました\n:{emoji.name}: as {emoji_name}")

        await ctx.send("絵文字を追加します")
        if ctx.message.attachments:
            img = ctx.message.attachments[0]
            await setup_emoji(self, ctx, img, name)
        else:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.message.channel
            await ctx.send(f"{name}で登録する絵文字の画像を送信してください")
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=600)
            except asyncio.TimeoutError:
                await ctx.send("タイムアウトしました")
            else:
                if msg.attachments:
                    img = msg.attachments[0]
                    await setup_emoji(self, ctx, img, name)
                else:
                    await ctx.send("画像を認識できませんでした\nはじめからやり直してください")


def setup(bot):
    bot.add_cog(AddEmoji(bot))
