import discord

from discord.ext import commands
import datetime


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bot_info")
    async def _bot_info(self, ctx):
        async with ctx.channel.typing():

            role_count = len(ctx.guild.me.roles[1:])
            role_name = "、".join(role.name for role in ctx.guild.me.roles[1:])
            bot_role = f"{role_name}\nSum:{role_count}"
            if role_count == 0:
                bot_role = "まだ1つもroleを持っていません"
            elif role_count >= 10:
                bot_role = f"Sum:{role_count}"

            text = 0
            voice = 0
            for g in self.bot.guilds:
                for ch in g.channels:
                    if isinstance(ch, discord.TextChannel):
                        text += 1
                    elif isinstance(ch, discord.VoiceChannel):
                        voice += 1

            created_at_JST = self.bot.user.created_at + datetime.timedelta(hours=9)

            owner = self.bot.get_user(544774774405201923)

            embed = discord.Embed(
                title=f"Hi! I'm{self.bot.user}!",
                description=f"powered by discord.py\n{str(owner)} made me!\n"
                            f"[Support Server]({self.bot.guild_invite_url})",
                url=self.bot.invite_url)
            print(self.bot.owner_id)
            embed.set_thumbnail(url=self.bot.user.avatar_url)  # ユーザーアバターをセット
            embed.add_field(name="Name", value=self.bot.user)
            embed.add_field(name="ID", value=self.bot.user.id)
            embed.add_field(name="Create_at", value=created_at_JST.strftime("%Y %m/%d %H:%M(JST)"))
            embed.add_field(name="Guilds", value=f"{len(self.bot.guilds)}(Shared: {self.bot.get_shared_count(ctx.author)})")
            embed.add_field(name="Roles", value=bot_role)
            embed.add_field(name="Channels", value=f"total:{text + voice}\ntext:{text}\nvoice:{voice}")
            embed.add_field(name="Users", value=str(len(list(self.bot.get_all_members()))))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
