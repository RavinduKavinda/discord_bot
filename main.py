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

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warning':True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ''

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):  
          loop = loop or asyncio.get_event_loop()
          data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
          if 'entries' in data:
               data = data['entries'][0]
               filename = data['title'] if stream else ytdl.prepare_filename(data)
               return filename
          

    @bot.command(name = 'join')
    async def join(ctx):
        if not ctx.message.author.voice:
              await ctx.send("Please {} connected to a voice channel".format(ctx.massage.author.name))
              return
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

            