import discord
import asyncio
import random
import nsfw_dl
import time
import cv2
import os
import re
from environs import Env
from pyotp import TOTP
from datetime import datetime
from requests import Session, get
from func import YTDLSource, search, get_token, detect_url
from discord.ext.commands import Bot, has_permissions
from discord.ext import commands

# Bot token
MyToken = get_token()

intents = discord.Intents.default()
intents.message_content = True

# description & command_prefix
client = Bot(command_prefix=">", intents=intents, description="My Command List")
url_regex = re.compile(r'(https?://\S+)')


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
        if result != False:
            embed = discord.Embed()
            embed.add_field(name="URL Detected", value="警告请不要散播有害链接，你的消息将被删除", inline=False)
            embed.set_footer(text="Oren Bot")
            embed.color = discord.Color.red()
            embed.timestamp = datetime.utcnow()
            await message.delete()
            await message.channel.send(embed=embed)



class Channel(commands.Cog):

    def __int__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="CreateChannel", aliases=["cc"], help="Creates a channel")
    @has_permissions(administrator=True)
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            await guild.create_text_channel(channel_name)
            new_channel = discord.utils.get(guild.channels, name=channel_name)
            await new_channel.edit(topic="Created by " + ctx.author.name + " with using oren bot")
            await new_channel.edit(category=ctx.channel.category)
            await ctx.send("**" + "Channel " + channel_name + " created successfully" + "**")
        else:
            await ctx.send("**" + "Channel " + channel_name + " already exists" + "**")

    @create_channel.error
    async def create_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel already exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="DeleteChannel", aliases=["dc"], help="Deletes a channel")
    @has_permissions(administrator=True)
    async def delete_channel(self, ctx, channel_name: discord.TextChannel):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.delete()
            await ctx.send("**" + "Channel " + str(channel_name) + " deleted successfully" + "**")
        else:
            await ctx.send("**" + "Channel " + str(channel_name) + " doesn't exist" + "**")

    @delete_channel.error
    async def delete_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel doesn't exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="RenameChannel", aliases=["rc"], help="Renames a channel")
    @has_permissions(administrator=True)
    async def rename_channel(self, ctx, channel_name: discord.TextChannel, new_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.edit(name=new_name)
            await ctx.send("**" + "Channel " + str(channel_name) + " renamed successfully" + "**")

    @rename_channel.error
    async def rename_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel doesn't exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="Clear", aliases=["clear"], help="Clears the chat")
    @has_permissions(administrator=True)
    async def clear(self, ctx, num):
        if num.isdigit():
            await ctx.channel.purge(limit=int(num) + 1)
            await ctx.send("**" + "Cleared " + num + " messages successfully" + "**", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a number of messages to clear**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**An error occurred**")
            print(error)
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="SlowMode", aliases=["sm"], help="Sets the slowmode")
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, channel_name: discord.TextChannel, seconds):
        if seconds.isdigit():
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
            if existing_channel:
                await existing_channel.edit(slowmode_delay=int(seconds))
                await ctx.send("**" + "Slowmode in " + str(channel_name) + " set to " + seconds + " seconds" + "**")

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name and a number of seconds**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel doesn't exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="NSFW", aliases=["nsfw"], help="Sets the channel to NSFW")
    @has_permissions(manage_channels=True)
    async def nsfw(self, ctx, channel_name: discord.TextChannel):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.edit(nsfw=True)
            await ctx.send("**" + "Channel " + str(channel_name) + " set to NSFW" + "**")

    @nsfw.error
    async def nsfw_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel doesn't exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="SFW", aliases=["sfw"], help="Sets the channel to SFW")
    @has_permissions(manage_channels=True)
    async def sfw(self, ctx, channel_name: discord.TextChannel):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.edit(nsfw=False)
            await ctx.send("**" + "Channel " + str(channel_name) + " set to SFW" + "**")

    @sfw.error
    async def sfw_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel doesn't exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)


