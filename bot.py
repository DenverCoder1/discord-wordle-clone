import logging
import os
from typing import Optional

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

from utils import generate_info_embed, generate_puzzle_embed, process_message_as_guess

logging.basicConfig(level=logging.INFO)

load_dotenv()

activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="/play")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("w?"), activity=activity)

GUILD_IDS = (
    [int(guild_id) for guild_id in os.getenv("GUILD_IDS").split(",")]
    if os.getenv("GUILD_IDS", None)
    else nextcord.utils.MISSING
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(description="Play a game of Wordle Clone", guild_ids=GUILD_IDS)
async def play(
    interaction: nextcord.Interaction,
    puzzle_id: int = nextcord.SlashOption(
        description="Puzzle ID, leave out for a random puzzle", required=False
    ),
):
    # generate puzzle embed
    embed = generate_puzzle_embed(interaction.user, puzzle_id)
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@bot.command()
async def play(ctx: commands.Context, puzzle_id: Optional[int] = None):
    """Play a game of Wordle Clone"""
    embed = generate_puzzle_embed(ctx.author, puzzle_id)
    await ctx.reply(embed=embed, mention_author=False)


@bot.slash_command(description="Info about Discord Wordle Clone", guild_ids=GUILD_IDS)
async def info(interaction: nextcord.Interaction):
    await interaction.send(embed=generate_info_embed())


@bot.command()
async def info(ctx: commands.Context):
    """Info about Discord Wordle Clone"""
    await ctx.reply(embed=generate_info_embed(), mention_author=False)


@bot.event
async def on_message(message: nextcord.Message):
    """
    When a message is sent, process it as a guess.
    Then, process any commands in the message if it's not a guess.
    """
    processed_as_guess = await process_message_as_guess(bot, message)
    if not processed_as_guess:
        await bot.process_commands(message)


bot.run(os.getenv("TOKEN"))
