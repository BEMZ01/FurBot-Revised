import random

import discord
from discord.ext import commands, tasks


class utilCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.display_rotation = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print("UTIL: Started update_display loop")
        self.update_display.start()

    @tasks.loop(seconds=30)
    async def update_display(self):
        await self.bot.wait_until_ready()
        if self.display_rotation == 0:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.guilds)} servers."))
        elif self.display_rotation == 1:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Hello {random.choice(self.bot.guilds).name}!"))
        elif self.display_rotation == 2:
            self.display_rotation = -1
        self.display_rotation += 1



    @commands.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.slash_command(name="invite", description="Get the bot's invite link")
    async def invite(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Check my profile for my invite link! I hope you find my commands useful!")

    @commands.slash_command(name="vote", description="Get the bot's vote link")
    async def vote(self, ctx: discord.ApplicationContext):
        # Create a button that links to the bot's vote link
        button = discord.ui.Button(label="Top.gg", url=f"https://top.gg/bot/716259432878702633/vote")
        # Create a message with the button
        message = discord.ui.View()
        message.add_item(button)
        # Send the message
        await ctx.respond("Vote for me on top.gg!", view=message)

    @commands.slash_command(name="links", description="Get links to various sites about the bot")
    async def links(self, ctx: discord.ApplicationContext):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Invite", url="https://top.gg/bot/716259432878702633/invite", emoji="📩"))
        view.add_item(discord.ui.Button(label="Vote", url="https://top.gg/bot/716259432878702633/vote", emoji="🗳"))
        view.add_item(discord.ui.Button(label="Top.gg", url="https://top.gg/bot/716259432878702633", emoji="📈"))
        view.add_item(discord.ui.Button(label="Support", url="https://discord.gg/WSCCBe7", emoji="📞"))
        view.add_item(discord.ui.Button(label="Website", url="https://bemz.info/", emoji="🌐"))
        view.add_item(discord.ui.Button(label="Github", url="https://github.com/BEMZ01/FurBot-Revised", emoji="📦"))
        embed = discord.Embed(title="Links", description="Here are some links to various sites about the bot!")
        await ctx.respond(embed=embed, view=view, ephemeral=True, delete_after=60)

def setup(bot):
    bot.add_cog(utilCmds(bot))