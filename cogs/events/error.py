from discord.ext import commands
import traceback
from datetime import datetime
import discord


class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            pass
        elif isinstance(error, commands.BadArgument):
            pass
        else:
            now = datetime.now()
            time = now.strftime("%Y/%m/%d %H:%M:%S")
            client = self.bot
            orig_error = getattr(error, "original", error)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            channel = client.get_channel(639121643901288500)
            embed = discord.Embed(title='Error_log', description=error_msg, color=0xf04747)
            embed.set_footer(text=f'channel:{ctx.channel}\ntime:{time}')
            await channel.send("<@544774774405201923>エラーが発生しました", embed=embed)


def setup(bot):
    bot.add_cog(error(bot))
