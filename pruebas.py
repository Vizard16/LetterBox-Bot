import discord
from discord.ext import commands
from typing import Optional
import settings

logger = settings.logging.getLogger("bot")

# Custom converter for the command
class CommandConverter(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.replace(" ", "_")  # Replace spaces with underscores
     # Check for specific aliases
        aliases = {"corazón_de_hielo": "corazon_de_hielo",
                   "new_alias": "corresponding_command",

                   }
        

        # Use the alias if it exists, otherwise use the original argument
        return aliases.get(argument, argument)
   

async def corazon_de_hielo_embed(ctx):  # Accept ctx as an argument (even though it's not used)
    titulo = "Descripción"
    descripcion = (
        "Este ítem te permite mitigar el daño recibido de autoataques al igual que reducir la velocidad de ataque "
        "de los campeones que se encuentren cerca de ti en un 20%"
    )
    eficiencia = "Eficiencia de oro\nTiene un costo de 2400G y una eficiencia de 123%"

    # Lista de campeones con sus nombres
    buenos_con = ["Nasus", "Malphite", "Udyr", "Ryze", "Nautilus"]
    buenos_contra = ["Varus", "Kalista", "Kaisa", "Maestro Yi", "Twitch"]

    # Enviar el embed con la información y la imagen combinada
    embed = discord.Embed(
        title=titulo,
        description=f"{descripcion}\n\n**{eficiencia}**",
        color=0x3498db  # Puedes cambiar el color según tus preferencias
    )

    # Añade un campo para los campeones "Bueno Con"
    embed.add_field(name="Bueno Con", value=", ".join(buenos_con), inline=False)
    embed.add_field(name="Bueno Contra", value=", ".join(buenos_contra), inline=False)

    # Establece una miniatura (thumbnail) en el embed
    embed.set_thumbnail(
        url='https://static.wikia.nocookie.net/leagueoflegendsoficial/images/1/18/Frozen_Heart.png/revision/latest?cb=20220401022257&path-prefix=es')
    
    await ctx.send(embed=embed)  # Use await ctx.send instead of returning the embed

async def rukerno_kaenico_embed(ctx):
    titulo = "Descripción"
    descripcion = (
        "Al no recibir daño durante 12 segundos crearás un escudo contra daño mágico del 20% de tu vida"

    )
    eficiencia = "Eficiencia de oro\nTiene un costo de 2900G y una eficiencia de 102%"

    # Lista de campeones con sus nombres
    buenos_con = ["Sion", "Ornn", "K'Sante", "Shen", "Bardo", "Malphite"]
    buenos_contra = ["Daño AP: Syndra", "Akali", "Vex", "Fizz", "Diana", "Brand"]

    # Enviar el embed con la información y la imagen combinada
    embed = discord.Embed(
        title=titulo,
        description=f"{descripcion}\n\n**{eficiencia}**",
        color=0x3498db  # Puedes cambiar el color según tus preferencias
    )

    # Añade un campo para los campeones "Bueno Con"
    embed.add_field(name="Bueno Con", value=", ".join(buenos_con), inline=False)
    embed.add_field(name="Bueno Contra", value=", ".join(buenos_contra), inline=False)

    # Establece una miniatura (thumbnail) en el embed
    embed.set_thumbnail(
        url='https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt90434f1c8fc3405d/6598b88b9fa6cf90f6289b77/10924_2504_KaenicRookern.png')
    
    await ctx.send(embed=embed)  # Use await ctx.send instead of returning the embed

async def rukerno_kaenico_embed(ctx):
    titulo = "Descripción"
    descripcion = (
        "Al no recibir daño durante 12 segundos crearás un escudo contra daño mágico del 20% de tu vida"

    )
    eficiencia = "Eficiencia de oro\nTiene un costo de 2900G y una eficiencia de 102%"

    # Lista de campeones con sus nombres
    buenos_con = ["Sion", "Ornn", "K'Sante", "Shen", "Bardo", "Malphite"]
    buenos_contra = ["AP: Syndra", "Akali", "Vex", "Fizz", "Diana", ]

    # Enviar el embed con la información y la imagen combinada
    embed = discord.Embed(
        title=titulo,
        description=f"{descripcion}\n\n**{eficiencia}**",
        color=0x3498db  # Puedes cambiar el color según tus preferencias
    )

    # Añade un campo para los campeones "Bueno Con"
    embed.add_field(name="Bueno Con", value=", ".join(buenos_con), inline=False)
    embed.add_field(name="Bueno Contra", value=", ".join(buenos_contra), inline=False)

    # Establece una miniatura (thumbnail) en el embed
    embed.set_thumbnail(
        url='https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt90434f1c8fc3405d/6598b88b9fa6cf90f6289b77/10924_2504_KaenicRookern.png')
    
    await ctx.send(embed=embed)  # Use await ctx.send instead of returning the embed


def ejecutar_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Usuario: {bot.user} (ID: {bot.user.id})")

    # Dictionary to store item-related functions
    item_functions = {
        "corazon_de_hielo": corazon_de_hielo_embed,
        "rukerno_kaenico": rukerno_kaenico_embed
        # Add more items here

    }

    @bot.command(
        help="This is help",
        description="This is description",
        brief="This is brief",
        enabled=True,
        hidden=True
    )
    async def info(ctx, *, item: Optional[CommandConverter] = None):
        if item:
            # Check if the item is in the dictionary
            item_function = item_functions.get(item)
            if item_function:
                await item_function(ctx)  # Pass ctx as an argument
            else:
                await ctx.send(f"Comando desconocido: {item}")
        else:
            # If no item is provided, provide a list of available items
            available_items = ", ".join(item_functions.keys())
            await ctx.send("Uso incorrecto, uso correcto: !info (nombre del item)\n"
                           "Ejemplo: !info corazon de hielo")

    # Add more item-related functions here

    # Agrega tu token y ejecuta el bot
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    ejecutar_bot()
