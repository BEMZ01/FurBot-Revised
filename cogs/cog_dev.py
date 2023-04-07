import asyncio
import discord
from util.util import Generate_color, nsfw_check
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
        embed = discord.Embed(title="Announcement", description=message)
        info_message = await ctx.respond("Announcing... (0%)", embed=embed)
        # send the announcement to the first channel we can access
        for i, guild in enumerate(self.bot.guilds):
            for channel in guild.channels:
                if channel.permissions_for(guild.me).send_messages and type(channel) == discord.TextChannel:
                    try:
                        await channel.send(embed=embed)
                    except Exception as e:
                        print(f"Failed to send announcement to {channel.name} in {guild.name}:\n{e} (1/2)")
                        await asyncio.sleep(60)
                        # try again
                        try:
                            await channel.send(embed=embed)
                        except Exception as e:
                            print(f"Failed to send announcement to {channel.name} in {guild.name}:\n{e} (2/2)")
                        finally:
                            break
                    finally:
                        break
            print(f"Announcing... ({round((i + 1) / len(self.bot.guilds) * 100)}%)")
            if i % 10 == 0:
                await info_message.edit(content=f"Announcing... ({round((i + 1) / len(self.bot.guilds) * 100)}%)")


def setup(bot):
    bot.add_cog(DevCmds(bot))
