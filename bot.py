import logging
import os
from typing import Optional

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

from utils import (
    daily_puzzle_id,
    generate_info_embed,
    generate_puzzle_embed,
    process_message_as_guess,
    random_puzzle_id,
)

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


@bot.slash_command(name="play", description="Play Wordle Clone", guild_ids=GUILD_IDS)
async def play_slash(interaction: nextcord.Interaction):
    """This command has subcommands for playing a game of Wordle Clone."""
    pass


@play_slash.subcommand(name="random", description="Play a random game of Wordle Clone")
async def play_slash_random(interaction: nextcord.Interaction):
    # generate puzzle embed
    embed = generate_puzzle_embed(interaction.user, random_puzzle_id())
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@play_slash.subcommand(name="id", description="Play a game of Wordle Clone by its ID")
async def play_slash_id(
    interaction: nextcord.Interaction,
    puzzle_id: int = nextcord.SlashOption(description="Puzzle ID of the word to guess"),
):
    # generate puzzle embed
    embed = generate_puzzle_embed(interaction.user, puzzle_id)
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@play_slash.subcommand(name="daily", description="Play the daily game of Wordle Clone")
async def play_slash_id(interaction: nextcord.Interaction):
    # generate puzzle embed
    embed = generate_puzzle_embed(interaction.user, daily_puzzle_id())
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@bot.slash_command(description="Info about Discord Wordle Clone", guild_ids=GUILD_IDS)
async def info_slash(interaction: nextcord.Interaction):
    await interaction.send(embed=generate_info_embed())


@bot.group(invoke_without_command=True)
async def play(ctx: commands.Context, puzzle_id: Optional[int] = None):
    """Play a game of Wordle Clone"""
    embed = generate_puzzle_embed(ctx.author, puzzle_id or random_puzzle_id())
    await ctx.reply(embed=embed, mention_author=False)


@play.command(name="random", description="Play a random game of Wordle Clone")
async def play_random(ctx: commands.Context):
    embed = generate_puzzle_embed(ctx.author, random_puzzle_id())
    await ctx.reply(embed=embed, mention_author=False)


@play.command(name="id", description="Play a game of Wordle Clone by its ID")
async def play_id(ctx: commands.Context, puzzle_id: int):
    embed = generate_puzzle_embed(ctx.author, puzzle_id)
    await ctx.reply(embed=embed, mention_author=False)


@play.command(name="daily", description="Play the daily game of Wordle Clone")
async def play_daily(ctx: commands.Context):
    embed = generate_puzzle_embed(ctx.author, daily_puzzle_id())
    await ctx.reply(embed=embed, mention_author=False)


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
