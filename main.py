"""
Discord bot main file.
"""
import asyncio
import signal
import re
import sys
import discord
import platform
from datetime import datetime
from discord.ext.commands import Bot
from func import get_token, detect_url, is_google_api_key_set
from core.function.logger import LogCommand
from core.function.utility import which

# import cogs
from core.channel import Channel
from core.moderation import Moderation
from core.music import Music
from core.nsfw import R18

# Bot token
MyToken = get_token()

intents = discord.Intents.all()

# description & command_prefix
prefix = ">"
client = Bot(command_prefix=prefix, intents=intents, description="My Command List")
url_regex = re.compile(r'(https?://\S+)')

log = LogCommand()

try:
    google_safe_browsing_api, google_api_key = is_google_api_key_set()
except Exception as e:
    google_api_key = None
    google_safe_browsing_api = False
if google_safe_browsing_api is False:
    log.warn("BOT", "Google Safe Browsing API key is not set, bot stop scanning message")

@client.event
async def on_ready():
    activity = discord.Game(name=f"{prefix}help", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if google_safe_browsing_api and url_regex.search(message.content) is not None:
            url = url_regex.search(message.content).group(1)
            result = detect_url(url, google_api_key)
            if result:
                embed = discord.Embed()
                embed.add_field(name="URL Detected", value="Found a harmful link", inline=False)
                embed.set_footer(text="Oren Bot")
                embed.color = discord.Color.red()
                embed.timestamp = datetime.now()
                await message.delete()
                await message.channel.send(embed=embed)
                log.warn(message.author, "Sent a harmful link")
            else:
                await client.process_commands(message)
    else:
        await client.process_commands(message)


ffmpeg_name = "ffmpeg"
if platform.system() == "Windows":
    ffmpeg_name = "ffmpeg.exe"
elif platform.system() == "Linux":
    ffmpeg_name = "ffmpeg"
elif platform.system() == "Darwin":
    ffmpeg_name = "ffmpeg"
else:
    ffmpeg_name = None

async def main_entry():
    async with client:
        await client.add_cog(Channel(client))
        await client.add_cog(Moderation(client))
        await client.add_cog(R18(client))
        if which(ffmpeg_name):
            await client.add_cog(Music(client))
        else:
            log.warn("BOT", "ffmpeg is not installed, music function is disabled")
        await client.start(MyToken)

# singal handler
def signal_handler(_signal, _frame):
    print("Exiting...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main_entry())


if __name__ == "__main__":
    main()
