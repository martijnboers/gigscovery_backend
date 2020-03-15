import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from itertools import chain
from pprint import pprint
from itertools import islice, chain
from sklearn.preprocessing import normalize
from sklearn.cluster import DBSCAN, KMeans
import numpy as np
import pandas as pd


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

    current_user_top_artists = sp.current_user_top_artists(limit=number_artists, offset=0, time_range='medium_term')[
        'items']
    new_artists = [prune_artist(artist) for artist in current_user_top_artists]
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

    related_artists = list(chain.from_iterable(related_artists))

    all_artists = top_artists + related_artists

    return all_artists


# ENDPOINT 2 GET USERS FEATURE SPACE (song features of tracks of all artists)
def user_track_features(n_of_top_artists, n_related_artists, token):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(),
                         auth=token)

    all_artists = user_artists(n_of_top_artists, n_related_artists, token)

    toptracks_artists = [get_top_tracks_artist(artists['id'], token) for artists in all_artists]

    toptracks_artists = list(chain.from_iterable(toptracks_artists))
    #
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

    # pprint(user_track_features)

    data = [
        {"artist_id": item["artist_id"],
         "artist_name": item["artist_name"],
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

    # pprint([(feats["track_features"], feats["artist_name"]) for feats in data])

    # for features, artist in [(feats["track_features"], feats["artist_name"]) for feats in data]:

    df = pd.DataFrame([(feats["track_features"], feats["artist_name"], feats["artist_id"]) for feats in data], columns=["features", "artist", "artist_id"])

    averages = []

    for artst in df.artist.unique():
        all_artst_tracks = df[df.artist == artst]["features"]
        artist_id = df[df.artist == artst]["artist_id"].unique()[0]
        average = normalize(np.mean(all_artst_tracks.tolist(), axis=0).reshape(1, -1)).flatten()
        averages.append((artst, artist_id, average))

    average_df = pd.DataFrame(averages, columns=["artist", "artist_id", "embedding"])

    # print(average_df[average_df.artist == "Molchat Doma"]["embedding"][0])
    # normalized = normalize(list(averages.values()))


    # pprint(normalized[:2])
    # normalized = [feats["artist_features"] for feats in data]

    # normalized_full = [{"artist_id": item["artist_id"], "artist_name": item["artist_name"], "artist_features": feats} for item, feats in zip(df.artist.unique(), normalized)]
    #
    return average_df


def cluster(clustered_data, cluster_amount=5):

    data = clustered_data.embedding.tolist()
    if data:
        # algo = DBSCAN(eps=0.5, min_samples=5).fit_predict([item["artist_features"] for item in normalized])
        algo = KMeans(cluster_amount, n_jobs=-1).fit_predict(data)

        clusters = [(artist, artist_id, label) for artist, artist_id, label in zip(clustered_data["artist"], clustered_data["artist_id"], algo) if artist != "Various Artists"]

        return clusters
    else:
        return "No user data to form the bins!"


def retrieve_clusters(n_top, n_related, token):

    track_feats = user_track_features(n_top, n_related, token)

    clustering_data = create_data_for_clustering(track_feats)

    return cluster(clustering_data)

    # print(cluster(create_data_for_clustering(user_track_features(10, 5, tok))))

# print(normalized)


# clustered = cluster(user_track_features(10, 5, "BQAdgh7WeVL8kf6LLuvjQZDivPXLkjP3h6aCug4C9GkUAed_Gxe-KkR-T5FZn_AjLFg70Gg5fIPtj5RIzF6mYOVjeNNHTfgxfC8Fckd5ST_dVkM5jtviCIDSTWqIwHPQRShKNsuYQDOZM0GqPJ5Sz6o1Ezx_hpHAOSf6YJeuP-I9dCI"))

# user_track_features(10, 5, "BQAdgh7WeVL8kf6LLuvjQZDivPXLkjP3h6aCug4C9GkUAed_Gxe-KkR-T5FZn_AjLFg70Gg5fIPtj5RIzF6mYOVjeNNHTfgxfC8Fckd5ST_dVkM5jtviCIDSTWqIwHPQRShKNsuYQDOZM0GqPJ5Sz6o1Ezx_hpHAOSf6YJeuP-I9dCI")
# print(clustered)

# tok = "BQDFvJ7LjLEkBmhi3OW1Sw1C8ZM4fFuTVQrxZuOrJvU49yevKPEb82tWzJRWQPMXUM99Vu6BGswMagmUFb70dJacEasfZ3uD97NMm6lpqKRH7IEHw93MpgtWRF7enoTo-PiTO919rC_ZkMj58pXVftMI22Jfh4JAmrb2E4Y-OaensSI"

# cluster(create_data_for_clustering(user_track_features(1, 1, tok)))

# print(cluster(create_data_for_clustering(user_track_features(10, 5, tok))))


# print(retrieve_clusters(2, 4, tok)[0])


# Maybe do it differently: retrieve many more songs per artist, then take average embedding of the artist, and then cluster artists
# Or we use the spotify endpoint that generates recommendation seeds.
# We could also request top tracks from spotify instead of retrieving top artists and getting top songs from them.