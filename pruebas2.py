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

def fetch_trailer_url(movie_url):
    # Make a GET request to the movie URL
    response = requests.get(movie_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = bs(response.content, 'html.parser')
        
        # Find the anchor tag with class 'play' inside which the trailer URL is located
        trailer_tag = soup.find('a', class_='play')
        
        # Check if the trailer tag is found
        if trailer_tag:
            # Get the value of the 'href' attribute, which contains the trailer URL
            trailer_url = trailer_tag.get('href')
            
            # Modify the URL to include the protocol 'https:'
            trailer_url = f"https:{trailer_url}"
            
            return trailer_url
    
    # Return None if the trailer URL is not found or there was an error
    return None

# Function to fetch movie description
def fetch_movie_description(movie_instance):
    return movie.movie_description(movie_instance)


def fetch_movie_details(movie_instance):
    details = movie.movie_details(movie_instance)
    print(f"Type of details: {type(details)}")  # Add this line
    details_str = ""
    if isinstance(details, dict):
        if 'Country' in details:
            details_str += f"**Country**: {', '.join(details['Country'])}\n"
        if 'Language' in details:
            details_str += f"**Language**: {', '.join(details['Language'])}\n"
    return details_str

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

def get_movie_info(movie_title):
    # Capitalize the first letter of each word in the movie title
    movie_title = movie_title.title()
    
    # Create a movie instance
    movie_instance = movie.Movie(movie_title)

    # Fetch the poster URL for the movie
    poster_url = fetch_poster_url(movie_instance.url)

    description = fetch_movie_description(movie_instance)

    # Fetch popular reviews for the movie
    reviews = fetch_popular_reviews(movie_instance)

    # Fetch runtime for the movie
    runtime = fetch_movie_runtime(movie_instance.url)

    # Construct the movie data dictionary
    movie_data = {
        "title": movie_instance.title,
        "url": movie_instance.url,
        "directors": movie_instance.directors,
        "rating": movie_instance.rating,
        "year": movie_instance.year,
        "genres": movie_instance.genres,
        "poster": poster_url,
        "description": description,
        "popular_reviews": reviews,  # Add popular reviews to movie data
        "runtime": runtime  # Add runtime to movie data
    }

    return movie_data

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
