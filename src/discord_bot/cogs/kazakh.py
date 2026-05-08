import re
import random
import discord
from discord.ext import commands
from discord.ext.commands import Context
from googleapiclient.discovery import build

image_list = ["https://tenor.com/lZsVEYpuQXR.gif","https://tenor.com/jxSg0ZIFplh.gif", "https://tenor.com/vZTxhA4LYEp.gif","https://tenor.com/ieshMd3Uzvg.gif"]

class General(commands.Cog, name="kazakh"):
    def __init__(self, bot) -> None:
        self.bot = bot
    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user or message.author.bot:
            return
        if bool(re.search(r"\bkazakh\w*", message.content, re.IGNORECASE)):
            await message.add_reaction("🇰🇿")
            if random.random() < 0.2:
                await message.reply(
                    random.choice(image_list)
                )


async def setup(bot) -> None:
    await bot.add_cog(General(bot))