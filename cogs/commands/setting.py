from discord.ext import commands


class Setting(commands.Cog):
    """botの設定に関するコマンド
    サーバーにおいて何かしらの権限が必要
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    async def quote(self, ctx):
        """メッセージリンクを張った際に引用するかどうかを設定するコマンド"""
        value = '無効'if self.bot.settings.get('not_quote', False, ctx.guild.id) else '有効'
        await ctx.send(f'現在メッセージ展開は{value}に設定されています。`{ctx.prefix}quote on/off`で切り替えができます')

    @commands.has_permissions(manage_guild=True)
    @quote.command()
    async def off(self, ctx):
        if str(ctx.guild.id) in self.bot.settings.keys('not_quote'):
            return await ctx.send('メッセージ展開は既に**無効**になっています')
        await self.bot.settings.put('not_quote', True, ctx.guild.id)
        await ctx.send('メッセージ展開を**無効**にしました')

    @commands.has_permissions(manage_guild=True)
    @quote.command()
    async def on(self, ctx):
        if str(ctx.guild.id) not in self.bot.settings.keys('not_quote'):
            return await ctx.send('メッセージ展開は既に**有効**になっています')
        await self.bot.settings.remove('not_quote', ctx.guild.id)
        await ctx.send('メッセージ展開を**有効**にしました')


def setup(bot):
    bot.add_cog(Setting(bot))
