from discord.ext import commands
import discord
import datetime

class events(commands.Cog):
    def __init__(self, client, config):
        self.client = client
        self.config = config

    @commands.Cog.listener()
    async def on_ready(self):
      print(self.client.user.name, f"is online")
      print("id", self.client.user.id)
      await self.client.change_presence(activity=discord.Game(name=(self.config["status"])))


    @commands.Cog.listener()
    async def on_message(self, message):

      if isinstance(message.channel, discord.DMChannel):
        if message.author.id == self.client.user.id:
          return

        guild = self.client.get_guild(self.config["Guild"])
        user = message.author

        supportCategory = discord.utils.get(guild.categories, name = self.config["OpenCategory"])
        channel = discord.utils.get(supportCategory.channels, topic = str(message.author.id))

        if not channel:
          closedCategory = discord.utils.get(guild.categories, name = self.config["ClosedCategory"])
          channel = discord.utils.get(closedCategory.channels, topic = str(message.author.id))
          if channel:
            await channel.edit(category=supportCategory, name = f"{message.author.name}#{message.author.discriminator}", sync_permissions=True)
          else:
            channel = await supportCategory.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))

          em = discord.Embed(title=f'Thread Opened', description='Staff will respond soon', color=discord.Color.blue(),timestamp=datetime.datetime.utcnow())
          em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
          await user.send(embed=em)

          em = discord.Embed(title=f'New Thread Created', color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
          em.add_field(name='User Name', value=f'{user.name}#{user.discriminator}', inline=False)
          em.add_field(name='User ID', value=user.id, inline=False)
          em.add_field(name='Account Age', value=user.created_at)
          em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
          
          pings = None

          for i in self.config["Ping"]:
            if i is not None:
              role = self.client.get_guild(self.config["Guild"]).get_role(i)
              ping = f"{role.mention}"

          if ping is None:
            await channel.send(embed=em)
          else:
            await channel.send(ping, embed=em)

        if message.attachments:
          for f in message.attachments:
            await channel.send(f)
        
        em = discord.Embed(description=message.content, color=discord.Color.green(),timestamp=datetime.datetime.utcnow())
        em.set_author(name=f'{user.name}#{user.discriminator}', icon_url=message.author.avatar_url)
        em.set_footer(text=self.config["footer"], icon_url=self.client.get_guild(self.config["Guild"]).icon_url)
        await channel.send(embed=em)