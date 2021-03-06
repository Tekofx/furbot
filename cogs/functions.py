# Contains all functions that are not commands
import discord
from PIL import Image
import os
from discord.raw_models import RawReactionClearEvent
import logging
from dotenv import load_dotenv
import praw
import random
from discord.ext import commands
import requests


# .env data

load_dotenv()

# Users
creator_id = int(os.getenv("BOT_CREATOR"))
cracker_id = int(os.getenv("CRACKER"))
magnet_id = int(os.getenv("MAGNET"))
angel_id = int(os.getenv("ANGEL"))
zaffy_id = int(os.getenv("ZAFFY"))

# Channels
general_channel = int(os.getenv("GENERAL_CHANNEL"))
tests_channel = int(os.getenv("TESTS_CHANNEL"))

separator = "       "  # key word to distinguish separator roles

admin = [magnet_id, creator_id, zaffy_id]

# Create bot
prefixes = ["fur ", "Fur ", "FUR "]
bot = commands.Bot(command_prefix=prefixes, owner_id=int(creator_id))

# Paths
work_directory = "/home/teko/bots/furbot/"
stickers_path = "stickers/"
meme_templates_path = "resources/memes/"
meme_path = "memes/"
enanas_path = "fun/enanas/"

# Data files
help_txt = "resources/help.txt"
insults_txt = "resources/insults.txt"
cumpleaños_txt = "resources/cumpleaños.txt"
reddit_memes_history_txt = "resources/reddit_memes_history.txt"
animos_txt = "resources/animos.txt"
memes_history_txt = "resources/memes_history.txt"
activity_txt = "resources/activity.txt"
jojos_txt = "resources/jojos.txt"
species_txt = "resources/species.txt"
colors_txt = "resources/colors.txt"
ranks_txt = "resources/ranks.txt"

stickerSize = 500

# Creation of reddit
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


