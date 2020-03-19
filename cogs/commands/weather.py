import json
import sys
import urllib

from discord.ext import commands

from citycodes_dic import citycodes_dic

sys.path.append("../")


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather")
    async def _weather(self, ctx, titen):
        if titen in citycodes_dic.keys():
            citycode = citycodes_dic[titen]
            resp = urllib.request.urlopen(
                'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' %
                citycode).read()
            resp = json.loads(resp.decode('utf-8'))
            msg = resp['location']['city']
            msg += "の天気は、\n"
            for f in resp['forecasts']:
                msg += f['dateLabel'] + "が" + f['telop'] + "\n"
            msg += "です。"
            await ctx.send(msg)
        else:
            await ctx.send("そこの天気はわかりません")


def setup(bot):
    bot.add_cog(weather(bot))
