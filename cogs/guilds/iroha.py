from discord.ext import commands
import paramiko
import os

SSH = paramiko.SSHClient()

host = os.environ["Host"]
port = os.environ["Port"]
user = os.environ["User"]
Key = "~/.ssh/id_rsa"
SSH.load_host_keys(f"/home/{user}/.ssh/known_hosts")


class Iroha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        SSH.connect(host, int(port), user, key_filename=Key)

    def cog_check(self, ctx):
        if ctx.guild is None:
            return False
        #elif ctx.guild.id != 604945424922574848:
        #    return False
        elif ctx.author.guild_permissions.administrator:
            return True
        else:
            return False

    @commands.command(aliases=["boot"])
    async def start(self, ctx):
        SSH.exec_command("cd ~/Minecraft && bash start.sh")

    @commands.command()
    async def stop(self, ctx):
        SSH.exec_command("cd ~/Minecraft && bash stop.sh")

    @commands.command(aliases=["reboot"])
    async def restart(self, ctx):
        SSH.exec_command("cd ~/Minecraft && bash restart.sh")


def setup(bot):
    bot.add_cog(Iroha(bot))
