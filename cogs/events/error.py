from discord.ext import commands
import traceback
from datetime import datetime
import discord


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('このコマンドはサーバ専用です')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('このコマンドは製作者により無効化されています')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{error.missing_perms}の権限がありません")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'**botに{error.missing_perms}の権限がありません**\nサーバ管理者まで問い合わせてください')
        elif isinstance(error, commands.CommandInvokeError):
            msg = '引数などが正しいか確認してみてください。\nコマンドが正しいにも関わらずエラーが発生する場合msg_idとともに公式サーバまでお問い合わせください'
            embed = discord.Embed(title='エラーが発生しました', description=msg)
            embed.add_field(name="エラー内容 ＊bot開発者向け", value=str(error))
            embed.add_field(name=f'[公式サーバ]({self.bot.guild_invite_url})', value=f'msg_id: {ctx.message.id}')
            await ctx.send(embed=embed)
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            client = self.bot
            orig_error = getattr(error, "original", error)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            channel = client.get_channel(639121643901288500)
            embed = discord.Embed(title='Error_log', description=error_msg, color=0xf04747)
            embed.set_footer(text=f'channel:{ctx.channel}\ntime:{time}')
            await channel.send(f"<@544774774405201923>エラーが発生しました \nmsg_id: {ctx.message.id}", embed=embed)
            await channel.send(error.__cause__)


def setup(bot):
    bot.add_cog(Error(bot))
