from dotenv import load_dotenv
import os
import token
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print("The bot is now ready for use")
    print("-----------------------------")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am a development bot")


@client.command()
async def goodbye(ctx):
    await ctx.send("so sad to see you go😭😭")

TOKEN = os.getenv('BOT_AUTH')
client.run(TOKEN)
