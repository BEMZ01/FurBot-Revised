import asyncio
from pprint import pprint

import discord
from util.util import Generate_color, check_nsfw
from discord.ext import commands


class DevCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: discord.ApplicationContext):
        if ctx.author.id == self.bot.owner_id:
            return True
        else:
            await ctx.respond("This command can only be used by the bot owner", ephemeral=True)
            return False

    dev = discord.SlashCommandGroup(name="dev", description="Developer commands")

    async def cog_command_error(self, ctx: discord.ApplicationContext, error):
        await ctx.respond(error.original, delete_after=10, ephemeral=True)
        raise error

    @dev.command(name="reload", description="Reload a cog")
    async def reload(self, ctx: discord.ApplicationContext):
        async def reload_callback(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.defer()
                cog = interaction.data["values"][0]
                print(f"Reloading {cog}")
                try:
                    self.bot.reload_extension(f"{cog}")
                except Exception as e:
                    await interaction.edit_original_response(content=f"Failed to reload {cog}:\n{e}", view=None)
                    await asyncio.sleep(10)
                    await interaction.delete_original_response()
                    return
                await interaction.edit_original_response(content=f"Reloaded {cog}", view=None)
                await asyncio.sleep(10)
                await interaction.delete_original_response()
            else:
                return False
        await self.bot.wait_until_ready()
        cogs = [discord.SelectOption(label=cog, value=cog) for cog in self.bot.extensions.keys()]
        view = discord.ui.View()
        select = discord.ui.Select(options=cogs, placeholder="Select a cog to reload", min_values=1, max_values=1)
        select.callback = reload_callback
        view.add_item(select)
        await ctx.respond("Select a cog to reload", view=view)

    @dev.command(name="announce", description="Announce something")
    async def announce(self, ctx: discord.ApplicationContext, *, message: str):
        await ctx.defer()
        embed = discord.Embed(title="Announcement", description=message, color=0x00ff00)
        # send the announcement to the first channel we can access
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.permissions_for(guild.me).send_messages and type(channel) == discord.TextChannel:
                    try:
                        await channel.send(embed=embed)
                    except Exception as e:
                        await asyncio.sleep(15)
                        pass
                    break
            print(f"Announced to {guild.name} ({round((self.bot.guilds.index(guild) + 1) / len(self.bot.guilds) * 100, 2)}%)")


def setup(bot):
    bot.add_cog(DevCmds(bot))
