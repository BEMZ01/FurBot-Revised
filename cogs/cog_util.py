import random
import discord
from discord.ext import commands, tasks
from util.util import process_string


class utilCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.display_rotation = 0
        self.guilds = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("UTIL: Cog loaded")
        print("UTIL: Loading censor list")
        # read the censor list from file
        with open("storage/bad-words.txt", "r") as f:
            # strip any whitespace from the lines
            bad_words = f.read().strip(" ").splitlines()
        self.guilds = [guild.name for guild in self.bot.guilds]
        for i, name in enumerate(self.guilds):
            for word in bad_words:
                if word in name:
                    print(f"UTIL: Found bad word in guild name: {name}")
                    self.guilds[i] = self.guilds[i].replace(word, "*" * len(word))
        print("UTIL: Finished loading censor list")
        self.update_display.start()
        print("UTIL: Started update_display loop")

    @tasks.loop(seconds=30)
    async def update_display(self):
        guild = random.choice(self.guilds)
        await self.bot.wait_until_ready()
        if self.display_rotation == 0:
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(self.bot.guilds)} s"
                                                                                   f"ervers."))
        elif self.display_rotation == 1:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                                     name=f"with {guild}!"))
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

    @commands.slash_command(name="shard", description="Get the shard ID and info for the current guild")
    async def shard(self, ctx: discord.ApplicationContext):
        shard: discord.ShardInfo = self.bot.get_shard(ctx.guild.shard_id)
        shard_count: int = shard.shard_count
        shard_ping: float = round(shard.latency * 1000, 1)
        num_servers = len([guild for guild in self.bot.guilds if guild.shard_id == ctx.guild.shard_id])
        em = discord.Embed(title=f"FurBot Shard Info", description=f"Shard ID: {ctx.guild.shard_id}")
        em.add_field(name="Shard Count", value=f"{shard_count}")
        em.add_field(name="Shard Ping", value=f"{shard_ping}ms")
        em.add_field(name="Servers", value=f"{num_servers}")
        em.add_field(name="Total Servers", value=f"{len(self.bot.guilds)}")
        await ctx.respond(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("an:"):
            await message.channel.send(f"The `an:` prefix is deprecated. Please use the newer discord slash "
                                       f"commands instead. Type `/` to see a list of commands from supported bots.")



def setup(bot):
    bot.add_cog(utilCmds(bot))
