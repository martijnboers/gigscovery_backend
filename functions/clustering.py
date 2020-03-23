from functions.spotify_connectors import retrieve_clusters
from functions.bit_connectors import get_concerts
from collections import defaultdict

# tok = "BQCoYIgVzsny9xOFK6_11nU9_egcbCxmXvMzHL82achbKqI5DKk5c5G1MG7c1oS6bklysNdSeWdVjTh5z42LWBpnROCBbhgG7OJSZN2rfVIR5x6FiKtJMXZ8ld-mn5s2oeSMDfwqIZlabdCXmE2v_GMbiusQZzJGxpfKPBM"
# tok = "BQDv1tNs6nJf-aGZW16OnDaHxh1NeyqoE7ht0m0QKbPI86nl_IU2x2QjybbZnJI8jTRcMhGwmdICQWioizmTEF3JtOfQMElCExu8xdwEVHnBjaKqdXdO73rQo__QNwlk-j3hD-xa2-Yeh891DAHJWodnyCTtBgkY-GoJ0sLprANIu5E"
tok = "BQAUEd1uU89TWS3cUgVm6F1lLmTG6tk8pUY45SW5nZTL7BatP3EmurmyLnEWg3CFPLz63QaidED_WdQKAyACwdUIi9kwOSoRLgP3nEBZmup1MMheuKq5Ae3Yf_gFiOPXXkx51rbSxilGnzJ3iLvFUtISeKWxddOvu7JIfa8"

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


# print((52.516543, 13.404105, "2020-03-23", "2021-04-01", "Matthias Reim", 50))