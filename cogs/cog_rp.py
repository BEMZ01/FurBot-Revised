import random
import discord
from discord.ext import commands
from e621 import E621
from util.util import Generate_color


class RolePlay_cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = E621()
        self.tag_blacklist = ["-webm", "-child", "rating:s", "animated", "-flash"]

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.vote_button = discord.ui.Button(label="Top.gg", url=f"https://top.gg/bot/716259432878702633/vote")
        self.vote_message = discord.ui.View()
        self.vote_message.add_item(self.vote_button)

    rp = discord.SlashCommandGroup(name="roleplay", description="Roleplay commands")

    @rp.command(name="hug")
    async def hug(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        posts = self.api.posts.search(tags="hug " + " ".join(self.tag_blacklist), limit=100)
        post = random.choice(posts)
        # create the embed
        embed = discord.Embed(title="Hug", description=f"{ctx.author.mention} hugs {member.mention}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.set_image(url=post.file_obj.url)
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Source", url=f"https://e621.net/posts/{str(post.id)}"))
        view.add_item(discord.ui.Button(label="Vote", url=f"https://top.gg/bot/716259432878702633/vote"))
        await ctx.respond(embed=embed, view=view, delete_after=120)

    @rp.command(name="kiss")
    async def kiss(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        posts = self.api.posts.search(tags="kissing " + " ".join(self.tag_blacklist), limit=100)
        post = random.choice(posts)
        embed = discord.Embed(title="Kiss", description=f"{ctx.author.mention} <3 {member.mention}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.set_image(url=post.file_obj.url)
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Source", url=f"https://e621.net/posts/{str(post.id)}"))
        view.add_item(discord.ui.Button(label="Vote", url=f"https://top.gg/bot/716259432878702633/vote"))
        await ctx.respond(embed=embed, view=view, delete_after=120)

    @rp.command(name="boop")
    async def boop(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        posts = self.api.posts.search(tags="boop " + " ".join(self.tag_blacklist), limit=100)
        post = random.choice(posts)
        embed = discord.Embed(title="Boop", description=f"{ctx.author.mention} boops {member.mention}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.set_image(url=post.file_obj.url)
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Source", url=f"https://e621.net/posts/{str(post.id)}"))
        view.add_item(discord.ui.Button(label="Vote", url=f"https://top.gg/bot/716259432878702633/vote"))
        await ctx.respond(embed=embed, view=view, delete_after=120)

    @rp.command(name="lick")
    async def lick(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        posts = self.api.posts.search(tags="licking " + " ".join(self.tag_blacklist), limit=100)
        post = random.choice(posts)
        embed = discord.Embed(title="Lick", description=f"{ctx.author.mention} licks {member.mention}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.set_image(url=post.file_obj.url)
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Source", url=f"https://e621.net/posts/{str(post.id)}"))
        view.add_item(discord.ui.Button(label="Vote", url=f"https://top.gg/bot/716259432878702633/vote"))
        await ctx.respond(embed=embed, view=view, delete_after=120)

    @rp.command(name="pet")
    async def pet(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        posts = self.api.posts.search(tags="petting " + " ".join(self.tag_blacklist), limit=100)
        post = random.choice(posts)
        embed = discord.Embed(title="Pet", description=f"{ctx.author.mention} pets {member.mention}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.set_image(url=post.file_obj.url)
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Source", url=f"https://e621.net/posts/{str(post.id)}"))
        view.add_item(discord.ui.Button(label="Vote", url=f"https://top.gg/bot/716259432878702633/vote"))
        await ctx.respond(embed=embed, view=view, delete_after=120)
def setup(bot):
    bot.add_cog(RolePlay_cmds(bot))
