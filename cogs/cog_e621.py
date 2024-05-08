import os
import random
import discord
from discord.ext import commands
import e621 as e6
from dotenv import load_dotenv
from discord import option
from util.util import Generate_color, nsfw_check

load_dotenv()


class e621Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = e6.E621(client_name="FurBot")
        self.tag_blacklist = ["-webm", "-child", "-flash", "-cub"]
        self.again_button = discord.ui.Button(label="Again", style=discord.ButtonStyle.primary, emoji="🔁")
        self.close_button = discord.ui.Button(label="Close", style=discord.ButtonStyle.danger, emoji="❌")

    e621 = discord.SlashCommandGroup(name="e621", description="Get images from e621")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.vote_message = discord.ui.View()
        self.vote_message.add_item(discord.ui.Button(label="Top.gg", url=f"https://top.gg/bot/716259432878702633/vote"))

    async def cog_command_error(self, ctx: discord.ApplicationContext, error):
        await ctx.respond(error.original, delete_after=10, ephemeral=True)
        raise error

    async def close_callback(self, interaction: discord.Interaction):
        if interaction.user.id == interaction.message.author.id:
            await interaction.message.delete()
            return True
        else:
            await interaction.response.send_message("You can't use this button", ephemeral=True)
            return False

    @e621.command(name="top", description="Get the top posts from e621")
    @option(name="tags", description="The tags to search for", required=False)
    async def top(self, ctx: discord.ApplicationContext, tags: str = None):
        await ctx.defer()
        otags = tags
        if tags is None:
            tags = ""
        elif ", " in tags:
            tags = tags.replace(", ", " ")
        tags += " order:score"
        tags = nsfw_check(tags, ctx)
        # add a space before each tag in the blacklist then add it to the tags
        for tag in self.tag_blacklist:
            tags += f" {tag}"
        posts = self.api.posts.search(tags=tags, limit=1, page=1)
        if len(posts) == 0 or posts[0].file_obj is None:
            await ctx.respond("No posts found with those tags", ephemeral=True)
            return
        embed = discord.Embed(title="Top post", description=f"Tags: {otags}",
                              color=await Generate_color(posts[0].preview.url),
                              url=f"https://e621.net/posts/{str(posts[0].id)}")
        embed.add_field(name="Score", value=f"{posts[0].score.up + posts[0].score.down} "
                                            f"(↑{posts[0].score.up} ↓{str(posts[0].score.down).strip('-')})")
        embed.add_field(name="Rating", value=posts[0].rating)
        embed.add_field(name="Description", value=posts[0].description[:1024])
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        embed.set_image(url=posts[0].file_obj.url)
        await ctx.respond(embed=embed, ephemeral=True)

    @e621.command(name="random", description="Get a random post from e621")
    @option(name="tags", description="The tags to search for", required=False)
    async def random(self, ctx: discord.ApplicationContext, tags: str = None):
        async def r_callback(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                # edit the embed with a new post
                post = random.choice(self.api.posts.search(tags=tags))
                embed = discord.Embed(title="Random post", description=f"Tags: {otags}",
                                      color=await Generate_color(post.preview.url),
                                      url=f"https://e621.net/posts/{str(post.id)}")
                embed.add_field(name="Score", value=f"{post.score.up + post.score.down} "
                                                    f"(↑{post.score.up} ↓{str(post.score.down).strip('-')})")
                embed.add_field(name="Rating", value=post.rating)
                embed.add_field(name="Description", value=post.description[:1024])
                embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot",
                                 icon_url=f"{ctx.author.display_avatar.url}")
                embed.set_image(url=post.file_obj.url)
                await interaction.response.edit_message(embed=embed, view=view)
                return True
            else:
                await interaction.response.send_message("You can't use this button", ephemeral=True)
                return False
        await ctx.defer()
        otags = tags
        if tags is None:
            tags = ""
        elif ", " in tags:
            tags = tags.replace(", ", " ")
        # add a space before each tag in the blacklist then add it to the tags
        for tag in self.tag_blacklist:
            tags += f" {tag}"
        tags = nsfw_check(tags, ctx)
        posts = self.api.posts.search(tags=tags)
        try:
            post = random.choice(posts)
        except IndexError:
            await ctx.respond("No posts found with those tags", ephemeral=True, delete_after=10)
            return
        if len(posts) == 0 or post.file_obj is None:
            await ctx.respond("No posts found with those tags", ephemeral=True, delete_after=10)
            return
        embed = discord.Embed(title="Random post", description=f"Tags: {otags}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.add_field(name="Score", value=f"{post.score.up + post.score.down} "
                                            f"(↑{post.score.up} ↓{str(post.score.down).strip('-')})")
        embed.add_field(name="Rating", value=post.rating)
        embed.add_field(name="Description", value=post.description)
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        embed.set_image(url=post.file_obj.url)
        view = discord.ui.View()
        view.add_item(self.again_button)
        view.add_item(self.close_button)
        self.again_button.callback = r_callback
        self.close_button.callback = self.close_callback
        await ctx.respond(embed=embed, ephemeral=True, view=view)

    @e621.command(name="gif", description="Get a random gif from e621")
    @option(name="tags", description="The tags to search for", required=False)
    async def gif(self, ctx: discord.ApplicationContext, tags: str = None):
        async def g_callback(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                # edit the embed with a new post
                post = random.choice(self.api.posts.search(tags=tags))
                if len(posts) == 0 or posts[0].file_obj is None:
                    return False
                embed = discord.Embed(title="Random gif", description=f"Tags: {otags}",
                                      color=await Generate_color(post.preview.url),
                                      url=f"https://e621.net/posts/{str(post.id)}")
                embed.add_field(name="Score", value=f"{post.score.up + post.score.down} "
                                                    f"(↑{post.score.up} ↓{str(post.score.down).strip('-')})")
                embed.add_field(name="Rating", value=post.rating)
                embed.add_field(name="Description", value=post.description[:1024])
                embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot",
                                 icon_url=f"{ctx.author.display_avatar.url}")
                embed.set_image(url=post.file_obj.url)
                await interaction.response.edit_message(embed=embed, view=view, delete_after=240)
                return True
            else:
                await interaction.response.respond("You can't use this button", ephemeral=True, delete_after=10)
                return False
        await ctx.defer()
        otags = tags
        if tags is None:
            tags = ""
        elif ", " in tags:
            tags = tags.replace(", ", " ")
        tags += " animated"
        # add a space before each tag in the blacklist then add it to the tags
        for tag in self.tag_blacklist:
            tags += f" {tag}"
        tags = nsfw_check(tags, ctx)
        posts = self.api.posts.search(tags=tags)
        try:
            post = random.choice(posts)
        except IndexError:
            await ctx.respond("No posts found with those tags", ephemeral=True, delete_after=10)
            return
        if len(posts) == 0 or post.file_obj is None:
            await ctx.respond("No posts found with those tags", ephemeral=True, delete_after=10)
            return
        embed = discord.Embed(title="Random gif", description=f"Tags: {otags}",
                              color=await Generate_color(post.preview.url),
                              url=f"https://e621.net/posts/{str(post.id)}")
        embed.add_field(name="Score", value=f"{post.score.up + post.score.down} "
                                            f"(↑{post.score.up} ↓{str(post.score.down).strip('-')})")
        embed.add_field(name="Rating", value=post.rating)
        embed.add_field(name="Description", value=post.description[0:1024])
        embed.set_footer(text=f"Command ran by {str(ctx.author)} | FurBot", icon_url=f"{ctx.author.display_avatar.url}")
        embed.set_image(url=post.file_obj.url)
        view = discord.ui.View()
        view.add_item(self.close_button)
        view.add_item(self.again_button)
        self.close_button.callback = self.close_callback
        self.again_button.callback = g_callback
        await ctx.respond(embed=embed, ephemeral=True, view=view, delete_after=240)


def setup(bot):
    bot.add_cog(e621Cmds(bot))
