import discord
import dotenv
import os
import logging
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(debug_guilds=[867773426773262346])
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename.startswith('cog_'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

if __name__ == "__main__":
    bot.run(TOKEN, reconnect=True)
