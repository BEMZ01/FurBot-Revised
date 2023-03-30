import discord
from discord.commands import options
from discord.ext import commands
import e621 as e6


def check_nsfw(ctx: discord.ApplicationContext):
    # if channel is marked as nsfw or is inside a DM
    if ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel):
        return True
    else:
        return False


class nsfwCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.e621 = e6.E621()

    @commands.slash_command(name="e621", description="E621 related commands")
    async def e621(self, ctx: discord.ApplicationContext, tags: str = None):
        if check_nsfw(ctx):
            ...
        else:
            await ctx.respond(f"Please use this command in a NSFW channel!", delete_after=5, ephemeral=True)


def setup(bot):
    bot.add_cog(nsfwCmds(bot))
