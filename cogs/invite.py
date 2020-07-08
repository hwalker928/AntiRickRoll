import discord
from discord.ext import commands


class invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Click here to invite me!", url="https://discord.com/api/oauth2/authorize?client_id=724918979134488577&permissions=8&scope=bot")
        embed.set_footer(text="AntiRickRoll was made by harrydev#9999",
                        icon_url="https://cdn.discordapp.com/avatars/428450288668508160/a_abb0a57834bed5a46050f23f9ba4c1c6.gif?size=1024")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(invite(bot))
