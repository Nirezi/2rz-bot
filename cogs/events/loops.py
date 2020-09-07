import asyncio
import sys
from datetime import datetime
import re

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
        if hm == "23:50":
            ch = self.bot.get_channel(706322916060692571)
            record_list = None
            async for msg in ch.history():
                if msg.author == self.bot.user:
                    last_record = await ch.fetch_message(msg.id)
                    record_list = last_record.content.splitlines()
                    break

            if record_list is None:
                await ch.send("Error: couldn't get message")

            mcid_uuid_dic = {
                "shibatanienn_ts": "f63f13d9-ea1d-43f9-a0c7-46bb9445625d",
                "takosan_ykz": "4303b357-30ca-4209-a6c9-d96bafc60cf0",
                "chorocra": "438ed7bf-cbcf-40d9-a672-aacc2868e267",
                "ranzumu": "45578816-9dab-49fc-bef0-0525e0a57289",
                "kakkoiihito": "24eeb1a3-ed4a-444e-828c-5318122f4e4a",
                "nekorobi_0": "d6be1561-47c1-4e67-9829-2aca48f9be39",
                "kaerusan82433413": "9cec894e-9ae3-4a25-97c5-b7a6c55c1376"
            }

            msg = ""
            for i, mcid in enumerate(mcid_uuid_dic.keys()):
                uuid = mcid_uuid_dic[mcid]
                last_user_record = 0
                for row in record_list:
                    if row.startswith(mcid):
                        last_user_record = int(re.sub(r'\(前日比:\d+\)', '', record_list[i].split('>>>')[1]))

                data = self.bot.get_mined_block(uuid)

                data_diff = data - last_user_record
                msg += f"{mcid}の整地量>>>{data}(前日比:{data_diff})\n"
                if data_diff == 0:
                    msg += f"おいごらぁ!{mcid}!!あく整地!!!\n"
                await asyncio.sleep(2)
            await ch.send(msg)

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
