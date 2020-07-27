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


@bot.command(name='create-category')
@commands.has_role('admin')
async def create_category(ctx, category_name):
  guild = ctx.guild
  existing_category = discord.utils.get(guild.categories, name=category_name)
  
  if existing_category:
    print(f'Category already exist...')
    return existing_category

  print(f'Creating new category {category_name}...')
  await guild.create_category(category_name)
  existing_category =  discord.utils.get(guild.categories, name=category_name)
  return existing_category


@bot.command(name='create-channel', help='Create a new channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name, category=''):
  guild = ctx.guild
  category = category.replace('-',' ').title()
  existing_channel = discord.utils.get(guild.channels, name=channel_name)
  
  if existing_channel:
    response = f'Channel `{channel_name}` already exists...'
    await ctx.send(response)
    return

  if category != '':
    existing_category = discord.utils.get(guild.categories, name=category)
    if not existing_category:
      print(f'Category {category} does not exist...')
      existing_category = await create_category(ctx, category)
      print(f'Creating new channel {channel_name}...')
      await guild.create_text_channel(channel_name, category=existing_category)
      return

  print(f'Creating new channel {channel_name}...')
  await guild.create_text_channel(channel_name)


@bot.command(name='create-role')
@commands.has_role('admin')
async def create_role(ctx, role_name):
  guild = ctx.guild
  role_name = role_name.replace('-', ' ').title()
  existing_role = discord.utils.get(guild.roles, name=role_name)

  if existing_role:
    ctx.send(f'Role {role_name} already exists')
    return
  
  print(f'Creating new role {role_name}...')
  await guild.create_role(name=role_name, mentionable=True)


@bot.command(name='ping', help='Get your ping latency')
async def get_ping(ctx):
  message = ctx.message
  print(message.created_at)


@bot.command(name='purge', help='Delete n number of messages.')
async def purge(ctx, number):
  channel = ctx.channel  # Commad location
  msg = []  # Empty array where list of message will be stored
  number = int(number) + 1  # Converting number to int and adding command message
  async for x in channel.history(limit=number):
    msg.append(x)
  print('Deleting messages...')
  await channel.delete_messages(msg)


@bot.command(name='roll_dice', help='Simulates rolling dice (rolls a 6 sided dice by defualt).')
async def roll_dice(ctx, number_of_dice=1, number_of_sides=6):
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


# @bot.event
# async def on_message(message):
#   if message.content == 'ping':
#     await message.channel.send('pong 🏓')


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CheckFailure):
    await ctx.send('You do not have the correct role to use this command.')


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
