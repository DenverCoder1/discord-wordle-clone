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


@bot.slash_command(description="Play a game of Wordle Clone", guild_ids=GUILD_IDS)
async def play(
    interaction: nextcord.Interaction,
    puzzle_id: int = nextcord.SlashOption(
        description="Puzzle ID, leave out for a random puzzle", required=False
    ),
):
    # generate a puzzle
    puzzle_id = puzzle_id or random_puzzle_id()
    # create the puzzle to display
    embed = generate_puzzle_embed(interaction.user, puzzle_id)
    # send the puzzle as an interaction response
    await interaction.send(embed=embed)


@bot.slash_command(description="Info about Discord Wordle Clone", guild_ids=GUILD_IDS)
async def info(interaction: nextcord.Interaction):
    join_url = "https://discord.com/api/oauth2/authorize?client_id=938502854921027584&permissions=11264&scope=bot%20applications.commands"
    discord_url = "https://discord.gg/fPrdqh3Zfu"
    youtube_url = "https://www.youtube.com/c/DevProTips"
    github_url = "https://github.com/DenverCoder1/discord-wordle-clone"
    embed = nextcord.Embed(
        title="About Discord Wordle Clone",
        description=(
            "Discord Wordle Clone is a game of wordle-like puzzle solving.\n"
            "You can play it by typing `/play` or `/play <puzzle_id>`\n"
            "You can also play a random puzzle by leaving out the puzzle ID.\n\n",
            f"<:bot_tag:596576775555776522> [Add this bot to your server]({join_url})\n",
            f"<:discord:891394837507604521> [Join my Discord Server]({discord_url})\n",
            f"<:youtube:891394512197410856> [YouTube tutorial on the making of this bot]({youtube_url})\n",
            f"<:github:819659738354417734> [View the source code on GitHub]({github_url})\n",
        ),
    )
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
