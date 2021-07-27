import discord
from discord.ext import commands
import random
import datetime
import time
import os
import asyncio
import config

client = commands.Bot(command_prefix = '.', help_command=None)

@client.event
async def on_ready():
    print("Confessioner is now Online")

@client.command()
async def test():
    print("Working")

channel_pairs = {}
@client.command()
async def channel(ctx, priest_channel: discord.Channel, penitent_channel: discord.Channel):
    global channel_pairs
    channel_pairs[ctx.guild.id] = [priest_channel.id, penitent_channel.id]

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


client.run(config.token)