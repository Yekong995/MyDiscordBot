"""
Discord bot main file.
"""
import asyncio
import signal
import re
import sys
import discord
from datetime import datetime
from discord.ext.commands import Bot
from environs import Env
from functools import wraps
from func import get_token, detect_url
from core.function.logger import LogCommand

# import cogs
from core.channel import Channel
from core.moderation import Moderation
# from core.music import Music # youtube-dl is not working, so temporarily disable music
from core.nsfw import R18

# Bot token
MyToken = get_token()

intents = discord.Intents.all()

# description & command_prefix
client = Bot(command_prefix=">", intents=intents, description="My Command List")
url_regex = re.compile(r'(https?://\S+)')

log = LogCommand()

google_api_key = Env()
google_api_key.read_env()
google_api_key = google_api_key.str("GOOGLE_SAFE_BROWSING_API_KEY")
is_google_api_key_set = False if google_api_key == "" else True

if is_google_api_key_set is False:
    log.warn("BOT", "Google Safe Browsing API key is not set, bot stop scanning message")

@client.event
async def on_ready():
    activity = discord.Game(name=">help", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if is_google_api_key_set is True:
        if url_regex.search(message.content):
            url = url_regex.search(message.content).group(1)
            result = detect_url(url, google_api_key)
            if result is not False:
                embed = discord.Embed()
                embed.add_field(name="URL Detected", value="警告请不要散播有害链接，你的消息将被删除", inline=False)
                embed.set_footer(text="Oren Bot")
                embed.color = discord.Color.red()
                embed.timestamp = datetime.utcnow()
                await message.delete()
                await message.channel.send(embed=embed)
                log.warn(message.author, "Sent a harmful link")
    else:
        await client.process_commands(message)


async def main_entry():
    async with client:
        await client.add_cog(Channel(client))
        # youtube-dl is not working, so temporarily disable music
        # await client.add_cog(Music(client))
        await client.add_cog(Moderation(client))
        await client.add_cog(R18(client))
        await client.start(MyToken)

# singal handler
def signal_handler(_signal, _frame):
    print("Exiting...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main_entry())

main()
