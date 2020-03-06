import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from itertools import chain

os.environ['SPOTIPY_CLIENT_ID'] = "adba25a186284c00b4551d8532c7e066"
os.environ['SPOTIPY_CLIENT_SECRET'] = "0c4912fca560400c86f33449167e58e9"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                     auth="BQCQUiPYIQqE1tuh5gmWp4cmUiFpkVIjQOS8l7L3YcGQY1vR3vjEWcmBR2N6NGwlkTAwV0T9vAGSV4YVmNH4Z5fQI3xLiqYY_6MI43iv_vrXut9aKjSRFf242rWhna2EE2v7KXguJFjuYzCgxTWfz4hcgROguLkpsHCnuEJbtyNLNTA")


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


def get_random_related_artists(artist_id, number_related_artists):
    artist_related_artists = sp.artist_related_artists(artist_id)['artists']
    new_related_artists = [prune_artist(artist) for artist in artist_related_artists]
    random_artists = random.sample(new_related_artists, number_related_artists)
    return random_artists

def get_top_tracks_artist(artist_id):
    top_tracks_artist = sp.artist_top_tracks(artist_id)['tracks']
    return top_tracks_artist 

def top_tracks_all_artists(number_of_top_artists, number_related_artists_sampled): 
    top_artists = give_top_artists(number_of_top_artists)
  
    related_artists = [get_random_related_artists(artist['id'], number_related_artists_sampled) for artist in top_artists] 
    related_artists = list(chain.from_iterable(related_artists))
  
    all_artists = top_artists + related_artists

    toptracks_artists = [get_top_tracks_artist(artists['id']) for artists in all_artists]
    toptracks_artists = list(chain.from_iterable(toptracks_artists))

    return toptracks_artists


def get_audio_features_tracks(list_all_artists):
    features_all_tracks = [sp.audio_features(artist['id']) for artist in list_all_artists]
    return features_all_tracks

#ENDPOINT 1 GET_USERS_ARTIST(n_artist)
def user_artists(n_of_top_artists, n_related_artists): 
  
    top_artists = give_top_artists(n_of_top_artists)

    related_artists = [get_random_related_artists(artist['id'],  n_related_artists) for artist in top_artists] 

    related_artists = list(chain.from_iterable(related_artists))
  
    all_artists = top_artists + related_artists

    return all_artists

