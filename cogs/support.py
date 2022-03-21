from discord.ext import commands
import discord
import datetime


class support(commands.Cog):
    def __init__(self, client, config):
      self.client = client
      self.config = config      

    @commands.command(aliases=['c'])
    async def close(self, ctx):
      if not ctx.guild.id == self.config["guild"]:
        return
      await ctx.message.delete()
      
      category = self.client.get_channel(self.config["category"])
      if ctx.channel in category.channels:
        await ctx.channel.delete()
        user = self.client.get_user(int(ctx.channel.topic))
        em = discord.Embed(title=f'Thread Closed', description='If you reply to this message you will open a new thread', color=discord.Color.red(),timestamp=datetime.datetime.utcnow())
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["guild"]).icon_url)
        await user.send(embed=em)
