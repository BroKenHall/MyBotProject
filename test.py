import discord
from discord.ext import commands
import random
import datetime
import time
import os
import asyncio

client = commands.Bot(command_prefix = '.', help_command=None)

@client.event
async def on_ready():
    print("Confessioner is now Online")

channel_pairs = {}
@client.command()
async def channel(ctx):
    global channel_pairs
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Where do you want confessions sent?")
    msg = await client.wait_for('message', check=check)
    try:
        channel_1 = await commands.TextChannelConverter().convert(ctx, msg.content) # Converting message text to text channel
    except:
        # If it's an invalid channel, or conversion fails
        return await ctx.send("That's not a valid channel!")

    await ctx.send("Where do you want confessions recieved?")
    msg = await client.wait_for('message', check=check)
    try:
        channel_2 = await commands.TextChannelConverter().convert(ctx, msg.content) # Converting message text to text channel
    except:
        # If it's an invalid channel, or conversion fails
        return await ctx.send("That's not a valid channel!")

    channel_pairs[ctx.guild.id] = [channel_1.id, channel_2.id] # first item is sending channel, second item is receiving channel

@client.listen()
async def on_message(message):
    guild = message.guild
    pair = channel_pairs.get(guild.id)
    if not pair:
      return
    
    if message.channel.id == pair[1]: # If channel ID is the receiving channel
        embed = discord.Embed(
            colour=discord.Color.random()
            )

        embed.add_field(name="Confession", value=f"{message.content}")
        embed.set_footer(text="Anonymous Confession")

        send_ch = discord.utils.get(message.guild.channels, id=pair[0])
        await send_ch.send(embed=embed)
        await message.delete()


client.run('ODY3NzIzMzI1NzkxMDEwODE3.YPlQUg.yQUqICvjwM8UBvoM4Lcb_CeCsYo')