def setup_logs():
    """Set up the logs"""
    logging.basicConfig(
        filename="logs",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    logging.info("\n\n\nStarted furbot")


def get_user_avatar(url: str, name: str):
    """Downloads the avatar of a user

    Args:
        user (discord.Member): user to download avatar from
        name (str): user to download avatar from
    """

    r = requests.get(url, allow_redirects=True)

    open(meme_templates_path + name, "wb").write(r.content)

    logging.info("Saved avatar with url " + url + " in " + meme_templates_path)


def convert_pic(picture: str, imgName: str, imgSize: str = None):
    """Converts an image to PNG with a differents size

    Args:
        picture (str): picture to convert
        imgName (str): exported picture name
        imgSize (str): exported image size
    """
    img = Image.open(picture)

    if imgSize is not None:
        wpercent = imgSize / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((imgSize, hsize), Image.ANTIALIAS)

    img.save(meme_templates_path + imgName + ".png")


def get_user(context, user: discord.Member = None):
    """Gets user from a message

    Args:
        context (Message): Message to get an avatar
        user (discord.Member, optional): User of a message. Defaults to None.

    Returns:
        discord.Member: user
    """
    if user is None:
        output = context.author
    else:
        output = user

    return output


def is_admin(context):
    """Checks if user that calls a function is a bot admin

    Args:
        context (discord.ext.commands.context.Context): context of the function

    Returns:
        bool: true if is owner, false if not
    """
    if context.author.id in admin:
        return True
    return False


def create_meme(
    pictures: list, avatar_url: str, avatar_size: int, position: list, invert: bool
):
    """Crea un meme

    Args:
        pictures (list): lista de imagenes, siendo pictures[0] el meme y el resto avatares
        avatar_url (str): url del avatar a añadir al meme
        avatar_size (int): tamañao al que convertir el avatar de webp a png
        position (list): posiciones en las que colocar las imagenes, siendo position[0] y position[1] la x,y del meme
        invert (bool): Si es True usa el meme como canvas, en caso contrario, usa el avatar
    """

    r = requests.get(avatar_url, allow_redirects=True)
    open(meme_templates_path + "01.webp", "wb").write(r.content)

    # Convert avatar
    convert_pic(meme_templates_path + "01.webp", "01", avatar_size)

    if not invert:  # burn
        canvas = pictures[1]
        width, height = (
            Image.open(meme_templates_path + canvas + ".png").convert("RGBA").size
        )
    else:  # cringe
        canvas = pictures[0]
        width, height = (
            Image.open(meme_templates_path + canvas + ".png").convert("RGBA").size
        )

    output = Image.new("RGBA", (width, height))  # Create picture
    meme = Image.open(meme_templates_path + pictures[0] + ".png").convert(
        "RGBA"
    )  # Open meme picture

    # Add avatar pictures
    i = 2
    for x in pictures[1:]:
        img = Image.open(meme_templates_path + x + ".png").convert("RGBA")
        output.paste(img, (position[i], position[i + 1]), img)
        i += 2

    # Add meme picture
    output.paste(meme, (position[0], position[1]), meme)

    # Save final meme
    output.save(meme_templates_path + "output.png", "PNG")


############################# Carnet functions ##############################
def get_user_ranks(user: discord.Member):
    """Get ranks from a user

    Args:
        user (discord.Member): user to search for roles

    Returns:
        str: String containing all ranks
    """
    output = []
    for role in user.roles:
        if exists_string_in_file(ranks_txt, str(role.name)):
            output.append(role.name)
    if output:
        b = ", ".join(output)
    else:
        return "Admin"
    return str(b)


def get_user_roles(user: discord.Member):
    """Get user roles that are not ranks

    Args:
        user (discord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    mention = []
    for role in user.roles:
        if (
            role.name != "@everyone"
            and not exists_string_in_file(ranks_txt, str(role.name))
            and separator not in str(role)
        ):
            mention.append(role.name)

    b = ", ".join(mention)
    return str(b)


def get_user_species(user: discord.Member):
    """Get user roles that are species

    Args:
        user (discord.Member): user to search for roles

    Returns:
        str: String containing roles
    """
    mention = []
    for role in user.roles:
        if exists_string_in_file(species_txt, str(role.name)):
            mention.append(role.name)

    b = ", ".join(mention)
    return b


def get_user_color(user: discord.Member):
    """Get user role that is a color

    Args:
        user (discord.Member): user to search for color

    Returns:
        str: String with color
    """
    output = "blanco"
    for role in user.roles:
        if exists_string_in_file(colors_txt, str(role.name)):
            output = role.name
            break

    return str(output)


def get_color_code(color: str):
    """Gets the color code of a given color

    Args:
        color (str): color to search color_code

    Returns:
        list(int): contains values of RGB
    """
    with open(colors_txt) as f:
        for line in f:
            if color in line:
                output = f.readline()

                # Transform into a list
                output = output.split(" ")

                # Delete \n from last element
                output = [s.replace("\n", "") for s in output]

                # Convert all elements into int
                output = list(map(int, output))
                return output


############################### Reddit functions ###############################
def get_reddit_image(Subreddit: str, Flair: str, Filter: str):
    """Gets a random Reddit image

    Args:
        Subreddit (str): subreddit to get the photo from
        Flair (str): flair to filter by
        Filter (str): filter to search by

    Returns:
        str: url from a reddit image
    """
    try:
        var = True
        while var:
            if Flair is None:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    Filter
                )  # Gets a random images from r/foxes with flair Pics!
            else:
                memes_submissions = reddit.subreddit(Subreddit).search(
                    "Flair:" + Flair
                )  # Gets a random images from r/foxes with flair Pics!
            post_to_pick = random.randint(1, 10)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            if submission.url.endswith("jpg"):
                var = False
    except ConnectionError:
        logging.error("Error at getting images from reddit")

    return submission.url


def get_hot_subreddit_image(Subreddit: str, Limit: int):
    """Get an image from a subreddit in hot

    Args:
        Subreddit (str): Subreddit to search for
        Limit (int): Limit to search in subreddit

    Returns:
        str: link to image
    """
    output = random.choice([x for x in reddit.subreddit(Subreddit).hot(limit=Limit)])
    try:
        while exists_string_in_file(reddit_memes_history_txt, output.url):
            output = random.choice(
                [x for x in reddit.subreddit(Subreddit).hot(limit=Limit)]
            )

        write_in_file(reddit_memes_history_txt, output.url + "\n")

        return output.url
    except FileNotFoundError:
        logging.error("Error at getting reddit_memes_history.txt")


############################### Files functions ###############################
def exists_string_in_file(file_name: str, string: str):
    """Checks if string is contained as line in file_name

    Args:
        file_name (str]): file to check
        string (str): string to search

    Returns:
        bool: True if string is in file_name, False if not
    """
    with open(file_name, "r") as file:
        for line in file:
            if string in line:
                return True
    return False


def count_lines_in_file(file: str):
    """Counts lines of a file

    Args:
        file (str): file to count lines from

    Returns:
        int: number of lines
    """
    output = 0
    with open(file, "r") as f:
        for line in f:
            output += 1
    return output


def count_files_in_dir(directory: str):
    """Counts files in a directory

    Args:
        directory (str): directory to count files from

    Returns:
        int: number of files in directory
    """
    files = os.listdir(directory)  # dir is your directory path
    output = len(files)
    return output


def exists_file(file: str, directory: str):
    """Checks if exists a file with a given name

    Args:
        file (str): name of the file
        directory (str): folder to search for file

    Returns:
        [Bool]: true if exists, false if not
    """
    output = False
    files = os.listdir(directory)
    if file in files:
        output = True
    return output


def exists_substring_in_file(substring: str, directory: str):
    output = False
    files = os.listdir(directory)
    for file in files:
        if substring in file:
            output = True
    return output


def get_files_in_directory(directory: str):
    """Get a list of files in a directory

    Args:
        directory (str): directory to search

    Returns:
        [list]: list of files in dir
    """
    return os.listdir(directory)


def get_files_in_directory_with_substring(substring: str, directory: str):
    """Get a list of files in a directory that contain a substring

    Args:
        directory (str): directory to search

    Returns:
        [files]: list of files in dir
    """
    output = ""
    files = os.listdir(directory)
    for file in files:
        if substring in file:
            output += str(file[:-4]) + ", "
    output = output[:-2]
    return output


def write_in_file(file: str, string: str):
    """Writes text in a file

    Args:
        file (str): file to write
        string (str): string to write
    """
    f = open(file, "a")
    f.write(string)
    f.close()


def delete_content_in_file(file: str):
    """Deletes contents of a file

    Args:
        file (str): File to delete contents
    """
    open(file, "w").close()


def get_random_line_of_file(file: str):
    """Gets random line of a file

    Args:
        file (str): file to get the line

    Returns:
        [str]: random line
    """
    with open(file) as f:
        lines = f.readlines()
    f.close()

    return random.choice(lines)


def delete_files(elements: list):
    """Delete files needed to create a meme

    Args:
        elements (list): files used in a meme
    """
    for x in elements:
        if os.path.isfile(meme_templates_path + x):
            os.remove(meme_templates_path + x)
    logging.info("Removed dependencies")
