import youtube_dl
import discord
import asyncio
import requests
import json
import urllib
import pyotp
import qrcode
from requests import get
from environs import Env

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def search(query):
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(query)
        except:
            search_ = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else:
            search_ = ydl.extract_info(query, download=False)

    return search_


def get_token() -> str:
    env = Env()
    env.read_env()
    return env.str("DISCORD_TOKEN")

def detect_url(message):
    env = Env()
    env.read_env()
    api_url = "https://ipqualityscore.com/api/json/url/" + env.str("IPQUALITYSCORE_API_KEY") + "/"
    encoded_url = urllib.parse.quote(message, safe='')
    data = requests.get(api_url + encoded_url)
    return json.dumps(data.json(), indent=4)

def genereate_otp_qr():
    env = Env()
    env.read_env()
    owner = env.str("OWNER_SECRET_KEY")
    totp = pyotp.totp.TOTP(owner).provisioning_uri(name="OrenBotSchedule", issuer_name="OrenBot")
    print(totp)
    qrcode.make(totp).save("qrcode.png")
