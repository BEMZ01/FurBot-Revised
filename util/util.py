# This python script will be imported into other python files and will provide some useful functions
import io

import aiohttp
import discord
from PIL import Image


async def Generate_color(image_url):
    """Generate a similar color to the album cover of the song.
    :param image_url: The url of the album cover.
    :return: The color of the album cover."""

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            if resp.status != 200:
                return discord.Color.blurple()
            f = io.BytesIO(await resp.read())
    image = Image.open(f)
    # Get adverage color of the image
    colors = image.getcolors(image.size[0] * image.size[1])
    # Sort the colors by the amount of pixels and get the most common color
    colors.sort(key=lambda x: x[0], reverse=True)
    # Get the color of the most common color
    color = colors[0][1]
    try:
        if len(color) != 3:
            return discord.Color.blurple()
    except TypeError:
        return discord.Color.blurple()
    # Convert the color to a discord color
    return discord.Color.from_rgb(color[0], color[1], color[2])


def check_nsfw(ctx: discord.ApplicationContext):
    # if channel is marked as nsfw or is inside a DM
    if ctx.channel.is_nsfw() or isinstance(ctx.channel, discord.DMChannel):
        return True
    else:
        return False
# Path: util\util.py