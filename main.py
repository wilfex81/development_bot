from dotenv import load_dotenv
import os
import requests
import json
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


@client.event
async def on_member_join(member):

    JOKEAPI = os.getenv('JOKEAPIKEY')
    dad_jokes = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": JOKEAPI,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(dad_jokes, headers=headers)

    channel = client.get_channel(1194302076952531048)
    await channel.send("Welcome to the server!, How about a nice dad joke!! UUH?")
    await channel.send(json.load(response.text)['content'])


@client.event
async def on_member_remove(member):
    channel = client.get_channel(1194302076952531048)
    await channel.send("Goodbye!")

TOKEN = os.getenv('BOT_AUTH')
client.run(TOKEN)
