import settings
import random
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents= intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command(
            aliases=['p'],
            help = "This is help",
            description = "This is description",
            brief = "This is brief",
            enabled = True,
            hidden = True
    )

    async def ping(ctx):
        """Answers with Pong"""
        await ctx.send("pong")

    @bot.command()
    async def say(ctx, *what):
        if not what:
        # If no arguments provided, default to "WHAT?"
            what = ["WHAT?"]
        await ctx.send(" ".join(what))

    @bot.command()
    async def choices(ctx, *options):
        await ctx.send(random.choice(options))


    @bot.command()
    async def say3(ctx, what = "WHAT?", why= "WHY?"):
        await ctx.send(what + why)
        

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()

