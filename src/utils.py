import datetime
import random
import re
from typing import List, Optional

import nextcord

import data.data as data

popular_words = data.pokemon_names
all_words = set(popular_words)
max_length = max(map(len, all_words))

EMOJI_CODES = {
    "green": {
        "a": "<:green_a:1076194995024957440>",
        "b": "<:green_b:1076195022828994690>",
        "c": "<:green_c:1076195073764634695>",
        "d": "<:green_d:1076195076193136790>",
        "e": "<:green_e:1076195077203964035>",
        "f": "<:green_f:1076195079234002995>",
        "g": "<:green_g:1076195080601358447>",
        "h": "<:green_h:1076195081620557874>",
        "i": "<:green_i:1076195083336040571>",
        "j": "<:green_j:1076195084908900542>",
        "k": "<:green_k:1076195189267370064>",
        "l": "<:green_l:1076195191305809961>",
        "m": "<:green_m:1076195193008701540>",
        "n": "<:green_n:1076195194178899978>",
        "o": "<:green_o:1076195196141834270>",
        "p": "<:green_p:1076195197366575256>",
        "q": "<:green_q:1076195199245627543>",
        "r": "<:green_r:1076195201674137681>",
        "s": "<:green_s:1076195227905310782>",
        "t": "<:green_t:1076195229067120661>",
        "u": "<:green_u:1076195231432724560>",
        "v": "<:green_v:1076195232581947472>",
        "w": "<:green_w:1076195234616193035>",
        "x": "<:green_x:1076195236767858788>",
        "y": "<:green_y:1076195237883547668>",
        "z": "<:green_z:1076195239737446501>",
        " ": "<:green_square:1076539072228634705>",
        "2": "<:green_2:1076547977667149926>"
    },
    "yellow": {
        "a": "<:yellow_a:1076195901221114027>",
        "b": "<:yellow_b:1076195902433267865>",
        "c": "<:yellow_c:1076195904454930502>",
        "d": "<:yellow_d:1076195905981648916>",
        "e": "<:yellow_e:1076195908124938280>",
        "f": "<:yellow_f:1076195909597147257>",
        "g": "<:yellow_g:1076195910800920658>",
        "h": "<:yellow_h:1076195912893866064>",
        "i": "<:yellow_i:1076195913854369944>",
        "j": "<:yellow_j:1076196172273828010>",
        "k": "<:yellow_k:1076195915423043695>",
        "l": "<:yellow_l:1076196174257729556>",
        "m": "<:yellow_m:1076196175239196765>",
        "n": "<:yellow_n:1076195919080476802>",
        "o": "<:yellow_o:1076196176870785095>",
        "p": "<:yellow_p:1076195922318475315>",
        "q": "<:yellow_q:1076196179018252318>",
        "r": "<:yellow_r:1076196180515631164>",
        "s": "<:yellow_s:1076196181580972032>",
        "t": "<:yellow_t:1076195926529548308>",
        "u": "<:yellow_u:1076196183216754699>",
        "v": "<:yellow_v:1076195929247457380>",
        "w": "<:yellow_w:1076196184307273728>",
        "x": "<:yellow_x:1076196255069384755>",
        "y": "<:yellow_y:1076196257376256051>",
        "z": "<:yellow_z:1076195933051682886>",
        " ": "<:yellow:square:1076539242311843990>",
        "2": "<:yellow_2:1076548185905954887>"
    },
    "gray": {
        "a": "<:gray_a:1076196441648795739>",
        "b": "<:gray_b:1076196444664512583>",
        "c": "<:gray_c:1076196446216396800>",
        "d": "<:gray_d:1076196447315304612>",
        "e": "<:gray_e:1076196449458589786>",
        "f": "<:gray_f:1076196450607837314>",
        "g": "<:gray_g:1076196452512043028>",
        "h": "<:gray_h:1076196453715820584>",
        "i": "<:gray_i:1076196454785364039>",
        "j": "<:gray_j:1076196480819404831>",
        "k": "<:gray_k:1076196481909923850>",
        "l": "<:gray_l:1076196483939967067>",
        "m": "<:gray_m:1076196485030490133>",
        "n": "<:gray_n:1076196486884380773>",
        "o": "<:gray_o:1076196488457240746>",
        "p": "<:gray_p:1076196489627439185>",
        "q": "<:gray_q:1076196491783319682>",
        "r": "<:gray_r:1076196493075165235>",
        "s": "<:gray_s:1076196515732803604>",
        "t": "<:gray_t:1076196517746065418>",
        "u": "<:gray_u:1076196518995972176>",
        "v": "<:gray_v:1076196521332191262>",
        "w": "<:gray_w:1076196523194458142>",
        "x": "<:gray_x:1076196524326924358>",
        "y": "<:gray_y:1076196525400674435>",
        "z": "<:gray_z:1076196527283904634>",
        " ": "<:gray_square:1076539159373676634>",
        "2": "<:gray_2:1076548331309891646>"
    },
}

