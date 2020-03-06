import requests
import sqlite3
from alofokeparserv2 import  add_song
from bs4 import BeautifulSoup

def get_links(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    all_links = soup.findAll('a')
    links = [{'name': link.text, 'link': link['href']} for link in all_links if len(link['href']) > 3]
    return  links


def get_songs(folder):
    base_url = 'http://www.playurbanomp3.com'
    folder_select = str(folder).capitalize()
    start_link = f'/{folder_select}/'
    print(f'Folder: {base_url}{start_link}')
    first_url = base_url + '' + start_link
    links = get_links(first_url)
    print(f'found {len(links)} artists..')

    try:
        connect = sqlite3.connect('alofoke.db')
    except:
        print('Could not establish connection to DB')
        raise
    with connect:
        for link in links:
            artist_name = link['name']
            print(f'songs for {artist_name}')
            artist_link = link['link']
            songs = get_links(base_url + '' + artist_link)
            print(f'found {len(songs)} songs')
            for song in songs:
                song_title = song['name']
                if not song_title:
                    continue
                if song_title == 'Parent Directory':
                    continue
                song_link = base_url + '' + song['link']
                print(song_link)
                song = (artist_name, song_title, song_link)
                print(f'Adding {song_title} to DB on {artist_name}')
                add_song(connect, song)


if __name__ == '__main__':
    # TODO add folder selection for songs acquisition
    # folder = input('')
    get_songs("Canciones")