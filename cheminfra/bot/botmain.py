import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from cheminfra.configuration import load_default_configuration
from cheminfra.db.base import Base
from cheminfra.db.bot_commands import BotCommand
from cheminfra.deployment import Deployment
from structlog import get_logger

config = load_default_configuration()
engine = create_engine(config.database.url, echo=config.database.echo)
Base.metadata.create_all(engine)
deployment = Deployment(config.deployment.core_dir)
logger = get_logger()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
)


@bot.event
async def on_ready():
    logger.info("We have logged in", username=bot.user.name)


@bot.command()
async def echo(ctx):
    with Session(engine) as session:
        session.add(BotCommand(command=ctx.message.content, user=ctx.author.name))
        session.commit()
    await ctx.send(ctx.message.content)


@bot.command()
async def restart(ctx):
    logger.info("restarting", user=ctx.author)
    with Session(engine) as session:
        session.add(BotCommand(command=ctx.message.content, user=ctx.author.name))
        session.commit()
    await ctx.send("Restarting...")
    try:
        deployment.restart()
    except Exception as e:
        logger.error("error restarting", error=str(e))
        await ctx.send("Error restarting: " + str(e))
        return
    await ctx.send("Finished restarting")


def run_bot():
    bot.run(config.discord.token)
