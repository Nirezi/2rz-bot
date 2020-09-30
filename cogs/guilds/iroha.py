import asyncio
import os
from datetime import datetime

import paramiko
from discord.ext import commands, tasks

SSH = paramiko.SSHClient()


class Iroha(commands.Cog, name="iroha"):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.reboot.start()
        if not self.bot.local:
            host = os.environ["Host"]
            port = os.environ["Port"]
            user = os.environ["User"]
            Key = f"/home/{user}/.ssh/id_rsa"
            SSH.load_host_keys(f"/home/{user}/.ssh/known_hosts")
            SSH.connect(host, int(port), user, key_filename=Key)

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        elif ctx.guild.id != 604945424922574848:
            return False
        elif ctx.author.guild_permissions.administrator or ctx.author.id == 544774774405201923:
            return True
        else:
            return False

    @commands.command(aliases=["boot"], hidden=True)
    async def start(self, ctx):
        stdin, stdout, stderr = await self.loop.run_in_executor(None, SSH.exec_command, "screen -ls | grep minecraft")
        if stdin:
            return await ctx.send("Server is already running!")
        await ctx.send("Starting minecraft server,,")
        await self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash start.sh")

    @commands.command(aliases=["kill"], hidden=True)
    async def stop(self, ctx):
        stdin, stdout, stderr = await self.loop.run_in_executor(None, SSH.exec_command, "screen -ls | grep minecraft")
        if not stdin:
            return await ctx.send("Server isn't running yet!")
        await ctx.send("Stopping minecraft server,,")
        await self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash stop.sh")

    @commands.command(aliases=["reboot"], hidden=True)
    async def restart(self, ctx):
        stdin, stdout, stderr = await self.loop.run_in_executor(None, SSH.exec_command, "screen -ls | grep minecraft")
        if not stdin:
            return await ctx.send("Server isn't running yet!")
        ch = self.bot.get_channel(739270726036488272)
        await ch.send(":warning:Warning!10秒後にサーバーが再起動するよ！")
        await asyncio.sleep(10)
        await self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash restart.sh")

    @commands.command(name="eval", hidden=True)
    async def _eval(self, ctx, *, command):
        await self.loop.run_in_executor(None, SSH.exec_command, f"screen -r -X eval 'stuff \"{command}\"\\015'")
        await ctx.send(f"Command {command} has done by {ctx.author.name}")

    @tasks.loop(minutes=1)
    async def reboot(self):
        hm = datetime.now().strftime("%H:%M")
        if hm == "22:00" or hm == "06:00":
            ch = self.bot.get_channel(739270726036488272)
            await ch.send(":warning:Warning!10秒後にサーバーが再起動するよ！")
            await asyncio.sleep(10)
            await self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash restart.sh")


def setup(bot):
    bot.add_cog(Iroha(bot))
