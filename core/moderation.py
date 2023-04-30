"""
Moderation cog for the bot.
"""
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from core.function.logger import LogCommand

log = LogCommand()

class Moderation(commands.Cog):

    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="Kick", aliases=['kick'], help="Kicks a user")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        """
        Kicks a user.
        """

        await member.kick(reason=reason)
        await ctx.send(f'**{member} has been kicked by {ctx.author.mention}\nReason: {reason}**')
        log.info(ctx.author, "Run command Kick")

    @kick.error
    async def kick_error(self, ctx, error):

        """
        Error handler for kick.
        """

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

        """
        Bans a user.
        """

        await member.ban(reason=reason)
        await ctx.send(f'**{member} has been banned by {ctx.author.mention}\nReason: {reason}**')
        log.info(ctx.author, "Run command Ban")

    @ban.error
    async def ban_error(self, ctx, error):

        """
        Error handler for ban.
        """

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

        """
        Unbans a user.
        """

        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'**{user} has been unbanned by {ctx.author.mention}**')
        log.info(ctx.author, "Run command Unban")

    @unban.error
    async def unban_error(self, ctx, error):

        """
        Error handler for unban.
        """

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

        """
        Creates a role.
        """

        await ctx.guild.create_role(name=name)
        await ctx.send(f'**{name} has been created**')
        log.info(ctx.author, "Run command CreateRole")

    @create_role.error
    async def create_role_error(self, ctx, error):

        """
        Error handler for create_role.
        """

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

        """
        Deletes a role.
        """

        await name.delete()
        await ctx.send(f'**{name} has been deleted**')
        log.info(ctx.author, "Run command DeleteRole")

    @delete_role.error
    async def delete_role_error(self, ctx, error):

        """
        Error handler for delete_role.
        """

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have permission to do that**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please specify a role name**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I don't have permission to do that**")
        else:
            await ctx.send("**Something went wrong**")
            print(error)
