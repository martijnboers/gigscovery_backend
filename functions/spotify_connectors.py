import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from itertools import islice, chain
from sklearn.preprocessing import normalize
from sklearn.cluster import DBSCAN, KMeans
import numpy as np
import pandas as pd

client_keys = "adba2@5a186284c00b4551d8532c7e066$0c4912fca560400c86f33449167e58e9@"

os.environ['SPOTIPY_CLIENT_ID'] = client_keys.split('$')[0].replace("@", "")
os.environ['SPOTIPY_CLIENT_SECRET'] = client_keys.split('$')[1].replace("@", "")


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def add_top_flag(artist, flag):
    artist["flag"] = flag
    return artist


def give_top_artists(number_artists, token):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)

    current_user_top_artists = sp.current_user_top_artists(limit=number_artists, offset=0, time_range='medium_term')[
        'items']
    new_artists = [add_top_flag(prune_artist(artist), "top") for artist in current_user_top_artists]
    return new_artists


def prune_artist(artist):
    artist_dict = {}
    for key, value in artist.items():
        if key in ["genres", "id", "name"]:
            artist_dict[key] = value
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

    related_artists = [get_random_related_artists(artist['id'], number_related_artists_sampled, token) for artist in
                       top_artists]
    related_artists = list(chain.from_iterable(related_artists))

    all_artists = top_artists + related_artists

    toptracks_artists = [get_top_tracks_artist(artists['id'], token) for artists in all_artists]
    toptracks_artists = list(chain.from_iterable(toptracks_artists))

    return toptracks_artists


def get_audio_features_tracks(list_all_artists, token):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)

    features_all_tracks = [sp.audio_features(artist['id']) for artist in list_all_artists]

    return features_all_tracks


# ENDPOINT 1 GET_USERS_ARTIST(top artists + related artists )
def user_artists(n_of_top_artists, n_related_artists, token):
    top_artists = give_top_artists(n_of_top_artists, token)

    related_artists = [get_random_related_artists(artist['id'], n_related_artists, token) for artist in top_artists]

    related_artists = [add_top_flag(artist, "related") for artist in list(chain.from_iterable(related_artists))]

    all_artists = top_artists + related_artists

    return all_artists

def add_flag_to_tracks(tracks, flag):
    for track in tracks:
        track["flag"] = flag
    return tracks

# ENDPOINT 2 GET USERS FEATURE SPACE (song features of tracks of all artists)
def user_track_features(n_of_top_artists, n_related_artists, token):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)

    all_artists = user_artists(n_of_top_artists, n_related_artists, token)

    toptracks_artists = [add_flag_to_tracks(get_top_tracks_artist(artists['id'], token), artists["flag"]) for artists in all_artists]

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
        features_new["flag"] = track["flag"]
        features_all_tracks_with_names.append(features_new)

    return features_all_tracks_with_names


def create_data_for_clustering(user_track_features):

    data = [
        {"artist_id": item["artist_id"],
         "artist_name": item["artist_name"],
         "flag": item["flag"],
         "track_features":
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
              # item["duration_ms"]
              ]}
        for item in user_track_features
    ]

    df = pd.DataFrame([(feats["track_features"], feats["artist_name"], feats["artist_id"], feats["flag"]) for feats in data], columns=["features", "artist", "artist_id", "flag"])

    averages = []

    for artst in df.artist.unique():
        all_artst_tracks = df[df.artist == artst]["features"]
        artist_id = df[df.artist == artst]["artist_id"].unique()[0]
        artist_flag = df[df.artist == artst]["flag"].unique()[0]
        average = normalize(np.mean(all_artst_tracks.tolist(), axis=0).reshape(1, -1)).flatten()
        averages.append((artst, artist_id, average, artist_flag))

    average_df = pd.DataFrame(averages, columns=["artist", "artist_id", "embedding", "flag"])

    return average_df


def cluster(clustered_data, cluster_amount=5):

    data = clustered_data.embedding.tolist()
    if data:
        # algo = DBSCAN(eps=0.5, min_samples=5).fit_predict([item["artist_features"] for item in normalized])
        algo = KMeans(cluster_amount, n_jobs=-1).fit_predict(data)

        clusters = [(artist, artist_id, label, flag) for artist, artist_id, label, flag in zip(clustered_data["artist"], clustered_data["artist_id"], algo, clustered_data["flag"]) if artist != "Various Artists"]

        return clusters
    else:
        return "No user data to form the bins!"


def retrieve_clusters(n_top, n_related, token):

    track_feats = user_track_features(n_top, n_related, token)

    clustering_data = create_data_for_clustering(track_feats)

    return cluster(clustering_data)
