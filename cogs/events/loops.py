import ast
import asyncio
import random
import sys
from datetime import datetime

import discord
from discord.ext import commands, tasks

sys.path.append("../")


class Loops(commands.Cog, name="loop"):
    def __init__(self, bot):
        self.bot = bot
        self.status_num = 0
        self.check_seichi.start()
        self.change_status.start()

    @tasks.loop(seconds=60)
    async def check_seichi(self):
        await self.bot.wait_until_ready()
        hm = datetime.now().strftime("%H:%M")
        if True:
            log_ch = self.bot.get_channel(706322916060692571)
            last_record = None
            async for msg in log_ch.history():
                if msg.author == self.bot.user and "Log" in msg.content:
                    last_record = ast.literal_eval(msg.content.replace("Log", ""))
                    await msg.delete()
                    break

            if last_record is None:
                return await log_ch.send("Error: couldn't get message")

            mcid_uuid_dic = {
                "shibatanienn_ts": "f63f13d9-ea1d-43f9-a0c7-46bb9445625d",
                "takosan_ykz": "4303b357-30ca-4209-a6c9-d96bafc60cf0",
                "chorocra": "438ed7bf-cbcf-40d9-a672-aacc2868e267",
                "ranzumu": "45578816-9dab-49fc-bef0-0525e0a57289",
                "kakkoiihito": "24eeb1a3-ed4a-444e-828c-5318122f4e4a",
                "Buu_sakurasawa": "47eee383-c807-46aa-ae00-a69b77b3a16c",
                "kaerusan82433413": "9cec894e-9ae3-4a25-97c5-b7a6c55c1376",
                "jojo_kpc": "d43a91ed-675a-4df7-ae50-dc9b0839592a",
                "nyanko_Tofu": "04f6fb30-c432-4395-887f-5a6741839bc8"
            }

            today_data = {mcid: self.bot.get_mined_block(uuid) for mcid, uuid in mcid_uuid_dic.items()}

            for mcid, data in today_data.items():
                icon = f"http://cravatar.eu/helmavatar/{mcid}.png"

                data_diff = data - last_record[mcid]

                embed = discord.Embed(title=f"{mcid}の整地量", description=f"{data}(前日比:{data_diff})")
                embed.set_thumbnail(url=icon)

                await log_ch.send(embed=embed)
                if data_diff == 0:
                    choice = random.choice(["あくしろ働け", "整地しろ！", "あく整地！"])
                    await log_ch.send(f"おいごらぁ！{mcid}!{choice}")
                if mcid == "chorocra" and data_diff < 10000000:
                    await log_ch.send(f"<@325846946864431104>あくしろはたらけ")
                await asyncio.sleep(2)
            await log_ch.send(f"Log{today_data}")

    @tasks.loop(minutes=3)
    async def change_status(self):
        await self.bot.wait_until_ready()
        if self.status_num == 0:
            await self.bot.change_presence(activity=discord.Game(f"{len(list(self.bot.get_all_members()))}人を監視中"))
            self.status_num += 1
        elif self.status_num == 1:
            await self.bot.change_presence(activity=discord.Game(f"{len(self.bot.guilds)}サーバー"))
            self.status_num += 1
        else:
            await self.bot.change_presence(activity=discord.Game("カスタムprefixを実装"))
            self.status_num = 0


def setup(bot):
    bot.add_cog(Loops(bot))
