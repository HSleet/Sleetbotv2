import os
import pprint
import spotipy
from urllib.request import urlretrieve
from spotipy.oauth2 import SpotifyClientCredentials


client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Artist:

    def __init__(self, artist_object):
        self.__artist = artist_object
        self.artist_name = self.__artist["name"]
        self.artist_url = self.__artist["external_urls"]["spotify"]


class Track:

    def __init__(self, track_id):
        self.__id = track_id
        self.__track_data = sp.track(track_id)
        self.preview = self.__track_data["preview_url"]
        self.name = self.__track_data["name"]
        self.url = self.__track_data["external_urls"]["spotify"]
        self.artist = Artist(self.__track_data["artists"][0])
        self.duration = self.__track_data["duration_ms"]
        self.is_explicit = self.__track_data["explicit"]

    def __str__(self):
        return f"{self.artist.artist_name} - {self.name}"

    def __len__(self):
        duration_in_minutes = int(self.duration / 60000)
        residual_in_seconds = self.duration / 1000 % 60
        return f"Track length: {duration_in_minutes}:{residual_in_seconds:.2f}"


def search_query(search_parameter):
    song_info = sp.search(search_parameter, limit=5, type='track', market='DO')['tracks']
    preview = []
    song_list = []
    for item in song_info['items']:
        song_name = item['name']
        # pprint.pprint(item)
        song = {'name': song_name, "song_id": item['id']}
        artist = item['artists'][0]['name']
        song_list.append({'song': song, 'artists': artist, })
        preview.append(item['preview_url'])
    return song_list


if __name__ == '__main__':
    pprint.pprint(search_query("alive"))
