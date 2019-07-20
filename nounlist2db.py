import requests
import sqlite3

conn = sqlite3.connect('misc_class.db')
c = conn.cursor()

url = "http://www.desiquintans.com/downloads/nounlist/nounlist.txt"
r = requests.get(url, stream=True)
count = 1

for noun in r.iter_lines():
    if noun:
        print(noun.decode())
        c.execute("INSERT INTO nouns(ID, Noun) VALUES(?, ?)", (count, noun.decode()))
        count += 1

conn.commit()
