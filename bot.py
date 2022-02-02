import os
from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

from utils import (
    generate_puzzle_embed,
    is_game_over,
    is_valid_word,
    update_embed,
    random_puzzle_id,
)

load_dotenv()

bot = commands.Bot(command_prefix=[])

GUILD_IDS = (
    [int(guild_id) for guild_id in os.getenv("GUILD_IDS").split(",")]
    if os.getenv("GUILD_IDS", None)
    else nextcord.utils.MISSING
)


@bot.slash_command(description="Play a game of wordle", guild_ids=GUILD_IDS)
async def play(interaction: nextcord.Interaction):
    # generate a puzzle
    puzzle_id = random_puzzle_id()
    # create the puzzle to display
    embed = generate_puzzle_embed(interaction.user, puzzle_id)
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@bot.event
async def on_message(message: nextcord.Message):
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return

    # check that the message has embeds
    if not parent.embeds:
        return

    embed = parent.embeds[0]

    # check that the user is the one playing
    if embed.author.name != message.author.name:
        await message.reply(
            f"This game was started by {embed.author.name}. Start a new game with /play",
            delete_after=5,
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    # check that the game is not over
    if is_game_over(embed):
        await message.reply(
            "The game is already over. Start a new game with /play", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    # check that a single word is in the message
    if len(message.content.split()) > 1:
        await message.reply(
            "Please respond with a single 5-letter word.", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    # check that the word is valid
    if not is_valid_word(message.content):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

    # update the embed
    embed = update_embed(embed, message.content)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass


bot.run(os.getenv("TOKEN"))
