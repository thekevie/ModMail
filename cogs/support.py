from discord.ext import commands
import discord
import datetime


class support(commands.Cog):
    def __init__(self, client, config):
      self.client = client
      self.config = config

    @commands.command(aliases=['o'])
    async def open(self, ctx):
      if not ctx.guild.id == self.config["Guild"]:
        return

      category = discord.utils.get(ctx.guild.categories, name = self.config["ClosedCategory"])
      channel = discord.utils.get(category.channels, name=ctx.channel.name)
      if not channel is None:
        user = self.client.get_user(int(channel.topic))
        em = discord.Embed(title=f'Thread Opened', color=discord.Color.blue(),timestamp=datetime.datetime.utcnow())
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
        await user.send(embed=em)

        await ctx.message.delete()
        em = discord.Embed(title=f'Thread Opened', color=discord.Color.blue(),timestamp=datetime.datetime.utcnow())
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)

        category = discord.utils.get(ctx.guild.categories, name=self.config["OpenCategory"]) 
        await ctx.channel.edit(category=category, sync_permissions=True)

        await ctx.send(embed=em)        

    @commands.command(aliases=['c'])
    async def close(self, ctx):
      if not ctx.guild.id == self.config["Guild"]:
        return
      
      user = self.client.get_user(int(ctx.channel.topic))
      em = discord.Embed(title=f'Thread Closed', description='If you reply to this message you will open a new thread', color=discord.Color.red(),timestamp=datetime.datetime.utcnow())
      em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
      await user.send(embed=em)

      await ctx.message.delete()
      em = discord.Embed(color=discord.Color.red(),timestamp=datetime.datetime.utcnow())
      em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
      em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
      em.add_field(name='Thread Closed', value=f'Use `{self.config["prefix"]}open` to reopen the thread')

      category = discord.utils.get(ctx.guild.categories, name=self.config["ClosedCategory"]) 
      await ctx.channel.edit(category=category, sync_permissions=True)

      await ctx.send(embed=em)
        

    @commands.command(aliases=['r'])
    async def reply(self, ctx, *, msg):
      if not ctx.guild.id == self.config["Guild"]:
        return
      
      category = discord.utils.get(ctx.guild.categories, name = self.config["OpenCategory"])
      channel = discord.utils.get(category.channels, name=ctx.channel.name)
      if not channel is None:
        user = self.client.get_user(int(channel.topic))
        em = discord.Embed(description=msg, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
        await user.send(embed=em)

        await ctx.message.delete()
        em = discord.Embed(description=msg, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)

        await ctx.send(embed=em)

    @commands.command(aliases=['ar'])
    async def areply(self, ctx, *, msg):
      if not ctx.guild.id == self.config["Guild"]:
        return
      
      category = discord.utils.get(ctx.guild.categories, name = self.config["OpenCategory"])
      channel = discord.utils.get(category.channels, name=ctx.channel.name)
      if not channel is None:
        user = self.client.get_user(int(channel.topic))
        em = discord.Embed(description=msg, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'Anonymous Reply')
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
        await user.send(embed=em)

        await ctx.message.delete()
        em = discord.Embed(title='Anonymous Reply' ,description=msg, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)

        await ctx.send(embed=em)

    @commands.command(aliases=['er'])
    async def ereply(self, ctx, *, msg):
      if not ctx.guild.id == self.config["Guild"]:
        return
      
      category = discord.utils.get(ctx.guild.categories, name = self.config["OpenCategory"])
      channel = discord.utils.get(category.channels, name=ctx.channel.name)
      if not channel is None:
        user = self.client.get_user(int(channel.topic))
        await user.send(msg)

        await ctx.message.delete()
        em = discord.Embed(description=msg, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'{ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url)
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
        em.set_author(name='No Embed Reply')

        await ctx.send(embed=em)
