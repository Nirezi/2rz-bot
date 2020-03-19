from discord.ext import commands
import datetime
import asyncio


class d_bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == 684751142403440661 and message.content == "!d bump":
            await asyncio.sleep(3)
            async for msg in message.channel.history():
                if msg.embeds:
                    if "表示順をアップしたよ" in msg.embeds[0].description:
                        tugi = msg.created_at + datetime.timedelta(hours=11)
                        tugi_str = tugi.strftime("%H:%M")
                        send_msg = f"次のbumpは{tugi_str}頃にできます"
                        
                        await message.channel.send(send_msg)
                        break


def setup(bot):
    bot.add_cog(d_bump(bot))
