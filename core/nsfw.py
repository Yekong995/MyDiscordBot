"""
NSFW cog for the bot.
"""
import os
import discord
import nsfw_dl
from requests import Session
from discord.ext import commands
from core.function.logger import LogCommand
from core.function.nsfw_base import Rule34

log = LogCommand()

class R18(commands.Cog):

    """
    NSFW commands
    """

    def __init__(self, bot):
        # (Can't use or don't want use) Nhentai, Tsumino, Tbib, Lolibooru, Konachan(Search), Hbrowse, Gelbooru
        # Furrybooru, E621, Danbooru, Drunkenpumken
        self.bot = bot
        self.NSFW = nsfw_dl.NSFWDL(session=Session())
        self.R34 = Rule34()

    @commands.command(pass_context=True, name="rule34", aliases=['r34'], help="Random rule34 image")
    @commands.is_nsfw()
    async def rule34(self, ctx: commands.Context):

        """
        Random rule34 image.
        """

        link = self.R34.random_image()
        await ctx.send(file=discord.File(link))
        os.remove(link)
        log.info(ctx.author, "Run command rule34")

    @rule34.error
    async def rule34_error(self, ctx, error):

        """
        Error handler for rule34.
        """

        if isinstance(error, commands.NSFWChannelRequired):
            log.warn(ctx.author, "Run command rule34 in non-NSFW channel")
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            log.error(ctx.author, "Error in command rule34")
            print(error)

    @commands.command(pass_context=True, name="rule34search", aliases=['r34s'], help="Search rule34 image")
    @commands.is_nsfw()
    async def rule34search(self, ctx: commands.Context, *, title: str):
            
            """
            Search rule34 image.
            """
    
            link = self.R34.search_img(title)
            file_name = self.R34.get_img_by_id(link)
            await ctx.send(file=discord.File(file_name))
            os.remove(file_name)
            log.info(ctx.author, "Run command rule34search")

    @rule34search.error
    async def rule34search_error(self, ctx, error):
            
            """
            Error handler for rule34search.
            """
    
            if isinstance(error, commands.NSFWChannelRequired):
                log.warn(ctx.author, "Run command rule34search in non-NSFW channel")
                await ctx.send("**This command can only be used in NSFW channels**")
            else:
                await ctx.send("**An error has occurred**")
                log.error(ctx.author, "Error in command rule34search")
                print(error)

    @commands.command(pass_context=True, name="Yandere", aliases=['yandere'], help="Random yandere image")
    @commands.is_nsfw()
    async def yandere(self, ctx: commands.Context):

        """
        Random yandere image.
        """

        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('YandereRandom'))
        log.info(ctx.author, "Run command yandere")

    @yandere.error
    async def yandere_error(self, ctx, error):

        """
        Error handler for yandere.
        """

        if isinstance(error, commands.NSFWChannelRequired):
            log.warn(ctx.author, "Run command yandere in non-NSFW channel")
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            log.error(ctx.author, "Error in command yandere")
            print(error)

    @commands.command(pass_context=True, name="Xbooru", aliases=['xbooru'], help="Random xbooru image")
    @commands.is_nsfw()
    async def xbooru(self, ctx: commands.Context):

        """
        Random xbooru image.
        """

        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('XbooruRandom'))
        log.info(ctx.author, "Run command xbooru")

    @xbooru.error
    async def xbooru_error(self, ctx, error):

        """
        Error handler for xbooru.
        """

        if isinstance(error, commands.NSFWChannelRequired):
            log.warn(ctx.author, "Run command xbooru in non-NSFW channel")
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            log.error(ctx.author, "Error in command xbooru")
            print(error)

    @commands.command(pass_context=True, name="XbooruSearch", aliases=['xboorus'], help="Searches xbooru")
    @commands.is_nsfw()
    async def xbooru_search(self, ctx: commands.Context, *, name):

        """
        Searches xbooru.
        """

        self.NSFW.load_default()
        await ctx.send(self.NSFW.download('XbooruSearch', name))
        log.info(ctx.author, "Run command xbooru_search")

    @xbooru_search.error
    async def xbooru_search_error(self, ctx, error):

        """
        Error handler for xbooru_search.
        """

        if isinstance(error, commands.NSFWChannelRequired):
            log.warn(ctx.author, "Run command xbooru_search in non-NSFW channel")
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            log.error(ctx.author, "Error in command xbooru_search")
            print(error)

    @commands.command(pass_context=True, name="Konachan", aliases=['konachan'], help="Random konachan image")
    @commands.is_nsfw()
    async def konachan(self, ctx: commands.Context):

        """
        Random konachan image.
        """

        self.NSFW.load_default()
        url = self.NSFW.download('KonachanRandom').replace("https:", "")
        await ctx.send("https:" + url)
        log.info(ctx.author, "Run command konachan")

    @konachan.error
    async def konachan_error(self, ctx, error):

        """
        Error handler for konachan.
        """

        if isinstance(error, commands.NSFWChannelRequired):
            log.warn(ctx.author, "Run command konachan in non-NSFW channel")
            await ctx.send("**This command can only be used in NSFW channels**")
        else:
            await ctx.send("**An error has occurred**")
            log.error(ctx.author, "Error in command konachan")
            print(error)
