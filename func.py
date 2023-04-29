import youtube_dl
import discord
import asyncio
import requests
import colorama
import datetime
import pprint
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
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
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
            search_ = ydl.extract_info(f"ytsearch:{query}", download=False)[
                'entries'][0]
        else:
            search_ = ydl.extract_info(query, download=False)

    return search_


def get_token() -> str:
    env = Env()
    env.read_env()
    return env.str("DISCORD_TOKEN")


def detect_url(message: str):
    env = Env()
    env.read_env()
    apikey = env.str("GOOGLE_SAFE_BROWSING_API_KEY")
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    content_json = {
        "client": {
            "clientId": "OrenBot",
            "clientVersion": "0.0.1"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": message},
            ]
        }
    }
    result = requests.post(api_url, json=(content_json), params={'key': apikey})
    re_json = result.json()
    if re_json == {}:
        return False
    else:
        if "matches" in re_json:
            return True
        else:
            return False
        

class LogCommand():

    def __init__(self) -> None:
        super(LogCommand, self).__init__()
        # D/M/Y H:M:S
        self.current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def info(self, author: str, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTBLUE_EX}{author}{colorama.Fore.RESET} > {colorama.Fore.LIGHTGREEN_EX}{msg}{colorama.Fore.RESET}"
        print(msg)
    
    def error(self, author: str, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTBLUE_EX}{author}{colorama.Fore.RESET} > {colorama.Fore.LIGHTRED_EX}{msg}{colorama.Fore.RESET}"
        print(msg)
    
    def warn(self, author: str, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTBLUE_EX}{author}{colorama.Fore.RESET} > {colorama.Fore.YELLOW}{msg}{colorama.Fore.RESET}"
        print(msg)

    def log_err_code(self, msg: str) -> None:
        msg = f"{colorama.Fore.BLUE}{self.current_time} {colorama.Fore.LIGHTMAGENTA_EX}{msg}{colorama.Fore.RESET}"
        pprint.pprint(msg)
