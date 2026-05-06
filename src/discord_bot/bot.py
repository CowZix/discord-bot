import os
import platform
import random
import sys
from pathlib import Path

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

from discord_bot.database.database_manager import DatabaseManager

load_dotenv()

intents = discord.Intents.all()


class DiscordBot(commands.Bot):
    def __init__(self, logger) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(str(os.getenv("PREFIX"))),
            intents=intents,
            help_command=None,
        )
        self.logger = logger
        self.database = None
        self.bot_prefix = os.getenv("PREFIX")
        self.invite_link = os.getenv("INVITE_LINK")

    async def init_db(self) -> None:
        async with aiosqlite.connect(
            Path(__file__).resolve().parent / "database" / "database.db"
        ) as db:
            with Path.open(
                Path(__file__).resolve().parent / "database" / "schema.sql",
                encoding="utf-8",
            ) as file:
                await db.executescript(file.read())
            await db.commit()

    from pathlib import Path

    async def load_cogs(self) -> None:
        root = Path(__file__).resolve().parent
        cogs_path = root / "cogs"

        # Ensure root is in sys.path
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

        for file in cogs_path.glob("*.py"):
            if file.name == "__init__.py":
                continue

            module = f"cogs.{file.stem}"

            try:
                await self.load_extension(module)
                self.logger.info("Loaded extension '%s'", file.stem)
            except Exception as e:
                self.logger.exception(
                    "Failed to load extension %s (%s: %s)",
                    file.stem,
                    type(e).__name__,
                    e,
                )

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        statuses = ["Zeep!", "Zorp!", "Vorp!", "Gleep!"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info(f"Prefix: {self.bot_prefix}")
        self.logger.info("-------------------")
        await self.init_db()
        await self.load_cogs()
        self.status_task.start()
        self.database = DatabaseManager(
            connection=await aiosqlite.connect(
                Path(__file__).resolve().parent / "database" / "database.db"
            )
        )

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="You are not the owner of the bot!", color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error
