import discord
from discord.ext import commands
from cheminfra.configuration import load_default_configuration

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")


@bot.command()
async def restart(ctx):
    ctx.send("Restarting...")


def run_bot():
    config = load_default_configuration()
    bot.run(config.discord.token)
