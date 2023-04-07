import discord
import dotenv
import os
import logging
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(owner_id=234248229426823168)
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename.startswith('cog_'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')
        except discord.errors.ExtensionFailed as e:
            print(f'Failed to load {filename[:-3]}')
            print(e)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord for {len(bot.guilds)} guilds!')

if __name__ == "__main__":
    bot.run(TOKEN, reconnect=True)
