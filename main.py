"""
Discord bot main file.
"""
import discord
import asyncio
import signal
import re
from discord.ext.commands import Bot
from datetime import datetime
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


@client.event
async def on_ready():
    activity = discord.Game(name=">help", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if url_regex.search(message.content):
        url = url_regex.search(message.content).group(1)
        result = detect_url(url)
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


async def main():
    async with client:
        await client.add_cog(Channel(client))
        # youtube-dl is not working, so temporarily disable music
        # await client.add_cog(Music(client))
        await client.add_cog(Moderation(client))
        await client.add_cog(R18(client))
        await client.start(MyToken)

# singal handler
def signal_handler(signal, frame):
    print("Exiting...")
    exit(0)


if  __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(main())
