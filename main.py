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

    @bot.command(name = 'play')
    async def play(ctx, url):
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
             filename = await YTDLSource.from_url(url, loop = bot.loop)
             voice_channel.play(discord.FFmpegPCMAudio(executable = "", source = filename))
        await ctx.send('**Now Playing:** {}'.format(filename))

    @bot.command(name = 'pause')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
              await voice_client.pause()
        else:
             await ctx.send("The bot has pauses the music")

    @bot.command(name = 'resume')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
              await voice_client.resume()
        else:
             await ctx.send("The bot is not playing music")

    @bot.command(name = 'leave')
    async def leave(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
              await voice_client.disconnected()
        else:
             await ctx.send("The bot has not join a voice channel")
