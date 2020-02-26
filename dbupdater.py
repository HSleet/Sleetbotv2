import sqlite3
import os
import pandas as pd


def create_table(conn, sql_string):
    c = conn.cursor()
    c.execute(sql_string)


def add_artist(conn, artist):
    sql = '''INSERT INTO artists(name)
             VALUES(?)'''
    c = conn.cursor()
    c.execute(sql, artist)
    return c.lastrowid


def add_song(conn, song):
    sql = """INSERT INTO songs(artist_id, song_name,file_url) VALUES(?,?,?)"""
    c = conn.cursor()
    c.execute(sql, song)



sql_create_artists_table = """CREATE TABLE IF NOT EXISTS artists(
                                    id integer PRIMARY KEY,
                                    name text not null)"""


sql_create_songs_table = """CREATE TABLE IF NOT EXISTS songs(
                                id integer PRIMARY KEY,
                                artist_id integer NOT NULL,
                                song_name text NOT NULL,
                                file_url text,
                                FOREIGN KEY (artist_id) REFERENCES artists(id))"""


connect = sqlite3.connect('alofoke.db')
with connect:
    create_table(connect, sql_create_artists_table)
    create_table(connect, sql_create_songs_table)
    data_dir = ".\\artists_data\\"
    data_files = os.scandir(data_dir)
    for file in data_files:
        file_path = file.path
        file_name = file.name
        artist_name = (str(file_name[:-4]),)
        artist_id = add_artist(connect, artist_name)
        df = pd.read_csv(file_path, index_col=0)
        for index, row in df.iterrows():
            song_name = row['song']
            song_url = row['url']
            song = (artist_id, song_name, song_url)
            add_song(connect, song)