class Music(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.playlist = []
        self.file = discord.File("./image/youtube.png", filename="youtube.png")

    @commands.command(pass_context=True, name="Play", aliases=['play'], help="Plays a song")
    async def play(self, ctx, *, name):
        try:
            server = ctx.message.guild.voice_client
            if server.is_playing():
                reJson = search(name)
                self.playlist.append(reJson['title'])
                await ctx.send("**" + reJson['title'] + " added to the playlist" + "**")
            else:
                urlJson = search(name)
                urlN = urlJson['webpage_url']
                player = await YTDLSource.from_url(urlN, loop=self.client.loop, stream=True)
                server.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx),
                                                                                     self.client.loop))
                await ctx.send("**" + "Now playing: " + "**" + urlJson['title'])
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    async def play_next(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            try:
                urlJson = search(self.playlist[0])
                urlN = urlJson['webpage_url']
                player = await YTDLSource.from_url(urlN, loop=self.client.loop, stream=True)
                server.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx),
                                                                                     self.client.loop))
                await ctx.send("**" + "Now playing: " + "**" + urlJson['title'])
                self.playlist.pop(0)
            except IndexError:
                await ctx.send("**" + "Playlist is empty" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Pause", aliases=['pause'], help="Pauses the song")
    async def pause(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            server.pause()
            await ctx.send("**" + "Paused the song" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Resume", aliases=['resume'], help="Resumes the song")
    async def resume(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            server.resume()
            await ctx.send("**" + "Resumed the song" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Stop", aliases=['stop'], help="Stops the song")
    async def stop(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            server.stop()
            await ctx.send("**" + "Stopped the song" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="NowPlaying", aliases=['np', 'nowplaying'],
                      help="Shows the song that is currently playing")
    async def now_playing(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            await ctx.send("**" + "Now playing: " + "**" + server.source.title)
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Volume", aliases=['volume'], help="Changes the volume")
    async def volume(self, ctx, *, volume):
        try:
            server = ctx.message.guild.voice_client
            server.source.volume = float(volume) / 100
            await ctx.send("**" + "Changed the volume to " + volume + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @volume.error
    async def volume_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a volume**")
        else:
            await ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="Join", aliases=['join'], help="Joins the voice channel")
    async def join(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send("**" + "Joined " + str(channel) + "**")
        else:
            await ctx.send("You are not connected to a voice channel")

    @commands.command(pass_context=True, name="Leave", aliases=['disconnect', 'leave'], help="Leaves the voice channel")
    async def leave(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            await server.disconnect()
            await ctx.send("**" + "Left the voice channel" + "**")
            self.playlist.clear()
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Queue", aliases=['queue'], help="Shows the queue")
    async def queue(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            if self.playlist:
                embed = discord.Embed(title="Oren's Playlist", color=0x00ff00)
                embed.set_author(name=self.client.user.name)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text="Requested by " + ctx.message.author.name)
                embed.set_thumbnail(url="attachment://youtube.png")
                num = 1
                for i in self.playlist:
                    embed.add_field(name="**[" + str(num) + "]**", value=i, inline=False)
                    num += 1
                await ctx.send(embed=embed, file=self.file)
            else:
                await ctx.send("**" + "The queue is empty" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Add", aliases=['add'], help="Adds a song to the queue")
    async def add(self, ctx, *, name):
        try:
            urlJson = search(name)
            urlN = urlJson['title']
            self.playlist.append(urlN)
            await ctx.send("**" + "Added " + urlJson['title'] + " to the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**" + "Please specify a song" + "**")
        else:
            print(error)
            await ctx.send("**" + "An error occurred" + "**")

    @commands.command(pass_context=True, name="Remove", aliases=['remove'], help="Removes a song from the queue")
    async def remove(self, ctx, *, number: int):
        try:
            self.playlist.pop(int(number) - 1)
            await ctx.send("**" + "Removed song from the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**" + "Please specify a song" + "**")
        else:
            print(error)
            await ctx.send("**" + "An error occurred" + "**")

    @commands.command(pass_context=True, name="ClearQueue", aliases=['clearqueue', 'cq'], help="Clears the queue")
    async def clear_queue(self, ctx):
        try:
            self.playlist.clear()
            await ctx.send("**" + "Cleared the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Shuffle", aliases=['shuffle'], help="Shuffles the queue")
    async def shuffle(self, ctx):
        try:
            random.shuffle(self.playlist)
            await ctx.send("**" + "Shuffled the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")

    @commands.command(pass_context=True, name="Skip", aliases=['skip'], help="Skips the song")
    async def skip(self, ctx):
        try:
            server = ctx.message.guild.voice_client
            server.stop()
            await self.play(ctx, self.playlist[0])
            await ctx.send("**" + "Skipped the song" + "**")
            self.playlist.pop(0)
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="Kick", aliases=['kick'], help="Kicks a user")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'**{member} has been kicked by {ctx.author.mention}\nReason: {reason}**')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a user to kick**")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("**User not found**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I don't have permission to do that**")
        else:
            await ctx.send("**Something went wrong**")
            print(error)

    @commands.command(pass_context=True, name="Ban", aliases=['ban'], help="Bans a user")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'**{member} has been banned by {ctx.author.mention}\nReason: {reason}**')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a user to ban**")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("**User not found**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I don't have permission to do that**")
        else:
            await ctx.send("**Something went wrong**")
            print(error)

    @commands.command(pass_context=True, name="Unban", aliases=['unban'], help="Unbans a user")
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member):
        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'**{user} has been unbanned by {ctx.author.mention}**')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a user to unban**")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("**User not found**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I don't have permission to do that**")
        else:
            await ctx.send("**Something went wrong**")
            print(error)

    @commands.command(pass_context=True, name="CreateRole", aliases=['createrole', 'cr'], help="Creates a role")
    @has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, name):
        await ctx.guild.create_role(name=name)
        await ctx.send(f'**{name} has been created**')

    @create_role.error
    async def create_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a role name**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I don't have permission to do that**")
        else:
            await ctx.send("**Something went wrong**")
            print(error)

    @commands.command(pass_context=True, name="DeleteRole", aliases=['deleterole', 'dr'], help="Deletes a role")
    @has_permissions(manage_roles=True)
    async def delete_role(self, ctx, *, name: discord.Role):
        await name.delete()
        await ctx.send(f'**{name} has been deleted**')

    @delete_role.error
    async def delete_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a role name**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I don't have permission to do that**")
        else:
            await ctx.send("**Something went wrong**")
            print(error)


class R18(commands.Cog):

    def __init__(self, bot):
        # (Can't use or don't want use) Nhentai, Tsumino, Tbib, Lolibooru, Konachan(Search), Hbrowse, Gelbooru
        # Furrybooru, E621, Danbooru, Drunkenpumken
        self.bot = bot
        self.NSFW = nsfw_dl.NSFWDL(session=Session())

    @commands.command(pass_context=True, name="rule34", aliases=['r34'], help="Random rule34 image")
    @commands.is_nsfw()
    async def rule34(self, ctx):
        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('Rule34Random'))

    @rule34.error
    async def rule34_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            print(error)

    @commands.command(pass_context=True, name="Yandere", aliases=['yandere'], help="Random yandere image")
    @commands.is_nsfw()
    async def yandere(self, ctx):
        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('YandereRandom'))

    @yandere.error
    async def yandere_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            print(error)

    @commands.command(pass_context=True, name="Xbooru", aliases=['xbooru'], help="Random xbooru image")
    @commands.is_nsfw()
    async def xbooru(self, ctx):
        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('XbooruRandom'))

    @xbooru.error
    async def xbooru_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            print(error)

    @commands.command(pass_context=True, name="XbooruSearch", aliases=['xboorus'], help="Searches xbooru")
    @commands.is_nsfw()
    async def xbooru_search(self, ctx, *, name):
        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('XbooruSearch', name))

    @xbooru_search.error
    async def xbooru_search_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            print(error)

    @commands.command(pass_context=True, name="Konachan", aliases=['konachan'], help="Random konachan image")
    @commands.is_nsfw()
    async def konachan(self, ctx):
        self.NSFW.load_default()
        url = self.NSFW.download('KonachanRandom').replace("https:", "")
        await ctx.send("https:" + url)

    @konachan.error
    async def konachan_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            print(error)


