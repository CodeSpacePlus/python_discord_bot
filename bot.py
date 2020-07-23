import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class CustomClient(discord.Client):
  async def on_ready(self):
    print(f'{self.user} is ready.')

  async def on_member_join(self, member):
    await member.create_dm()
    print(f'{member.user} has joined the server')
    await member.dm_channel.send(f'Hello {member.name}, welcome to the server!')

  async def on_message(self, message):
    if message.author == self.user:
      return
    
    brookly_99_quotes = [
      'I\'m the human form of the 💯 emoji.',
      'Bingpot!',
      (
          'Cool. Cool cool cool cool cool cool cool, '
          'no doubt no doubt no doubt no doubt.'
      ),
    ]

    if message.content == '99!':
      response = random.choice(brookly_99_quotes)
      print(f'{message.author} triggered a command.')
      await message.channel.send(response)


client = CustomClient()
client.run(TOKEN)
