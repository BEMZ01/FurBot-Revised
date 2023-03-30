import discord
from discord.ext import commands


class utilCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.slash_command(name="invite", description="Get the bot's invite link")
    async def invite(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Check my profile for my invite link! I hope you find my commands useful!")

    @commands.slash_command(name="info", description="Get info about any user")
    async def info(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(title=f"{user.name}'s info", description=f"User ID: {user.id}", color=0x00ff00)
        embed.add_field(name="Joined at", value=user.joined_at)
        embed.add_field(name="Created at", value=user.created_at)
        await ctx.respond(embed=embed, ephemeral=True, delete_after=30)

def setup(bot):
    bot.add_cog(utilCmds(bot))