import sqlite3  # Used to get data from database
from os import listdir, path, mkdir  # Used to list the directories in the scout dir
from random import randint, choice  # Used to randomly select a number from ID and for randomly selecting files
from secret import Secrets  # Used to get the API key from secrets.py


class Misc:
    getSecret = Secrets()  # Creates a object called getSecret from the class Secrets
    youtubeKey = getSecret.youtube()  # Gets the YouTube API key

    conn = sqlite3.connect('misc_class.db')
    c = conn.cursor()

    d = path.abspath(path.dirname(__file__))  # directory of script

    # Stupid dad joke thing every bot alive has now
    def hi_blank_im(self, message):
        split_msg = message.content.split(' ')
        word = split_msg[1]

        self.c.execute("SELECT max(rowid) from nouns")
        n = self.c.fetchone()[0]
        num = randint(1, n)

        self.c.execute("SELECT noun FROM nouns WHERE ID=?;", (num,))
        raw_noun = self.c.fetchall()
        noun = str(raw_noun[0][0])
        msg = ("Hi %s, I'm %s" % (word, noun)).format(message)
        return msg

    # Randomly selects a fact from a sqlite database
    def dog_fact(self):

        self.c.execute("SELECT max(rowid) from dog_facts")
        n = self.c.fetchone()[0]
        num = randint(1, n)

        self.c.execute("SELECT fact FROM dog_facts WHERE ID=?;", (num,))
        fact = str(self.c.fetchall()[0][0])

        return fact

    # Randomly select a file from scoutVoices directory
    def scout_voice_line(self):
        voice = choice(listdir(self.d + '\\scoutVoices\\'))
        return self.d + '\\scoutVoices\\' + voice

    def __init__(self):
        scout_exits = path.isdir(self.d + "\\scoutVoices\\")

        if not scout_exits:
            mkdir(self.d + '\\scoutVoices\\')

