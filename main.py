# Add logging and appropriate outputs

from hexbot import HexBot  # Gradients and pixel manipulation class
from youtube import YouTubeApi
from search import Search
from misc import Misc

from secret import Secrets  # Used to get Discord API key
import discord  # Used to easily interact with discord API
import os  # Used to get path of execution

# Gets current directory
d = os.path.abspath(os.path.dirname(__file__))

# Gets Discord API key, sets discord client
getSecret = Secrets()
TOKEN = getSecret.discord()
client = discord.Client()

# Classes for events
hb = HexBot()
sp = Misc()
yt = YouTubeApi()
sh = Search()


# Used to concatenate a string together using commas
async def hexbot_multi_value_split(msg_list):
    values = ''
    for i in range(len(msg_list) - 2):
        values += msg_list[i+2].lstrip('#') + ','
        if i == 24:  # Limit to the amount of colours used
            break
    return values[:-1]


# Used for requesting multiple values for a sort type, saves and returns file names and folder directory
async def hexbot_multi_value_save(msg_list, gradient_type, sort_type):
    values = await hexbot_multi_value_split(msg_list)
    images = hb.gradient(values, sort_type)
    folder_dir = d + '\\gradients\\%s\\' % gradient_type
    return images, folder_dir


@client.event
async def on_message(message):
    # Splits the list by spaces, and gets the first word used with the message
    msg_list = message.content.split(' ')
    command = str(msg_list[0]).upper().replace('\'', '').replace('\'', '')

    # If the author of the message is the bot, don't do anything
    if message.author == client.user:
        return

    # When a user says !hello in chat, it responds to the user saying hello, as well as @ their username
    elif command == '!HELLO':
        await message.channel.send('Hello {0}'.format(message.author.mention))

    # Gets the syntax to use for the gradient bot
    elif command == '!HELP':
        await message.channel.send('Need to do')  # TODO

    # Gets the syntax to use for the gradient bot
    elif command == 'G!HELP':
        await message.channel.send('Need to do')  # TODO

    elif command == 'G!2' or command == 'G!GLITCH' or command == 'G!NGLITCH' or command == 'G!DEBUG':
        # Try and see if they successfully convert to int, if not it is not into so throw error to user
        try:
            # Try to convert the first two values to integer
            w = int(msg_list[1])
            h = int(msg_list[2])
        except ValueError:
            # Respond to the user with below text
            await message.channel.send('Invalid width or height.')
            return

        # If the width or height is above 250 pixels wide, respond with error
        if w > 250 or h > 250:
            await message.channel.send('Keep below 251 please in any dimension.')
            return

        else:
            # Respond that the image is being generated
            await message.channel.send('Generating...')

            # remove one due to python counting from 1, not from 0
            w -= 1
            h -= 1

            # Declare variables
            folder_dir = ''  # Gets the directory where the image is stored
            images = []

            # Change the size of the image
            hb.change_size(w, h)

            # If the user wants a glitch gradient using my bubble sort, then generate and sort values, return image
            if command == 'G!GLITCH':
                images, folder_dir = await hexbot_multi_value_save(msg_list, "glitch", "bubble")

            # If the user wants a nice gradient from two values, using numpy, generate and sort values, return image
            elif command == 'G!2':
                values = msg_list[3].lstrip('#') + ',' + msg_list[4].lstrip('#')
                images = hb.gradient(values, 'numpy')
                folder_dir = (d + '\\gradients\\two\\')

            # If the user wants to have a glitched gradient using numpy, generate and sort values, return image
            elif command == 'G!NGLITCH':
                images, folder_dir = await hexbot_multi_value_save(msg_list, "numpyGlitch", "numpyOverride")

            # Trying to make a multicolour gradient, so far not working
            elif command == 'G!DEBUG':
                word = "debug"
                images, folder_dir = await hexbot_multi_value_save(msg_list, word, word)

            # Respond with the unsorted image, and sorted image
            await message.channel.send('Unsorted')
            await message.channel.send(file=discord.File(folder_dir + images[0] + '.png'))
            await message.channel.send('Sorted')
            await message.channel.send(file=discord.File(folder_dir + images[1] + '.png'))

        # Gets the syntax to use for the gradient bot
    elif command == 'M!HELP':
        await message.channel.send('Need to do')  # TODO

    elif command == "M!DOGFACT":
        await message.channel.send(sp.dog_fact())

    elif command == "M!SCOUT":
        await message.channel.send(file=discord.File(sp.scout_voice_line()))

    # Gets the syntax to use for the gradient bot
    elif command == 'Y!HELP':
        await message.channel.send('Need to do')  # TODO

    elif command == "Y!SCOOB":
        await message.channel.send(yt.scoob())

    # Gets the syntax to use for the gradient bot
    elif command == 'S!HELP':
        await message.channel.send('Need to do')  # TODO

    elif command == "S!DDG":
        await message.channel.send("DuckDuckGo: %s" % sh.ddg_search(sh.ddg_join(msg_list)))

    elif command == "S!G":
        await message.channel.send("Google: %s" % sh.ddg_bang("!g+" + sh.ddg_join(msg_list)))

    elif command == "S!WIKI":
        await message.channel.send("Wikipedia: %s" % sh.ddg_bang("!wiki+" + sh.ddg_join(msg_list)))

    elif command == "S!SPT":
        await message.channel.send("Spotify: %s" % sh.ddg_bang("!spt+" + sh.ddg_join(msg_list)))

    elif command == "S!YT":
        await message.channel.send("YouTube: %s" % sh.ddg_bang("!yt+" + sh.ddg_join(msg_list)))

    elif command == "S!GH":
        await message.channel.send("GitHub: %s" % sh.ddg_bang("!gh+" + sh.ddg_join(msg_list)))

    elif command == "S!GL":
        await message.channel.send("GitLab: %s" % sh.ddg_bang("!glab+" + sh.ddg_join(msg_list)))

    elif command == "S!SO":
        await message.channel.send("Stack Overflow: %s" % sh.ddg_bang("!!sof+" + sh.ddg_join(msg_list)))

    elif command.strip("'") == "IM":
        if len(msg_list) - 1 > 0:
            await message.channel.send(sp.hi_blank_im(message))
        else:
            await message.channel.send("Tried to trick me :((")

# When discord client successfully starts, run
@client.event
async def on_ready():
    activity = discord.Activity(name='Lasagna Cook', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Starts the program
client.run(TOKEN)
