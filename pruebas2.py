import settings
import random
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
import json
from letterboxdpy import movie


logger = settings.logging.getLogger("bot")

def fetch_backdrop_image(movie_url):
    r = requests.get(movie_url)
    if r.status_code == 200:
        html_content = r.text
        soup = bs(html_content, 'html.parser')
        backdrop_element = soup.find("div", class_="backdrop-wrapper")
        if backdrop_element:
            # Extract the image URL from the data-backdrop attribute
            image_url = backdrop_element.get("data-backdrop")
            return image_url
    return None



def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents= intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def say(ctx, *what):
        if not what:
        # If no arguments provided, default to "WHAT?"
            what = ["WHAT?"]
        await ctx.send(" ".join(what))

    @bot.command()
    async def movie_info(ctx, *, movie_title):
        """Fetches information about a movie"""
        movie_data = get_movie_info(movie_title)
        embed = create_movie_embed(movie_data)
        await ctx.send(embed=embed)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()
