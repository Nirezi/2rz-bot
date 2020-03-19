from discord.ext import commands
import asyncio
import discord


class white(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mcs = message.channel.send

        if isinstance(message.channel, discord.DMChannel):
            return

        if message.guild.id == 551006363698855946:
            if message.content.startswith("/etimer"):
                if message.author.id == 447376081247404043:  # Whiteさん
                    msg = message.content.split()
                    try:
                        n = float(msg[1])
                    except ValueError:
                        await mcs("時間の指定は数値でね!!ほわいとさん!")
                    else:
                        await mcs(f"{msg[1]}時間後にイベントの通知をします\nイベント名:{msg[2]}")
                        await asyncio.sleep(n * 3600)
                        await mcs(f"イベントの通知です!!@everyone\nイベント名:{msg[2]}")
                else:
                    await mcs("えーと、誰？")


def setup(bot):
    bot.add_cog(white(bot))
