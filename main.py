import asyncio
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl

load_dotenv()
DISCORD_TOKEN = os.getenv("MTEzODc4NzQ1NTYwNTE0OTc5Nw.Gd_uR2.6T6IAjpD_VovI4-D4QQZHeHY7G7mcVyukzetzQ")

intents = discord.Intents().all
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='/', intents=intents)