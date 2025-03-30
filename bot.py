import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Clase para colores en la consola
class ConsoleColors:
    SUCCESS = '\033[92m'  # Verde
    WARNING = '\033[93m'  # Amarillo
    FAIL = '\033[91m'     # Rojo
    ENDC = '\033[0m'      # Restablecer el color

# Cargar configuraciones desde las variables de entorno
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX")

# Verificar que las configuraciones sean válidas
if not BOT_TOKEN or not BOT_PREFIX:
    print(f"{ConsoleColors.FAIL}Error: Configuration variables didn't load correctly.{ConsoleColors.ENDC}")
    exit(1)
    
    
# Configurar el bot con los intents necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

# Evento: Bot está listo
@bot.event
async def on_ready():
    print(f"--> {bot.user} is online.")
    await load_cogs(bot)  # Cargar los Cogs
    await sync_commands(bot)  # Sincronizar comandos de barra.
    # Configurar la actividad del bot
    activity = discord.Activity(type=discord.ActivityType.watching, name="✨ 5.0/5.0")
    await bot.change_presence(activity=activity)

# Cargar las Cogs
async def load_cogs(bot):
    base_path = './bot/Cogs'  # Directorio base donde están las cogs
    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if filename.endswith('.py'):  # Solo cargar archivos .py
                # Comprobar si el archivo está en una subcarpeta o en la raíz
                if dirpath == base_path:
                    cog = f"bot.Cogs.{filename[:-3]}"  # Cog en la raíz de Cogs
                else:
                    # Convertir la ruta en un formato válido para el importador de Cogs
                    relative_path = dirpath.replace(base_path, '').replace(os.sep, '.')[1:]
                    cog = f"bot.Cogs.{relative_path}.{filename[:-3]}"  # Cog dentro de una subcarpeta

                try:
                    await bot.load_extension(cog)
                    print(f"{ConsoleColors.SUCCESS}Cog '{cog}' loaded successfully.{ConsoleColors.ENDC}")
                except commands.ExtensionAlreadyLoaded:
                    print(f"{ConsoleColors.WARNING}Cog '{cog}' was already loaded.{ConsoleColors.ENDC}")
                except Exception as e:
                    print(f"{ConsoleColors.FAIL}Error loading the cog '{cog}': {e}{ConsoleColors.ENDC}")


# Sincronizar los comandos de barra (slash commands)
async def sync_commands(bot):
    try:
        await bot.tree.sync()
        print(f"--> Slash commands synced successfully.")
    except Exception as e:
        print(f"{ConsoleColors.FAIL}Error syncing slash commands: {e}{ConsoleColors.ENDC}")


# Manejo de errores de comandos
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist. Use `/help` to see the list of commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("It seems you missed a required argument. Please check the command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("One of the provided arguments is invalid.")
    else:
        print(f"{ConsoleColors.FAIL}Unexpected error: {error}{ConsoleColors.ENDC}")
        message = await ctx.send("An unexpected error occurred. Please try again later.")    
        # Borrar el mensaje después de 5 segundos
        await message.delete(delay=5)

# Iniciar el bot
if __name__ == "__main__":
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"{ConsoleColors.FAIL}Error starting the bot: {e}{ConsoleColors.ENDC}")
