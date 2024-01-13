from profanityfilter import ProfanityFilter
from dotenv import load_dotenv
import os
import requests
import json
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

load_dotenv()

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

queues = {}


def check_queue(ctx, id):
    if id in queues and queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


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


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = discord.FFmpegPCMAudio('music.mp3')
        player = voice.play(source)
    else:
        await ctx.send("You must be in a voice channel to run this command!!😡")


@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left voice channel")
    else:
        await ctx.send("I am not in a voice channel!!😡")


@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("At the moment, there is no audio playing in the channel")


@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("At the moment, no song is paused")


@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("At the moment, no song is playing")


@client.command(pass_context=True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = discord.FFmpegPCMAudio(arg)
    player = voice.play(
        source, after=lambda x=None: check_queue(ctx, ctx.guild.id))


@client.command(pass_context=True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    source = discord.FFmpegPCMAudio(arg)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx.send("Added to queue")


pf = ProfanityFilter()

@client.event
async def on_message(message):
    if pf.is_profane(message.content):
        await message.delete()
        await message.channel.send("Your message contains profanity and cannot be processed.")
        return

TOKEN = os.getenv('BOT_AUTH')
client.run(TOKEN)
