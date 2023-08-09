import asyncio
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl


intents = discord.Intents().all
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='/', intents=intents)