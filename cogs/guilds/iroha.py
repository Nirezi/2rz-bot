from discord.ext import commands
import paramiko
import os
import asyncio

SSH = paramiko.SSHClient()

host = os.environ["Host"]
port = os.environ["Port"]
user = os.environ["User"]
Key = f"/home/{user}/.ssh/id_rsa"
SSH.load_host_keys(f"/home/{user}/.ssh/known_hosts")


class Iroha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        SSH.connect(host, int(port), user, key_filename=Key)

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        elif ctx.guild.id != 604945424922574848:
            return False
        elif ctx.author.guild_permissions.administrator:
            return True
        else:
            return False

    @commands.command(aliases=["boot"])
    async def start(self, ctx):
        stdin, stdout, stderr = self.loop.run_in_executor(None, SSH.exec_command, "screen -ls | grep minecraft")
        if stdin:
            return await ctx.send("Server is already running!")
        await ctx.send("Starting minecraft server,,")
        self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash start.sh")

    @commands.command(aliases=["kill"])
    async def stop(self, ctx):
        stdin, stdout, stderr = self.loop.run_in_executor(None, SSH.exec_command, "screen -ls | grep minecraft")
        if not stdin:
            return await ctx.send("Server isn't running yet!")
        await ctx.send("Stopping minecraft server,,")
        self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash stop.sh")

    @commands.command(aliases=["reboot"])
    async def restart(self, ctx):
        stdin, stdout, stderr = self.loop.run_in_executor(None, SSH.exec_command, "screen -ls | grep minecraft")
        if not stdin:
            return await ctx.send("Server isn't running yet!")
        ch = self.bot.get_channel(739270726036488272)
        await ch.send(":warning:Warning!10秒後にサーバーが再起動するよ！")
        await asyncio.sleep(10)
        self.loop.run_in_executor(None, SSH.exec_command, "cd ~/Minecraft && bash restart.sh")

    @commands.command(name="eval")
    async def _eval(self, ctx, *, command):
        self.loop.run_in_executor(SSH.exec_command(f"screen -r -X eval 'stuff \"{command}\"\\015'"))
        await ctx.send(f"Command {command} has done by {ctx.author.name}")


def setup(bot):
    bot.add_cog(Iroha(bot))
