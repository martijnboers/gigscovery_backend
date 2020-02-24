import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

os.environ['SPOTIPY_CLIENT_ID'] = "adba25a186284c00b4551d8532c7e066"
os.environ['SPOTIPY_CLIENT_SECRET'] = "0c4912fca560400c86f33449167e58e9"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                     auth="BQDFKUpcrVQ_pI_gq0v91VjczVy0gaQsk1Ls-XDbcGdh6XU8k9Z4EV7BWKheaZg7G90ap7kq36pk9TAqOv_MrCUIx-yZk6jNDN0Bo-f9cHJoUK9lpM7nBb1Gp7Vs9zkg676iWvIGeSGkMInWKC1zAa32t8vVzSf8jfF4RbynzYzccYw")


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

