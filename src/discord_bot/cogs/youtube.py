import re
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import Context
from googleapiclient.discovery import build


youtube = build("youtube", "v3", developerKey=str(os.getenv("YOUTUBE")))

class General(commands.Cog, name="youtube"):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user or message.author.bot:
            return
        match = re.search(r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?", message.content, re.IGNORECASE)
        if match:
            link = match.group(1)
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=link,
                maxResults=100,
                textFormat="plainText"
            ).execute()
            
            item = random.choice(response["items"])
            snippet = item["snippet"]["topLevelComment"]["snippet"]

            username = snippet["authorDisplayName"]
            profile_pic = snippet["authorProfileImageUrl"]
            comment = snippet["textDisplay"]

            embed = discord.Embed(title="", description=comment)
            embed.set_author(
                name=username,
                icon_url=profile_pic,
            )

            await message.reply(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(General(bot))