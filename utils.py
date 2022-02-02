import random
import nextcord

popular_words = open("dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("dict-sowpods.txt"))

EMOJI_CODES = {
    "green": {
        "a": "<:1f1e6:938280353527906325>",
        "b": "<:1f1e7:938280353515315242>",
        "c": "<:1f1e8:938280353850875928>",
        "d": "<:1f1e9:938280353657929799>",
        "e": "<:1f1ea:938280354064785478>",
        "f": "<:1f1eb:938280353838276609>",
        "g": "<:1f1ec:938280353968291860>",
        "h": "<:1f1ed:938280353871839232>",
        "i": "<:1f1ee:938280354010239016>",
        "j": "<:1f1ef:938280353876021328>",
        "k": "<:1f1f0:938280354148675614>",
        "l": "<:1f1f1:938280353611780107>",
        "m": "<:1f1f2:938280353783775244>",
        "n": "<:1f1f3:938280353670504489>",
        "o": "<:1f1f4:938280354018656316>",
        "p": "<:1f1f5:938280353884414012>",
        "q": "<:1f1f6:938280354253537321>",
        "r": "<:1f1f7:938280354022850561>",
        "s": "<:1f1f8:938280354089947146>",
        "t": "<:1f1f9:938280353691476010>",
        "u": "<:1f1fa:938280353968304138>",
        "v": "<:1f1fb:938280353976696882>",
        "w": "<:1f1fc:938280353502752850>",
        "x": "<:1f1fd:938280354043789382>",
        "y": "<:1f1fe:938280840796995638>",
        "z": "<:1f1ff:938280841199616000>",
    },
    "yellow": {
        "a": "<:1f1e6:938280773906227230>",
        "b": "<:1f1e7:938280773910409256>",
        "c": "<:1f1e8:938280774057197639>",
        "d": "<:1f1e9:938280773918806066>",
        "e": "<:1f1ea:938280776057905152>",
        "f": "<:1f1eb:938280773977505832>",
        "g": "<:1f1ec:938280774006878208>",
        "h": "<:1f1ed:938280773910429726>",
        "i": "<:1f1ee:938280773998481418>",
        "j": "<:1f1ef:938280773910397028>",
        "k": "<:1f1f0:938280774120132628>",
        "l": "<:1f1f1:938280774011080715>",
        "m": "<:1f1f2:938280773922992138>",
        "n": "<:1f1f3:938280774002688010>",
        "o": "<:1f1f4:938280774065610822>",
        "p": "<:1f1f5:938280774019465286>",
        "q": "<:1f1f6:938280773881057392>",
        "r": "<:1f1f7:938280773994303568>",
        "s": "<:1f1f8:938280774191415357>",
        "t": "<:1f1f9:938280774023647233>",
        "u": "<:1f1fa:938280774002679858>",
        "v": "<:1f1fb:938280773910396979>",
        "w": "<:1f1fc:938280774006898749>",
        "x": "<:1f1fd:938280774065618984>",
        "y": "<:1f1fe:938280774115934228>",
        "z": "<:1f1ff:938280774145310801>",
    },
    "gray": {
        "a": "<:1f1e6:938280277627785347>",
        "b": "<:1f1e7:938280277703278593>",
        "c": "<:1f1e8:938280277988503633>",
        "d": "<:1f1e9:938280278026231858>",
        "e": "<:1f1ea:938280278038818926>",
        "f": "<:1f1eb:938280277862658059>",
        "g": "<:1f1ec:938280278051405844>",
        "h": "<:1f1ed:938280278126891058>",
        "i": "<:1f1ee:938280277980119120>",
        "j": "<:1f1ef:938280277988507649>",
        "k": "<:1f1f0:938280277900394537>",
        "l": "<:1f1f1:938280277862674503>",
        "m": "<:1f1f2:938280277678100501>",
        "n": "<:1f1f3:938280277866860555>",
        "o": "<:1f1f4:938280278189801502>",
        "p": "<:1f1f5:938280278017867776>",
        "q": "<:1f1f6:938280278097530941>",
        "r": "<:1f1f7:938280278038806538>",
        "s": "<:1f1f8:938280278110138468>",
        "t": "<:1f1f9:938280278055583764>",
        "u": "<:1f1fa:938280278043004958>",
        "v": "<:1f1fb:938280278051418153>",
        "w": "<:1f1fc:938280278131085332>",
        "x": "<:1f1fd:938280278105944074>",
        "y": "<:1f1fe:938280278177218560>",
        "z": "<:1f1ff:938280278215000064>",
    },
}


def generate_blanks() -> str:
    """Return a string of 5 blank emoji characters"""
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def is_valid_word(word: str) -> bool:
    """check if this is a valid word"""
    return word.lower() in all_words


def random_puzzle_id() -> int:
    return random.randint(0, len(popular_words) - 1)


def generate_colored_word(guess: str, answer: str) -> str:
    """Return a string of emojis with the letters colored"""
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
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


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
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


def is_game_over(embed: nextcord.Embed) -> bool:
    return "\n\n" in embed.description
