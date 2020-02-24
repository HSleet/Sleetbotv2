import sqlite3
from bs4 import BeautifulSoup
conn = sqlite3.connect('alofoke.db')
c = conn.cursor()

songs_url = "http://alofokemusic.net/musica/artistas/"

