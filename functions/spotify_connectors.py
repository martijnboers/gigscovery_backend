import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from itertools import chain
from pprint import pprint
from itertools import islice, chain
from sklearn.preprocessing import normalize

os.environ['SPOTIPY_CLIENT_ID'] = "adba25a186284c00b4551d8532c7e066"
os.environ['SPOTIPY_CLIENT_SECRET'] = "0c4912fca560400c86f33449167e58e9"


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


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

    top_artists = give_top_artists(n_of_top_artists, token)

    related_artists = [get_random_related_artists(artist['id'],  n_related_artists, token) for artist in top_artists]

    related_artists = list(chain.from_iterable(related_artists))
  
    all_artists = top_artists + related_artists

    return all_artists


#ENDPOINT 2 GET USERS FEATURE SPACE (song features of tracks of all artists)
def user_track_features(n_of_top_artists, n_related_artists, token):
    
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)
    
    all_artists = user_artists(n_of_top_artists, n_related_artists, token)

    toptracks_artists = [get_top_tracks_artist(artists['id'], token) for artists in all_artists]

    toptracks_artists = list(chain.from_iterable(toptracks_artists))

    features_all_tracks = []

    for chunk in chunks(toptracks_artists, 50):
        features_all_tracks.extend(sp.audio_features([track["id"] for track in chunk]))

    features_all_tracks_with_names = []

    for features, track in zip(features_all_tracks, toptracks_artists):
        features_new = features
        features_new["artist_name"] = track['album']["artists"][0]["name"]
        features_new["artist_id"] = track['album']["artists"][0]["id"]
        features_new["track_name"] = track['name']
        features_all_tracks_with_names.append(features_new)

    return features_all_tracks_with_names


def create_data_for_clustering(user_track_features):

    data = [
        [item["danceability"],
         item["energy"],
         item["key"],
         item["loudness"],
         item["mode"],
         item["speechiness"],
         item["acousticness"],
         item["instrumentalness"],
         item["liveness"],
         item["valence"],
         item["tempo"],
         item["duration_ms"]
         ]
        for item in user_track_features
    ]

    normalized = normalize(data)

    print(normalized)


create_data_for_clustering(user_track_features(1, 1, "BQAcX-ae8sAYvZGY3yoN6d34waDqRaF70prux0UmbVDELZCqid1ZKsfdKAbaSAqP2-lAVONybJqt39fvAGcD740UA43LZCXONo5Nk5OjZN3ixuJWXX217m7VIvdG5lf5mSXdGb2_-CmgzmHyPABAxuWztC_oj5hEvzN5_wXjB_iyB7s"))


