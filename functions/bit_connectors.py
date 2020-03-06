key = "bd482854c87eb7bc0c93d515ec3bbc29"

from bandsintown import Client
client = Client(key)

def filter_concert_location(city, concert_list):
  concerts_location = [item for item in concert_list if item["venue"]["city"] == city]
  return concerts_location

def get_concerts(location, date, artist):
  artist_concerts = get_artist_concerts(artist, date)
  artist_location = filter_concert_location(location,artist_concerts)
  return artist_location

