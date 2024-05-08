# This python script will be imported into other python files and will provide some useful functions
import io
import aiohttp
import discord
from PIL import Image


async def Generate_color(image_url: str):
    """Generate a similar color to the album cover of the song.
    :param image_url: The url of the album cover.
    :return discord.Color: A discord color.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            if resp.status != 200:
                return discord.Color.blurple()
            f = io.BytesIO(await resp.read())
    image = Image.open(f)
    # Get average color of the image
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


def nsfw_check(tags, ctx):
    if is_dm(ctx):
        return tags + " -rating:safe"
    if not ctx.channel.is_nsfw():
        tags += " rating:safe"
    else:
        tags += " -rating:safe"
    return tags


def is_dm(ctx):
    return ctx.channel.type is discord.ChannelType.private


def check_safe(string: str):
    # Check if the string contains any of the words from storage/bad-words.txt
    with open("storage/bad-words.txt", "r") as f:
        bad_words = f.read().splitlines()
    for word in bad_words:
        if word in string:
            return False
    return True


def process_string(string: str):
    # Remove any bad words from the string
    with open("storage/bad-words.txt", "r") as f:
        bad_words = f.read().splitlines()
    for word in bad_words:
        string = string.replace(word, "*" * len(word))
    return string
# Path: util\util.py
