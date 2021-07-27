import discord
from discord.ext import commands
import random
import datetime
import time
import os
import asyncio
import config

client = commands.Bot(command_prefix = '.', help_command=None)

animals = [
    'https://media.discordapp.net/attachments/869440719100706826/869447078995165204/lionel-animals-to-follow-on-instagram-1568319926.png',
    'https://media.discordapp.net/attachments/869440719100706826/869447348525346877/GettyImages-1145794687.png?width=1014&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869447427839635507/iStock-619961796-edit-59cabaf6845b3400111119b7.png',
    'https://media.discordapp.net/attachments/869440719100706826/869447669108580402/3000.png?width=1014&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869447808472739932/fashion-2015-10-cute-baby-turtles-main.png?width=1202&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869447923212091412/73f0857e-2a1a-4fea-b97a-bd4c241c01f5.png?width=947&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869448016900264006/p02k8mcv.png',
    'https://media.discordapp.net/attachments/869440719100706826/869448164632039445/f0623acd-fafa-4177-8035-f32d213a30e2-AFP_1153955091.png?width=1014&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869448300720451624/shutterstock_231680788.png',
    'https://media.discordapp.net/attachments/869440719100706826/869448373353209896/6650977359_69e091447f_b.png?width=1011&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869448474024874054/tumblr_phkozt6AB61vf93px_1280.png?width=687&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869448586277048330/DWhRUYKkLuoF57vaJLHVDJ.png',
    'https://media.discordapp.net/attachments/869440719100706826/869448778422288394/maxresdefault.png?width=1202&height=676',
    'https://media.discordapp.net/attachments/869440719100706826/869449049806372994/60489b65260000db03d84d79.png'
]

@client.event
async def on_ready():
    print("Chat reviver is now Online")

channel_pairs = {}
@client.command()
async def channel(ctx, priest_channel: discord.TextChannel, penitent_channel: discord.TextChannel):
    global channel_pairs
    await ctx.send("EX: .channel [where bot sends] [where user sends]")
    channel_pairs[ctx.guild.id] = [penitent_channel.id, priest_channel.id] # Penitent = Sending Channel | Priest = Receiving Channel

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

@client.command()
async def cute(ctx):
    await ctx.send(random.choice(animals))

@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Color.random()
        )
    
    embed.add_field(name="Help Command", value="**.channel [where bot sends] [where user sends]**\n```^ This is the command to setup confessions```\n\n**.cute**\n```sends cute animal picture```")
    
    await ctx.send(embed=embed)


client.run(config.token)