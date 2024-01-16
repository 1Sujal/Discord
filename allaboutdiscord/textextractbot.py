import discord
from discord.ext import commands
from PIL import Image, ImageFilter
import pytesseract

intents = discord.Intents.default()
intents.typing = False  # Disable typing event
intents.presences = False
intents.messages = True
intents.message_content = True #v2

bot_prefix = '!'
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def extract_text(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach an image.")
        return

    attachment = ctx.message.attachments[0]

    await attachment.save("input_image.png")

    image = Image.open("input_image.png")
    image = image.filter(ImageFilter.SHARPEN)
    image = image.convert("L") 

    text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    # Use 'eng' for English language, adjust for other languages

    await ctx.send(f"Extracted Text:\n```{text}```")

bot.run("Bot token")
