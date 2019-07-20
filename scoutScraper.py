from bs4 import BeautifulSoup
import re
import urllib3

http = urllib3.PoolManager()
url = "https://wiki.teamfortress.com/wiki/Scout_responses"

response = http.request('GET', url)
soup = BeautifulSoup(response.data, features='html.parser')

for link in soup.find_all('a', attrs={'href': re.compile("/w/images")}):
    print(link.get('href'))

    r = http.request('GET', "https://wiki.teamfortress.com" + link.get('href'), preload_content=False)

    with open("scoutVoices\\" + link.get('href')[15:], 'wb') as out:
        while True:
            data = r.read()
            if not data:
                break
            out.write(data)

    r.release_conn()
