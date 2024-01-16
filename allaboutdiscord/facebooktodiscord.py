import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

bot_prefix = '!'
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

last_link = ""

async def perform_facebook_task():
    driver = webdriver.Chrome('Chrome Driver Path')
    driver.get('https://mbasic.facebook.com/login')
    email = driver.find_element(By.NAME, 'email')
    email.send_keys('Facebook email')  # Replace with your actual email
    password = driver.find_element(By.NAME, 'pass')
    password.send_keys('Facebook password')  # Replace with your actual password
    login = driver.find_element(By.NAME, 'login')
    login.click()
    test = driver.find_element(By.CLASS_NAME, 'bn')
    test.click()
    driver.get('Group you want to extract of')

    # Video path
    video_link_element = driver.find_element(By.XPATH, '//a[@aria-label="Watch video"]')
    video_link_element.click()

    rvideo_link_element = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Watch video"]'))
    )
    video_link_element.click()
    driver.switch_to.window(driver.window_handles[-1])
    redirect_url = driver.current_url
    print("Redirected URL:", redirect_url)

    driver.quit()

    return redirect_url

async def download_and_upload_task(ctx):
    global last_link  # Use the global variable to store the last link
    while True:
        redirect_url = await perform_facebook_task()

        if redirect_url != last_link:
            response = requests.get(redirect_url)

            if response.status_code == 200:
                with open('downloaded_video.mp4', 'wb') as f:
                    f.write(response.content)

                await ctx.send(file=discord.File('downloaded_video.mp4'))
            else:
                await ctx.send("Failed to download the video.")

            last_link = redirect_url

            #set the time after which you want it to extract post again(minimum 2 minutes)
            await asyncio.sleep(900)

@bot.command()
async def download_and_upload(ctx):
    bot.loop.create_task(download_and_upload_task(ctx))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Run the bot with your token
bot.run("Bot token")

