from discord.ext import commands
import discord
import datetime
import json

class events(commands.Cog):
    def __init__(self, client, config):
        self.client = client
        self.config = config

    @commands.Cog.listener()
    async def on_ready(self):
      print(self.client.user.name, f"is online")
      print(f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=140123827281&scope=bot")
      await self.client.change_presence(activity=discord.Game(name=(self.config["status"])))
      
      if not self.client.get_guild(self.config['guild']):
        for guild in self.client.guilds:
          with open('config.json', 'r+') as f:
            data = json.load(f)
            data['guild'] = guild.id
            f.seek(0)
            json.dump(data, f, indent=4)


    @commands.Cog.listener()
    async def on_message(self, message):
      if message.content.startswith(self.config['prefix']):
        return
      
      if isinstance(message.channel, discord.TextChannel):
        if message.author.id == self.client.user.id:
          return
        
        guild = self.client.get_guild(self.config["guild"])
        if not message.guild is guild:
          return
        
        if not self.client.get_channel(self.config["category"]):
          category = await guild.create_category("support")
          with open('config.json', 'r+') as f:
            data = json.load(f)
            data['category'] = category.id
            f.seek(0)
            json.dump(data, f, indent=4)
        else:
          category = self.client.get_channel(self.config["category"])
        channel = discord.utils.get(category.channels, name=message.channel.name)
        
        if not channel is None:
          user = self.client.get_user(int(channel.topic))
          em = discord.Embed(description=message.content, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
          em.set_author(name=f'{message.author.name}#{message.author.discriminator}', icon_url=message.author.avatar_url)
          em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["guild"]).icon_url)
          await user.send(embed=em)

          await message.delete()
          em = discord.Embed(description=message.content, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
          em.set_author(name=f'{message.author.name}#{message.author.discriminator}', icon_url=message.author.avatar_url)
          em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["guild"]).icon_url)
          await message.channel.send(embed=em)
          
          if message.attachments:
            for f in message.attachments:
              await user.send(f)
              await channel.send(f)

      if isinstance(message.channel, discord.DMChannel):
        if message.author.id == self.client.user.id:
          return

        guild = self.client.get_guild(self.config["guild"])
        user = message.author
        
        if not self.client.get_channel(self.config["category"]):
          category = await guild.create_category("support")
          with open('config.json', 'r+') as f:
            data = json.load(f)
            data['category'] = category.id
            f.seek(0)
            json.dump(data, f, indent=4)
        else:
          category = self.client.get_channel(self.config["category"])
        channel = discord.utils.get(category.channels, topic = str(message.author.id))

        if not channel: 
          channel = await category.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))

          em = discord.Embed(title=f'Thread Opened', description='Staff will respond soon', color=discord.Color.blue(),timestamp=datetime.datetime.utcnow())
          em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["guild"]).icon_url)
          await user.send(embed=em)

          em = discord.Embed(title=f'New Thread Created', color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
          em.add_field(name='User Name', value=f'{user.name}#{user.discriminator}', inline=False)
          em.add_field(name='User ID', value=user.id, inline=False)
          em.add_field(name='Account Age', value=user.created_at)
          em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["guild"]).icon_url)
          
          pings = None

          for id in self.config["ping"]:
            if id is not None:
              pings =+ f"<@&{id}> "

          if pings is None:
            await channel.send(embed=em)
          else:
            await channel.send(pings, embed=em)

        if message.attachments:
          for f in message.attachments:
            await channel.send(f)
            
        await message.add_reaction("✅")
        
        em = discord.Embed(description=message.content, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'{user.name}#{user.discriminator}', icon_url=message.author.avatar_url)
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["guild"]).icon_url)
        await channel.send(embed=em)