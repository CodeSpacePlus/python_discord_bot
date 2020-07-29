import os
import discord
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
  print(f'{bot.user.name} is ready')


@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(f'Hello {member.name}, welcome to the server!')


@bot.event
async def on_command_error(ctx, error):
  print(error)
  if isinstance(error, commands.CheckFailure):
    await ctx.send('You do not have the correct role to use this command.')


@bot.event
async def on_error(event, *args, **kwargs):
  print('An error occurred')
  print(event, args[0])


@bot.command(name='test', help='Dev testing')
@commands.is_owner()
async def test(ctx):
  # https://cog-creators.github.io/discord-embed-sandbox/ for future embeding use

  embedMes = discord.Embed(title="Title", description="Desc", color=0x00ff00)
  embedMes.add_field(name="field1", value="hi", inline=False)
  embedMes.add_field(name="field2", value="hello", inline=False)

  await ctx.send(embed=embedMes)


@bot.command(name='logout')
async def logout_bot(ctx):
  print('Loggin out...')
  await bot.logout()


@bot.command(name='create-category', help="Create a channel category.")
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
async def create_channel(ctx, channel_name, category='', is_voice=False):
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
      if not is_voice:
        await guild.create_text_channel(channel_name, category=existing_category)
      else:
        await guild.create_voice_channel(channel_name, category=existing_category)
      return

  print(f'Creating new channel {channel_name}...')
  if not is_voice:
    await guild.create_text_channel(channel_name)
  else:
    await guild.create_voice_channel(channel_name)


@bot.command(name='create-role', help='Create a server role.')
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


# IMPORTANT NOTE: I have no clue if these are the correct times.
@bot.command(name='ping', help='Get your ping latency')
async def get_ping(ctx):
  message_date = ctx.message.created_at
  current_date = datetime.utcnow()
  api_time = abs(current_date - message_date)
  api_time = int(api_time.total_seconds() * 1000)

  embedMes = discord.Embed(title="🏓 Pong!", color=0xff0000)
  embedMes.add_field(name="Latency", value=f'{api_time}ms', inline=False)
  embedMes.add_field(name="API", value=f'{int(bot.latency * 1000)}ms', inline=False)

  await ctx.send(embed=embedMes)


@bot.command(name='purge', help='Delete n number of messages.')
@commands.has_role('admin')
async def purge(ctx, number):
  channel = ctx.channel  # Commad location
  msg = []  # Empty array where list of message will be stored
  number = int(number) + 1  # Converting number to int and adding command message
  async for x in channel.history(limit=number):
    msg.append(x)
  print(f'Deleting {len(msg) - 1} messages...')
  await channel.delete_messages(msg)


@bot.command(name='kick', help='Kick a member.')
@commands.has_role('admin')
async def kick_member(ctx, userName: discord.User, kickReason='Cuz I felt like it.'):
  guild = ctx.guild
  print(f'Kicking {userName}...')
  await guild.kick(user=userName, reason=kickReason)
  await ctx.send(f'User: {userName} has been kicked. \nReason: {kickReason}')


@bot.command(name='ban', help='Ban a member.')
@commands.has_role('admin')
async def ban_member(ctx, userName: discord.User, kickReason='Cuz I felt like it.'):
  guild = ctx.guild
  print(f'Kicking {userName}...')
  await guild.ban(user=userName, reason=kickReason)
  await ctx.send(f'User: {userName} has been banned. \nReason: {kickReason}')


@bot.command(name='roll_dice', help='Simulates rolling dice (rolls a 6 sided dice by defualt).')
async def roll_dice(ctx, number_of_dice=1, number_of_sides=6):
  dice = [
    str(random.choice(range(1, number_of_sides + 1)))
    for _ in range(number_of_dice)
  ]
  await ctx.send(f"🎲 {', '.join(dice)}")


# @bot.event
# async def on_message(message):
#   if message.content == 'ping':
#     await message.channel.send('pong 🏓')

bot.run(TOKEN)
