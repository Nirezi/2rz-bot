import asyncio
import re

import discord
from discord.ext import commands


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id == 662503350633365515:
            ch_dic = {
                669850293407842305: 669850327599546389,
                669850376341815347: 669850400039370762
            }
            if before.channel is None:
                if after.channel.id not in ch_dic.keys():
                    return
                ch = self.bot.get_channel(ch_dic[after.channel.id])
                await ch.send(f"{member}が{after.channel}に参加しました")
            if after.channel is None:
                if before.channel.id not in ch_dic.keys():
                    return
                ch = self.bot.get_channel(ch_dic[before.channel.id])
                await ch.send(f"{member}が{before.channel}にから離脱しました")

    @commands.has_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    async def voice(self, ctx):
        await ctx.send(f"{ctx.prefix}voice [set_log, rem_log]")

    @commands.has_permissions(manage_guild=True)
    @voice.command()
    async def set_log(self, ctx, ch_id: int = None):
        if ctx.author.voice.channel is None or ch_id is None:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            await ctx.send("監視するボイスチャンネルのidまたは名前を送信してください")

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=300)
            except asyncio.TimeoutError:
                return await ctx.send("タイムアウトしました。最初からやり直してください")

            p = re.compile(r"[0-9]+")
            if p.fullmatch(msg.content):
                ch = self.bot.get_channel(int(msg.content))
            else:
                ch = discord.utils.get(ctx.guild.voice_channels, name=msg.content)

            if ch is None:
                return await ctx.send("チャンネルを見つけられませんでした、名前、idが間違っていないか確かめてください")

            if not isinstance(ch, discord.VoiceChannel):
                return await ctx.send("指定されたチャンネルはボイスチャンネルではありません。名前、idが間違っていないか確かめてください")

            await self.bot.voice_log.put(ch.id, ctx.channel.id)
            await ctx.send(f"{ctx.channel}を{ch}のログチャンネルとして設定しました")
        elif ctx.author.voice.channel:
            await self.bot.voice_log.put(ctx.author.voice.channel.id, ctx.channel.id)
            await ctx.send(f"{ctx.channel}を{ctx.author.voice.channel}のログチャンネルとして設定しました")
        elif ch_id:
            ch = self.bot.get_channel(ch_id)
            if ch is None:
                return await ctx.send("チャンネルを見つけられませんでした、名前、idが間違っていないか確かめてください")

            if not isinstance(ch, discord.VoiceChannel):
                return await ctx.send("指定されたチャンネルはボイスチャンネルではありません。名前、idが間違っていないか確かめてください")


def setup(bot):
    bot.add_cog(Voice(bot))
