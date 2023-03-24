""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import platform
import random

import aiohttp
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
import openai
import json
from sqlitedict import SqliteDict
import os

class Ai(commands.Cog, name="ai"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="persona",
        description="Changes the Chatbot Persona."
    )
    async def persona(self, context: Context, prompt: str):
        if len(prompt) > 50:
            response = "Prompt was too long"
        else:
            self.bot.persona_db[int(context.guild.id)] = prompt
            response = f"The persona is now: \"{prompt}\""

        embed = discord.Embed(
            description = response,
            color=0x9C84EF
        )
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ai(bot))