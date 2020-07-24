import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
  print(f'{bot.user.name} is ready')


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name, category):
  guild = ctx.guild
  category = category.replace('-',' ').title()
  existing_category = discord.utils.get(guild.categories, name=category.replace('-',' '))
  existing_channel = discord.utils.get(guild.channels, name=channel_name)

  # TODO: Replace with function
  if not existing_category:
    print(f'Creating new category {category}...')
    await guild.create_category(category)
    existing_category = discord.utils.get(guild.categories, name=category)

  if existing_channel:
    response = f'Channel `{channel_name}` already exists...'
    await ctx.send(response)
    return
  
  print(f'Creating new channel {channel_name}...')
  await guild.create_text_channel(channel_name, category=existing_category)


@bot.command(name='roll_dice', help='Simulates rolling dice (rolls a 6 sided dice by defualt).')
async def roll(ctx, number_of_dice=1, number_of_sides=6):
  dice = [
    str(random.choice(range(1, number_of_sides + 1)))
    for _ in range(number_of_dice)
  ]
  await ctx.send(f"🎲 {', '.join(dice)}")


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
  brookly_99_quotes = [
    'I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    (
      'Cool. Cool cool cool cool cool cool cool, '
      'no doubt no doubt no doubt no doubt.'
    ),
  ]

  response = random.choice(brookly_99_quotes)
  await ctx.send(response)


bot.run(TOKEN)


# class CustomClient(discord.Client):
#   async def on_ready(self):
#     print(f'{self.user} is ready.')

#   async def on_error(self, event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#       if event == 'on_message':
#         f.write(f'Unhandled message: {args[0]}\n')
#       else:
#         raise

#   async def on_member_join(self, member):
#     await member.create_dm()
#     print(f'{member.user} has joined the server')
#     await member.dm_channel.send(f'Hello {member.name}, welcome to the server!')

#   async def on_message(self, message):
#     if message.author == self.user:
#       return

#     if message.content == '!stop':
#       print("Loggin out...")
#       await self.logout()
#       return
    
#     brookly_99_quotes = [
#       'I\'m the human form of the 💯 emoji.',
#       'Bingpot!',
#       (
#           'Cool. Cool cool cool cool cool cool cool, '
#           'no doubt no doubt no doubt no doubt.'
#       ),
#     ]

#     if message.content == '99!':
#       response = random.choice(brookly_99_quotes)
#       print(f'{message.author} triggered a command.')
#       await message.channel.send(response)
#     elif message.content == 'raise-exception':
#       raise discord.DiscordException


# client = CustomClient()
# client.run(TOKEN)
