import requests
import os
import pandas as pd
from bs4 import BeautifulSoup


class Artist:

    def __init__(self, name):
        self.name = name
        self.songs = dict()

    def add_song(self, song_name, url):
        song_name = song_name
        song_url = url
        self.songs.update({'song': song_name, 'url': song_url})

    def export_list(self):
        df = pd.DataFrame(self.songs, index=range(len(self.songs)))
        file_name = '{}.csv'.format(self.name)
        directory = '..\\artists_data'
        df.to_csv(os.path.join(directory, file_name), encoding='utf-8',sep=',')


def get_songs(artist_url):
    req = requests.get(artist_url)
    req.encoding = 'utf-8'
    soup2 = BeautifulSoup(req.text, "html.parser")
    artist_name = soup2.find(id='title-artista').text
    artist = Artist(artist_name)
    archive = soup2.find(id='archive')
    try:
        songs = archive.find_all('a', href=True)
    except:
        print(f'{artist_name} link not found')
    for song in songs:
        song_title = song.text
        song_url = requests.get(song['href'])
        song_url.encoding = 'utf-8'
        song_page = BeautifulSoup(song_url.text, 'html.parser')
        try:
            song_link = song_page.find('a', {'class': 'btn'})['href']
            artist.add_song(song_title, song_link)
        except:
            print(f'{song.text} link missing on {artist_name}')
    artist.export_list()


url = 'http://alofokemusic.net/musica/artistas/'
r = requests.get(url)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, "html.parser")
archive = soup.find(id='archive')
artists = archive.find_all('a', href=True)
artists_linklist = list()

for artist in artists:
    artists_linklist.append(artist['href'])

for link in artists_linklist:
    get_songs(link)
