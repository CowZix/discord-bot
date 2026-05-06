import logging
import os

from dotenv import load_dotenv

from discord_bot.bot import DiscordBot
from discord_bot.utils.formatting import LoggingFormatter

load_dotenv()

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def main():
    bot = DiscordBot(logger=logger)
    bot.run(str(os.getenv("TOKEN")))
