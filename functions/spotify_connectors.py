import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

os.environ['SPOTIPY_CLIENT_ID'] = "adba25a186284c00b4551d8532c7e066"
os.environ['SPOTIPY_CLIENT_SECRET'] = "0c4912fca560400c86f33449167e58e9"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                     auth="BQAfIkfWRJPzplvy3AHtj5hNvMTBbAPhRStqGe_NKdMrUBz-9VmIk4dClM0XU9uHoQYsIh9dAGcQyOq3DVkWmxpmZinhkOiFN2zGWrKULfuNyUsvKg4TaIjjpYfG8vTqY1NqL0rfiZPqwtj1i9ePhJfjtz0938RqtCzrO4ck4jfxN7Y")


def name():
    return "Natasha"


def give_top_artists(number_artists):
   current_user_top_artists = sp.current_user_top_artists(limit = number_artists, offset = 0, time_range ='medium_term')['items']
   new_artists = [prune_artist(artist) for artist in current_user_top_artists]
   return new_artists


def prune_artist(artist):
    artist_dict = {}
    for key, value in artist.items():
        if key in ["genres", "id", "name"]:
            artist_dict[key]=value
    return artist_dict

