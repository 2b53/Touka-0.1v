# userinfo.py
import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo')
    async def user_info(self, ctx, member: discord.Member = None):
        # Deine userinfo-Logik hier
        pass

def setup(bot):
    bot.add_cog(UserInfo(bot))