class Function(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.owner_key = Env()
        self.owner_key.read_env()
        self.owner_key = self.owner_key.str('OWNER_SECRET_KEY')
        self.owner_key = TOTP(self.owner_key)

    @commands.command(pass_context=True, name="ReadQR", aliases=['rqr', 'readqr'], help="Reads a QR code")
    async def read_qr(self, ctx):
        start = time.time()
        try:
            embed = discord.Embed(title="Read QR")
            for attachment in ctx.message.attachments:
                if attachment.content_type.split("/")[0] != "image":
                    embed.add_field(name="Error", value="**```Please attach an image```**")
                    embed.set_footer(text="Error no a image")
                    embed.colour = discord.Colour.red()
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
                elif attachment.content_type.split("/")[1] == "svg+xml":
                    embed.add_field(name="Error", value="**```We reject .svg file```**")
                    embed.set_footer(text="Error no .svg file")
                    embed.colour = discord.Colour.red()
                    embed.timestamp = datetime.utcnow()
                    await ctx.send(embed=embed)
                else:
                    message = await ctx.send("**Saving image...**")
                    await attachment.save("qr.png")
                    await message.edit(content="**Reading QR code...**")
                    img = cv2.imread("qr.png")
                    detector = cv2.QRCodeDetector()
                    data, bbox, straight_qrcode = detector.detectAndDecode(img)
                    end_time = time.time() - start
                    embed.add_field(name="Message from your QR Code", value="**```" + data + "```**", inline=False)
                    embed.add_field(name="Time", value="**`" + str(round(end_time, 2)) + "s`**", inline=False)
                    embed.set_footer(text="Read QR Success")
                    embed.colour = discord.Colour.purple()
                    embed.timestamp = datetime.utcnow()
                    await message.edit(content="**Done**", embed=embed)
                    os.remove("qr.png")

        except Exception as e:
            print(e)
            
    @commands.command(pass_context=True, name="Ping", aliases=['ping'], help="Ping a website")
    async def ping_(self, ctx, url):
        """
            :url: A url
        """
        embed = discord.Embed(title="Ping Response")
        message = await ctx.send(f"Pinging {url}, please wait for a while")
        try:
            url_engine = get(url=url, timeout=5).status_code
            if url_engine == 200:
                embed.add_field(name="Status Code", value='**`200`**', inline=False)
                embed.color = discord.Colour.green()
                embed.add_field(name="Status", value=f"**```Website: {url} Online```**", inline=False)
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text=f"Responses: {url_engine}")
                await message.edit(content="", embed=embed)
        except Exception as e:
            print(e)
            await ctx.send(e)

    @commands.command(pass_context=True, name="AddSchedule", aliases=['addschedule', 'as'], help="Add a schedule")
    async def add_schedule(self, ctx, *, name, otp = "123456"):
        """
            :name: Name of the schedule
        """
        if self.owner_key.verify(otp):
            id  = random.randint(100000, 999999)
            embed = discord.Embed(title="Add Schedule ID: " + str(id))
            embed.add_field(name="Name", value="**`" + name + "`**", inline=False)
            embed.add_field(name="Schedule", value="**`" + str(datetime.utcnow()) + "`**", inline=False)
            embed.set_footer(text="Add Schedule Success")
            embed.colour = discord.Colour.purple()
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
            with open("schedule.txt", 'a+') as f:
                f.write(str(id) + " " + name + " " + str(datetime.utcnow()) + "\n")
                f.close()
        else:
            await ctx.send("Invalid OTP or did not enter OTP")

    @commands.command(pass_context=True, name="RemoveSchedule", aliases=['removeschedule', 'rs'], help="Remove a schedule")
    async def remove_schedule(self, ctx, *, ID, otp = "123456"):
        """
            :name: Name of the schedule
        """
        if self.owner_key.verify(otp):
            with open("schedule.txt", 'r') as f:
                lines = f.readlines()
                f.close()
            with open("schedule.txt", 'w') as f:
                for line in lines:
                    if line.split()[0] != ID:
                        f.write(line)
                    name = line.split()[1]
                    schedule = line.split()[2]
                f.close()
            embed = discord.Embed(title="Remove Schedule ID: " + str(ID))
            embed.add_field(name="Name", value="**`" + name + "`**", inline=False)
            embed.add_field(name="Created Date", value="**`" + schedule + "`**", inline=False)
            embed.set_footer(text="Remove Schedule Success")
            embed.colour = discord.Colour.purple()
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid OTP or did not enter OTP")

    @commands.command(pass_context=True, name="Schedule", aliases=['schedule'], help="Show all schedule")
    async def schedule_(self, ctx, *, otp = "123456"):
        if self.owner_key.verify(otp):
            embed = discord.Embed(title="Schedule")
            with open("schedule.txt", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    embed.add_field(name="ID: " + line.split()[0], value="**`" + line.split()[1] + "`**", inline=False)
            embed.set_footer(text="Schedule")
            embed.colour = discord.Colour.purple()
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid OTP or did not enter OTP")


async def main():
    async with client:
        await client.add_cog(Channel(client))
        await client.add_cog(Music(client))
        await client.add_cog(Moderation(client))
        await client.add_cog(R18(client))
        await client.add_cog(Function(client))
        await client.start(MyToken)


asyncio.run(main())
