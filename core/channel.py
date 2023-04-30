"""
Channel cog for the bot.
"""
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from core.function.logger import LogCommand

log = LogCommand()

class Channel(commands.Cog):

    """
    Channel commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="CreateChannel", aliases=["cc"], help="Creates a channel")
    @has_permissions(administrator=True)
    async def create_channel(self, ctx, channel_name):

        """
        Creates a channel.
        """

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
        log.info(ctx.author, "Run command CreateChannel")

    @create_channel.error
    async def create_channel_error(self, ctx, error):

        """
        Error handler for create_channel.
        """

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

        """
        Deletes a channel.
        """

        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.delete()
            await ctx.send("**" + "Channel " + str(channel_name) + " deleted successfully" + "**")
        else:
            await ctx.send("**" + "Channel " + str(channel_name) + " doesn't exist" + "**")
        log.info(ctx.author, "Run command DeleteChannel")

    @delete_channel.error
    async def delete_channel_error(self, ctx, error):

        """
        Error handler for delete_channel.
        """

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

        """
        Renames a channel.
        """

        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.edit(name=new_name)
            await ctx.send("**" + "Channel " + str(channel_name) + " renamed successfully" + "**")
        log.info(ctx.author, "Run command RenameChannel")

    @rename_channel.error
    async def rename_channel_error(self, ctx, error):

        """
        Error handler for rename_channel.
        """

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

        """
        Clears the chat.
        """

        if num.isdigit():
            await ctx.channel.purge(limit=int(num) + 1)
            await ctx.send("**" + "Cleared " + num + " messages successfully" + "**", delete_after=5)
        log.info(ctx.author, "Run command Clear")

    @clear.error
    async def clear_error(self, ctx, error):

        """
        Error handler for clear.
        """

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

        """
        Sets the slowmode.
        """

        if seconds.isdigit():
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
            if existing_channel:
                await existing_channel.edit(slowmode_delay=int(seconds))
                await ctx.send("**" + "Slowmode in " + str(channel_name) + " set to " + seconds + " seconds" + "**")
        log.info(ctx.author, "Run command SlowMode")

    @slowmode.error
    async def slowmode_error(self, ctx, error):

        """
        Error handler for slowmode.
        """

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

        """
        Sets the channel to NSFW.
        """

        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.edit(nsfw=True)
            await ctx.send("**" + "Channel " + str(channel_name) + " set to NSFW" + "**")
        log.info(ctx.author, "Run command NSFW")

    @nsfw.error
    async def nsfw_error(self, ctx, error):

        """
        Error handler for nsfw.
        """

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

        """
        Sets the channel to SFW.
        """

        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, id=channel_name.id)
        if existing_channel:
            await existing_channel.edit(nsfw=False)
            await ctx.send("**" + "Channel " + str(channel_name) + " set to SFW" + "**")
        log.info(ctx.author, "Run command SFW")

    @sfw.error
    async def sfw_error(self, ctx, error):

        """
        Error handler for sfw.
        """

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a channel name**")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("**Channel doesn't exists**")
        else:
            await ctx.send("**An error occurred**")
            print(error)
