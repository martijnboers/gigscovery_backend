key = "bd482854c87eb7bc0c93d515ec3bbc29"

from bandsintown import Client

client = Client(key)


def prune_concerts(concert_list):
    pruned_concerts = []

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

    for item in concert_list[1:]:
        pruned_concerts.append(prune_concert(item))

    return pruned_concerts


def get_artist_concerts(artist_name, date_begin, date_end):
    date_range = f"{date_begin},{date_end}"
    concerts = client.artists_events(artist_name, date_range)
    pruned_concerts = prune_concerts(concert_list=concerts)
    return pruned_concerts


def filter_concert_location(latitude, longitude, concert_list):
    concerts_location = [item for item in concert_list if item["venue"]["latitude"] == latitude and item["venue"]["longitude"] == longitude]
    return concerts_location


def get_concerts(latitude, longitude, date_begin, date_end, artist):
    artist_concerts = get_artist_concerts(artist, date_begin, date_end)
    artist_location = filter_concert_location(latitude, longitude, artist_concerts)
    return artist_location

