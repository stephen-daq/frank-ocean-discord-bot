import asyncio
import json
from datetime import date, datetime, time, timedelta

import discord
import numpy as np
from discord.ext import commands

with open("key.json") as file:
    data = json.load(file)
    key = data["key"]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

WHEN = time(18,49,0)


async def daily_task():
    for guild in bot.guilds:
        channels = guild.voice_channels

        max_members = 0

        for c in channels:
            if len(c.members) > max_members:
                max_members = len(c.members)
                max_channel = c

        if not (max_members) == 0:
            member = max_channel.members[0]
            await play_message(member)


@bot.event
async def on_ready():
    await background_task()


async def play_message(member):
    channel = member.voice.channel
    vc = await channel.connect()
    audio = discord.FFmpegPCMAudio(source="./its 1049 pm.mp3")

    # Play audio and wait for it to finish
    vc.play(audio)

    # Wait while audio is playing
    while vc.is_playing():
        await asyncio.sleep(1)

    # Disconnect after audio finishes
    await vc.disconnect()


async def background_task():
    now = datetime.now()

    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(
            seconds
        )  # Sleep until tomorrow and then the loop will start

    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), WHEN)

        if now.time() > WHEN:
            target_time += timedelta(days=1)

        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await daily_task()

        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)


if __name__ == "__main__":
    bot.run(key)