def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:

    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray

    Args:
        word (str): The word to be colored
        answer (str): The answer to the word

    Returns:
        str: A string of emoji codes
    """
    guess_letters: List[Optional[str]] = list(guess)
    answer_letters: List[Optional[str]] = list(answer)

    guess_spaces_count = max_length - len(guess_letters)
    guess_spaces = [" "] * guess_spaces_count
    guess_letters = guess_letters + guess_spaces

    answer_spaces_count = max_length - len(answer_letters)
    answer_spaces = [" "] * answer_spaces_count
    answer_letters = answer_letters + answer_spaces

    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess_letters]

    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters

    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * max_length


def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user

    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID

    Returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses

    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user

    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word

    Args:
        word (str): The word to validate

    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID

    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)


def daily_puzzle_id() -> int:
    """
    Calculates the puzzle ID for the daily puzzle

    Returns:
        int: The puzzle ID for the daily puzzle
    """
    # calculate days since 1/1/2022 and mod by the number of puzzles
    num_words = len(popular_words)
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    return time_diff.days % num_words


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed

    Args:
        embed (nextcord.Embed): The embed to check

    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


def generate_info_embed() -> nextcord.Embed:
    """
    Generates an embed with information about the bot

    Returns:
        nextcord.Embed: The embed to be sent
    """
    join_url = "https://discord.com/api/oauth2/authorize?client_id=938502854921027584&permissions=11264&scope=bot%20applications.commands"
    discord_url = "https://discord.gg/fPrdqh3Zfu"
    youtube_url = "https://www.youtube.com/watch?v=0p_eQGKFY3I"
    github_url = "https://github.com/DenverCoder1/discord-wordle-clone"
    return nextcord.Embed(
        title="About Discord Wordle Clone",
        description=(
            "Discord Wordle Clone is a game of wordle-like puzzle solving.\n\n"
            "**You can start a game with**\n\n"
            ":sunny: `/play daily` - Play the puzzle of the day\n"
            ":game_die: `/play random` - Play a random puzzle\n"
            ":boxing_glove: `/play id <puzzle_id>` - Play a puzzle by ID\n\n"
            f"<:member_join:942985122846752798> [Add this bot to your server]({join_url})\n"
            f"<:discord:942984508586725417> [Join my Discord server]({discord_url})\n"
            f"<:youtube:942984508976795669> [YouTube tutorial on the making of this bot]({youtube_url})\n"
            f"<:github:942984509673066568> [View the source code on GitHub]({github_url})\n"
        ),
    )


async def process_message_as_guess(bot: nextcord.Client, message: nextcord.Message) -> bool:
    """
    Check if a new message is a reply to a Wordle game.
    If so, validate the guess and update the bot's message.

    Args:
        bot (nextcord.Client): The bot
        message (nextcord.Message): The new message to process

    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "Start a new game with /play"
        if embed.author:
            reply = f"This game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply("The game is already over. Start a new game with /play", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # strip mentions from the guess
    guess = re.sub(r"<@!?\d+>", "", guess).strip()

    bot_name = message.guild.me.nick if message.guild and message.guild.me.nick else bot.user.name

    if len(guess) == 0:
        await message.reply(
            "I am unable to see what you are trying to guess.\n"
            "Please try mentioning me in your reply before the word you want to guess.\n\n"
            f"**For example:**\n{bot.user.mention} crate\n\n"
            f"To bypass this restriction, you can start a game with `@\u200b{bot_name} play` instead of `/play`",
            delete_after=14,
        )
        try:
            await message.delete(delay=14)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(guess.split()) > 1:
        await message.reply("Please respond with a single 5-letter word.", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True
