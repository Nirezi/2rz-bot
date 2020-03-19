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

    @tasks.loop(minutes=1)
    async def loop4(self):
        client = self.bot
        await client.wait_until_ready()
        channel = client.get_channel(684751142403440661)
        async for msg in channel.history():
            if msg.author == client.user:
                next_time = msg.content[7:12]
                hm = datetime.now().strftime("%H:%M")
                if next_time == hm:
                    await channel.send("<@&686491092857782307>bumpが可能になりました")
                break


def setup(bot):
    bot.add_cog(loops(bot))
