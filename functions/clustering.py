from spotify_connectors import retrieve_clusters
from bit_connectors import get_concerts
from collections import defaultdict
from pprint import pprint

# tok = "BQCoYIgVzsny9xOFK6_11nU9_egcbCxmXvMzHL82achbKqI5DKk5c5G1MG7c1oS6bklysNdSeWdVjTh5z42LWBpnROCBbhgG7OJSZN2rfVIR5x6FiKtJMXZ8ld-mn5s2oeSMDfwqIZlabdCXmE2v_GMbiusQZzJGxpfKPBM"
# tok = "BQDv1tNs6nJf-aGZW16OnDaHxh1NeyqoE7ht0m0QKbPI86nl_IU2x2QjybbZnJI8jTRcMhGwmdICQWioizmTEF3JtOfQMElCExu8xdwEVHnBjaKqdXdO73rQo__QNwlk-j3hD-xa2-Yeh891DAHJWodnyCTtBgkY-GoJ0sLprANIu5E"
tok = "BQAUEd1uU89TWS3cUgVm6F1lLmTG6tk8pUY45SW5nZTL7BatP3EmurmyLnEWg3CFPLz63QaidED_WdQKAyACwdUIi9kwOSoRLgP3nEBZmup1MMheuKq5Ae3Yf_gFiOPXXkx51rbSxilGnzJ3iLvFUtISeKWxddOvu7JIfa8"

def get_cluster_concerts(latitude, longitude, date_begin, date_end, bands_with_clusters):

    if type(bands_with_clusters) == str:
        return "Not enough user data to create clusters!"

    clusters = defaultdict(list)

    for item in bands_with_clusters:

        clusters[item[2]].append([item[0], item[1]])

    bins = []

    for key, value in clusters.items():
        bin = {}
        bin["id"] = key
        bin["bin_reason"] = [{"band_name": band_name, "band_spotify_id": band_id} for band_name, band_id in value]
        bin["concerts"] = [get_concerts(latitude, longitude, date_begin, date_end, band_name) for band_name, _ in value]
        bins.append(bin)

    return bins


def filter_bins(user_bins):

    def is_good_bin(bin):

        return len([c for c in bin["concerts"] if len(c) > 0]) > 0

    good_bins = [bin for bin in user_bins if is_good_bin(bin)]

    for index, bin in enumerate(good_bins):
        bin["id"] = index

    return good_bins



def get_bins(latitude, longitude, date_begin, date_end, token, top_artists=10, related_artists=5):

    clusters = retrieve_clusters(top_artists, related_artists, token)
    bins = get_cluster_concerts(latitude, longitude, date_begin, date_end, clusters)
    return filter_bins(bins)




# bins = get_cluster_concerts(51.284127, 10.495945, "2020-01-02", "2020-07-02", retrieve_clusters(6, 5, tok))

# pprint(filter_bins(bins))

