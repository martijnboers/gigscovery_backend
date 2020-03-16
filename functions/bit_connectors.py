key = "bd482854c87eb7bc0c93d515ec3bbc29"

from bandsintown import Client
from math import asin, sqrt, sin, cos, pi

client = Client(key)


def prune_concerts(concert_list):

    pruned_concerts = []

    try:

        first_item = concert_list[0]

        artist_name = first_item['artist']["name"]
        artist_photo = first_item['artist']["thumb_url"]
        artist_bit_id = first_item['artist']["id"]
        first_item_datetime = first_item["datetime"]
        first_item_artist_description = first_item["description"]
        first_item_concert_id = first_item["id"]
        first_item_offers = first_item["offers"]
        first_item_venue = first_item["venue"]

        pruned_concerts.append(
            {
                "name": artist_name,
                "photo": artist_photo,
                "artist_id": artist_bit_id,
                "date": first_item_datetime,
                "description": first_item_artist_description,
                "concert_id": first_item_concert_id,
                "offers": first_item_offers,
                "venue": first_item_venue
            }
        )
    except:
        pass

    def prune_concert(concert):
        pruned = {
            "name": artist_name,
            "photo": artist_photo,
            "venue": concert["venue"],
            "offers": concert["offers"],
            "artist_id": concert["artist_id"],
            "description": concert["description"],
            "date": concert["datetime"]
        }

        return pruned

    try:
        for item in concert_list[1:]:
            try:
                pruned_concerts.append(prune_concert(item))
            except:
                continue
    except:
        pass

    # print(pruned_concerts)

    return pruned_concerts


def get_artist_concerts(artist_name, date_begin, date_end):
    date_range = f"{date_begin},{date_end}"
    print("Date range:", date_range)
    concerts = client.artists_events(artist_name, date_range)
    pruned_concerts = prune_concerts(concert_list=concerts)
    return pruned_concerts


def falls_within_latlong(latitude_venue, longitude_venue, latitude_city, longitude_city, radius):
    latitude_city = (float(latitude_city) * pi) / 180
    latitude_venue = (float(latitude_venue) * pi) / 180
    longitude_venue = (float(longitude_venue) * pi) / 180
    longitude_city = (float(longitude_city) * pi) / 180
    d = 2 * asin(sqrt((sin((latitude_venue - latitude_city) / 2))**2 + cos(latitude_venue) * cos(latitude_city) * (sin((longitude_venue - longitude_city) / 2))**2))
    distance = 6371 * d

    if distance < radius:
        return True
    else:
        return False


def filter_concert_location(latitude, longitude, concert_list, radius=150):
    concerts_location = [item for item in concert_list if
                         falls_within_latlong(item["venue"]["latitude"], item["venue"]["longitude"], latitude,
                                              longitude, radius)]
    return concerts_location


def get_concerts(latitude, longitude, date_begin, date_end, artist, radius=150):
    artist_concerts = get_artist_concerts(artist, date_begin, date_end)
    # print("Before:", artist_concerts)
    artist_location = filter_concert_location(latitude, longitude, artist_concerts, radius)
    # print("After:", artist_location)
    return artist_location

