import os
import traceback

import discord
from discord.ext import commands
import asyncio

# loop = asyncio.new_event_loop()

try:
    import tokens
    token1 = tokens.token1
    local = True
except ModuleNotFoundError:
    token1 = os.environ["token1"]
    local = False


class mybot(commands.Bot):
    def __init__(self, command_prefix):
        self.command_prefix = command_prefix
        self.local = local
        super().__init__(command_prefix)

        self.remove_command("help")
        for cog in os.listdir("./cogs/events"):
            if cog.endswith('.py'):
                try:
                    self.load_extension(f'cogs.events.{cog[:-3]}')
                except Exception:
                    traceback.print_exc()

        for cog in os.listdir("./cogs/guilds"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.guilds.{cog[:-3]}")
                except Exception:
                    traceback.print_exc()

        for cog in os.listdir("./cogs/commands"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.commands.{cog[:-3]}")
                except Exception:
                    traceback.print_exc()

    async def on_ready(self):  # botが起動したら
        print(bot.user.name)
        print(bot.user.id)
        print(discord.__version__)
        print("--------")
        await asyncio.sleep(5)
        channel_list = [627686645969322004, 635345750640951335, 635088307834847263, 635837721952387073]
        # --max-complexity=20
        for channel in channel_list:
            client = self
            channel = client.get_channel(channel)
            if local:
                await channel.send(f"{bot.user}がテスト起動しました")
            else:
                await channel.send(f"**{bot.user} has started**")

        while not client.is_closed():
            kazu = len(list(client.get_all_members()))
            await client.change_presence(activity=discord.Game(f"{kazu}人を監視中"))
            await asyncio.sleep(10)
            guild_kazu = str(len(client.guilds))
            await client.change_presence(activity=discord.Game(f"{guild_kazu}サーバー"))
            await asyncio.sleep(10)
            await client.change_presence(activity=discord.Game("/help"))
            await asyncio.sleep(10)


if __name__ == "__main__":
    # bot = bot(command_prefix = "/",loop = loop)
    # bot_task = loop.create_task(bot.start(token1))
    # loop.run_until_complete(bot_task)
    # loop.close()
    bot = mybot(command_prefix="/")
    bot.load_extension('jishaku')
    bot.run(token1)
