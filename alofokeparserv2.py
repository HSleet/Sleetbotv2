import re
import requests
import sqlite3
import os
from bs4 import BeautifulSoup as bs


def create_table(conn, sql_string):
    c = conn.cursor()
    c.execute(sql_string)


def add_song(conn, song):
    sql = """INSERT INTO songs(artist, song_name,file_url) VALUES(?,?,?)"""
    c = conn.cursor()
    c.execute(sql, song)


sql_create_songs_table = """CREATE TABLE IF NOT EXISTS songs(
                                id integer PRIMARY KEY,
                                artist text NOT NULL,
                                song_name text NOT NULL,
                                file_url text NOT NULL)"""


def get_last_song():
    match = lambda href: int(re.search(r'\d+', href).group())
    request = requests.get('http://alofokemusic.net/musica/')
    soup = bs(request.text, 'html.parser')
    last_mp3_element = soup.find('ul', {'class': 'mp3s'})
    last_element_tag = last_mp3_element.find('a')
    tag_href = last_element_tag['href']
    return match(tag_href)


def main():

    with connect:
        create_table(connect, sql_create_songs_table)
        loop_start = get_last_song()
        print(f'Starting loop on {loop_start}')
        for i in range(loop_start, 0, -1):
            url = f'http://alofokemusic.net/musica/{i}/'
            print(f'Requesting {url}...')
            request = requests.get(url, allow_redirects=False)
            request.encoding = 'utf-8'
            if request.status_code == 200:
                print(f'{request.status_code} - {request.url}:\nLooking for song info..')
                soup = bs(request.text, 'html.parser')
                btn = soup.find('a', {'class': 'btn'})
                info = soup.find(id='title')
                song_title = info.text
                song_info = song_title.split('–')
                artists = song_info[:-1]
                try:
                    artists = artists[0].split('ft')
                except:
                    artists = [song_title]
                artist = artists[0]
                try:
                    download_link = btn['href']
                    print(f'{song_title} Download Link found')
                    print(f'Sending {artist}, {song_title} to songs table')
                except:
                    download_link = None
                    print(f'{song_title}: No download Link')
                    continue
                song = (artist, song_title, download_link)
                add_song(connect, song)


print('connecting to database...')
try:
    connect = sqlite3.connect('alofoke.db')
    print('Connected')
except:
    print('Could not establish connection to DB')
    raise
main()
