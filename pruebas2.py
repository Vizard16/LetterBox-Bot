import settings
import random
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
import json
from letterboxdpy import movie


logger = settings.logging.getLogger("bot")

# Function to fetch poster URL from Letterboxd movie page
def fetch_poster_url(movie_url):
    r = requests.get(movie_url)
    soup = bs(r.text, 'html.parser')
    script_w_data = soup.select_one('script[type="application/ld+json"]')
    json_obj = json.loads(script_w_data.text.split(' */')[1].split('/* ]]>')[0])
    return json_obj['image']

# Function to fetch movie description
def fetch_movie_description(movie_instance):
    return movie.movie_description(movie_instance)

# Function to fetch popular reviews for a movie
def fetch_popular_reviews(movie_instance):
    return movie.movie_popular_reviews(movie_instance)

def fetch_movie_runtime(movie_url):
    r = requests.get(movie_url)
    soup = bs(r.text, 'html.parser')
    runtime_element = soup.find("p", class_="text-link text-footer")
    if runtime_element:
        runtime_text = runtime_element.text.strip()
        # Extract the runtime from the text
        runtime = runtime_text.split("\n")[0].strip()
        return runtime
    return "N/A"  # Return N/A if runtime not found
def create_movie_embed(movie_data):
    # Capitalize the first letter of the first word in the movie title and replace hyphens with spaces
    title = movie_data["title"].capitalize().replace("-", " ")
    
    # Randomly select a popular review
    random_review = random.choice(movie_data["popular_reviews"])
    
    # Create an embedded message with movie data and the random review
    embed = discord.Embed(
        title=title,
        url=movie_data["url"],
        description=" ",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=movie_data["poster"])
    embed.add_field(name="Directors", value=", ".join(movie_data["directors"]), inline=False)
    # Add fields for rating, director, runtime, and genres
    embed.add_field(name=":star: User Rating", value=str(movie_data["rating"]), inline=True)
    
    embed.add_field(name=":alarm_clock: Runtime", value=movie_data["runtime"], inline=True)
    embed.add_field(name="Genres", value=", ".join(movie_data["genres"]), inline=False)

    # Add the description field
    embed.add_field(name="Description", value=movie_data["description"], inline=False)

    # Add the random review to the embedded message
    embed.add_field(name=f"Random Review by {random_review['reviewer']}", value=f"Rating: {random_review['rating']}\nReview: {random_review['review']}", inline=False)

    # Fetch the image URL from the website
    image_url = fetch_backdrop_image(movie_data["url"])
    if image_url:
        # Set the image URL in the embed
        embed.set_image(url=image_url)
    
    return embed

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
