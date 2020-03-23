from functions.spotify_connectors import retrieve_clusters
from functions.bit_connectors import get_concerts
from collections import defaultdict

def get_cluster_concerts(latitude, longitude, date_begin, date_end, bands_with_clusters, radius=150):

    if type(bands_with_clusters) == str:
        return "Not enough user data to create clusters!"

    def add_spotify_id(list_of_concerts, spotify_id):
        for concert in list_of_concerts:
            concert["spotify_id"] = spotify_id
        return list_of_concerts

    def add_flag(list_of_concerts, flag):
        for concert in list_of_concerts:
            concert["flag"] = flag
        return list_of_concerts

    clusters = defaultdict(list)

    for item in bands_with_clusters:
        clusters[item[2]].append([item[0], item[1], item[3]])

    bins = []

    for key, value in clusters.items():
        bin = {}
        bin["id"] = key
        bin["bin_reason"] = [{"band_name": band_name, "band_spotify_id": band_id, "band_flag": band_flag} for band_name, band_id, band_flag in value]
        bin["concerts"] = [add_flag(add_spotify_id(get_concerts(latitude, longitude, date_begin, date_end, band_name, radius), band_id), band_flag) for band_name, band_id, band_flag in value]
        bins.append(bin)

    return bins


def filter_bins(user_bins):

    def is_good_bin(bin):

        return len([c for c in bin["concerts"] if len(c) > 0]) > 0

    good_bins = [bin for bin in user_bins if is_good_bin(bin)]

    for index, bin in enumerate(good_bins):
        bin["id"] = index

    return good_bins


def get_bins(latitude, longitude, date_begin, date_end, token, radius=150, top_artists=5, related_artists=5):

    clusters = retrieve_clusters(top_artists, related_artists, token)
    bins = get_cluster_concerts(latitude, longitude, date_begin, date_end, clusters, radius)
    return filter_bins(bins)
