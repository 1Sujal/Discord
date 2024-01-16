import discord
from discord.ext import commands
from pytube import YouTube
from PIL import Image, ImageFilter
import pytesseract


# Define your bot's token
TOKEN = 'Bot token'

intents = discord.Intents.default()
intents.typing = False  
intents.presences = False
intents.messages = True
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def download(ctx, url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    mp3_filename = f"{yt.title}.mp3"
    audio_stream.download(output_path=".", filename=mp3_filename)
    await ctx.send(content=f"Audio from **{yt.title}** (MP3 format):", file=discord.File(mp3_filename))
    
bot.run(TOKEN)
