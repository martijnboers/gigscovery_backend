import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from itertools import chain

os.environ['SPOTIPY_CLIENT_ID'] = "adba25a186284c00b4551d8532c7e066"
os.environ['SPOTIPY_CLIENT_SECRET'] = "0c4912fca560400c86f33449167e58e9"

def name():
    return "Natasha"


def give_top_artists(number_artists, token):

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)

    current_user_top_artists = sp.current_user_top_artists(limit = number_artists, offset = 0, time_range ='medium_term')['items']
    new_artists = [prune_artist(artist) for artist in current_user_top_artists]
    return new_artists


def prune_artist(artist):
    artist_dict = {}
    for key, value in artist.items():
        if key in ["genres", "id", "name"]:
            artist_dict[key]=value
    return artist_dict


def get_random_related_artists(artist_id, number_related_artists, token):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)
    artist_related_artists = sp.artist_related_artists(artist_id)['artists']
    new_related_artists = [prune_artist(artist) for artist in artist_related_artists]
    random_artists = random.sample(new_related_artists, number_related_artists)
    return random_artists

def get_top_tracks_artist(artist_id, token):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)
    top_tracks_artist = sp.artist_top_tracks(artist_id)['tracks']
    return top_tracks_artist 

def top_tracks_all_artists(number_of_top_artists, number_related_artists_sampled, token):
    top_artists = give_top_artists(number_of_top_artists, token)
  
    related_artists = [get_random_related_artists(artist['id'], number_related_artists_sampled) for artist in top_artists] 
    related_artists = list(chain.from_iterable(related_artists))
  
    all_artists = top_artists + related_artists

    toptracks_artists = [get_top_tracks_artist(artists['id']) for artists in all_artists]
    toptracks_artists = list(chain.from_iterable(toptracks_artists))

    return toptracks_artists


def get_audio_features_tracks(list_all_artists, token):

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)

    features_all_tracks = [sp.audio_features(artist['id']) for artist in list_all_artists]

    return features_all_tracks

#ENDPOINT 1 GET_USERS_ARTIST(top artists + related artists )
def user_artists(n_of_top_artists, n_related_artists, token):

    top_artists = give_top_artists(n_of_top_artists, 'token')

    related_artists = [get_random_related_artists(artist['id'],  n_related_artists, token) for artist in top_artists]

    related_artists = list(chain.from_iterable(related_artists))
  
    all_artists = top_artists + related_artists

    return all_artists

#ENDPOINT 2 GET USERS FEATURE SPACE (song features of tracks of all artists)
def user_track_features(n_of_top_artists, n_related_artists, token):
    
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)
    
    all_artists = user_artists(n_of_top_artists, n_related_artists, token)
    
    toptracks_artists = [get_top_tracks_artist(artists['id']) for artists in all_artists]
    toptracks_artists = list(chain.from_iterable(toptracks_artists))

    features_all_tracks = [sp.audio_features(artist['id']) for artist in toptracks_artists]
    return features_all_tracks
