"""
Music cog for the bot.
"""
import discord
import asyncio
import random
import datetime
from discord.ext import commands
from core.function.yt import YTDLSource, search
from core.function.logger import LogCommand

log = LogCommand()

class Music(commands.Cog):

    """
    Music commands. As youtube-dl problem is not solved, this cog is not working.
    """

    def __init__(self, bot):
        self.client = bot
        self.playlist = []
        self.file = discord.File("./image/youtube.png", filename="youtube.png")

    @commands.command(pass_context=True, name="Play", aliases=['play'], help="Plays a song")
    async def play(self, ctx, *, name):

        """
        Plays a song.
        """

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
        log.info(ctx.author, "Run command Play")

    async def play_next(self, ctx):

        """
        Plays the next song in the playlist.
        """

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
        log.info(ctx.author, "Run command Play_next")

    @commands.command(pass_context=True, name="Pause", aliases=['pause'], help="Pauses the song")
    async def pause(self, ctx):

        """
        Pauses the song.
        """

        try:
            server = ctx.message.guild.voice_client
            server.pause()
            await ctx.send("**" + "Paused the song" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Pause")

    @commands.command(pass_context=True, name="Resume", aliases=['resume'], help="Resumes the song")
    async def resume(self, ctx):

        """
        Resumes the song.
        """

        try:
            server = ctx.message.guild.voice_client
            server.resume()
            await ctx.send("**" + "Resumed the song" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Resume")

    @commands.command(pass_context=True, name="Stop", aliases=['stop'], help="Stops the song")
    async def stop(self, ctx):

        """
        Stops the song.
        """

        try:
            server = ctx.message.guild.voice_client
            server.stop()
            await ctx.send("**" + "Stopped the song" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Stop")

    @commands.command(pass_context=True, name="NowPlaying", aliases=['np', 'nowplaying'],
                      help="Shows the song that is currently playing")
    async def now_playing(self, ctx):

        """
        Shows the song that is currently playing.
        """

        try:
            server = ctx.message.guild.voice_client
            await ctx.send("**" + "Now playing: " + "**" + server.source.title)
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Now_playing")

    # TODO: Fix volume command (not working)
    # @commands.command(pass_context=True, name="Volume", aliases=['volume'], help="Changes the volume")
    # async def volume(self, ctx: commands.Context, *, volume):

    #     """
    #     Changes the volume.
    #     """

    #     try:
    #         server = ctx.message.guild.voice_client
    #         server.source.volume = float(volume) / 100
    #         await ctx.send("**" + "Changed the volume to " + volume + "**")
    #     except AttributeError:
    #         await ctx.send("I am not connected to a voice channel")
    #     log.info(ctx.author, "Run command Volume")

    # @volume.error
    # async def volume_error(self, ctx, error):

    #     """
    #     Error handler for volume.
    #     """

    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("**Please specify a volume**")
    #     else:
    #         await ctx.send("**An error occurred**")
    #         print(error)

    @commands.command(pass_context=True, name="Join", aliases=['join'], help="Joins the voice channel")
    async def join(self, ctx: commands.Context):

        """
        Joins the voice channel.
        """

        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send("**" + "Joined " + str(channel) + "**")
        else:
            await ctx.send("You are not connected to a voice channel")
        log.info(ctx.author, "Run command Join")

    @join.error
    async def join_error(self, ctx, error):
            
            """
            Error handler for join.
            """
    
            ctx.send("**An error occurred**")
            print(error)

    @commands.command(pass_context=True, name="Leave", aliases=['disconnect', 'leave'], help="Leaves the voice channel")
    async def leave(self, ctx):

        """
        Leaves the voice channel.
        """

        try:
            server = ctx.message.guild.voice_client
            await server.disconnect()
            await ctx.send("**" + "Left the voice channel" + "**")
            self.playlist.clear()
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Leave")

    @commands.command(pass_context=True, name="Queue", aliases=['queue'], help="Shows the queue")
    async def queue(self, ctx):

        """
        Shows the queue.
        """

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
        log.info(ctx.author, "Run command Queue")

    @commands.command(pass_context=True, name="Add", aliases=['add'], help="Adds a song to the queue")
    async def add(self, ctx, *, name):

        """
        Adds a song to the queue.
        """

        try:
            urlJson = search(name)
            urlN = urlJson['title']
            self.playlist.append(urlN)
            await ctx.send("**" + "Added " + urlJson['title'] + " to the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Add")

    @add.error
    async def add_error(self, ctx, error):

        """
        Error handler for add.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**" + "Please specify a song" + "**")
        else:
            print(error)
            await ctx.send("**" + "An error occurred" + "**")

    @commands.command(pass_context=True, name="Remove", aliases=['remove'], help="Removes a song from the queue")
    async def remove(self, ctx, *, number: int):

        """
        Removes a song from the queue.
        """

        try:
            self.playlist.pop(int(number) - 1)
            await ctx.send("**" + "Removed song from the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Remove")

    @remove.error
    async def remove_error(self, ctx, error):

        """
        Error handler for remove.
        """

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**" + "Please specify a song" + "**")
        else:
            print(error)
            await ctx.send("**" + "An error occurred" + "**")

    @commands.command(pass_context=True, name="ClearQueue", aliases=['clearqueue', 'cq'], help="Clears the queue")
    async def clear_queue(self, ctx):

        """
        Clears the queue.
        """

        try:
            self.playlist.clear()
            await ctx.send("**" + "Cleared the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command ClearQueue")

    @commands.command(pass_context=True, name="Shuffle", aliases=['shuffle'], help="Shuffles the queue")
    async def shuffle(self, ctx):

        """
        Shuffles the queue.
        """

        try:
            random.shuffle(self.playlist)
            await ctx.send("**" + "Shuffled the queue" + "**")
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Shuffle")

    @commands.command(pass_context=True, name="Skip", aliases=['skip'], help="Skips the song")
    async def skip(self, ctx):

        """
        Skips the song.
        """

        try:
            server = ctx.message.guild.voice_client
            server.stop()
            await self.play(ctx, self.playlist[0])
            await ctx.send("**" + "Skipped the song" + "**")
            self.playlist.pop(0)
        except AttributeError:
            await ctx.send("I am not connected to a voice channel")
        log.info(ctx.author, "Run command Skip")
