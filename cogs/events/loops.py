from discord.ext import commands, tasks
import discord
from datetime import datetime


class loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop2.start()
        self.loop3.start()
        self.loop4.start()

    @tasks.loop(seconds=60)
    async def loop2(self):
        client = self.bot
        await client.wait_until_ready()
        hm = datetime.now().strftime("%H:%M")
        if hm == "00:00":
            channel = client.get_channel(627867724541853716)
            await channel.send("日付変更をお知らせします")

    @tasks.loop(seconds=60)
    async def loop3(self):
        hm = datetime.now().strftime("%H:%M")
        client = self.bot
        await client.wait_until_ready()
        if hm == "19:00":
            guild = client.get_guild(610309046851076121)
            role = discord.utils.get(guild.roles, id=665853511740948500)  # 新規
            channel = client.get_channel(665854731180310528)
            kazu = len(role.members)
            if kazu == 0:
                await channel.send("おっと、始めにを読んでない人はいないみたいです")
            else:
                await channel.send(f"{role.mention}\n{kazu}人の人がまだ<#630402461395451913>を読んでないみたいですね")


def setup(bot):
    bot.add_cog(loops(bot))
