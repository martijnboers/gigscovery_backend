# Gigscovery API

What is Gigscovery?
Gigscovery is a personalized concert discovery service using Spotify data to provide users with concerts for both known and related artists. Gigscovery was designed according to "privacy by design" principles and does not store any Spotify-related user data on our servers. 

Gigscovery was built with the Spotify API and BandsInTown API using the following endpoints: 

Spotify API:

- [Get User's Top Artists and Tracks](https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/)
              
- [Get Audio Features for Several Tracks](https://developer.spotify.com/console/get-audio-features-several-tracks/):

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
              item["tempo"]

Bands in Town API:

- [Get User's Top Artists and Tracks](https://rest.bandsintown.com/artists/{artistName}/events?app_id=yourkey)

        "name": artist_name,
         "photo": artist_photo,
        "artist_id": artist_bit_id,
        "date": first_item_datetime,
        "description": first_item_artist_description,
        "concert_id": first_item_concert_id,
        "offers": first_item_offers,
        "venue": first_item_venue

What has been released in this repository?
We are releasing the following: 

- ENDPOINT 1: USERS ARTIST (TOP + RELATED)

This endpoint will return both top and related artists based on a Spotify user token, the parameters number of top and related artists can be changed accordingly. 

- ENDPOINT 2: USER'S TRACKS FEATURE SPACE

This endpoint will return certain track features for the artists returned from the first endpoint above. 

- ENDPOINT 3: GET USER BINS

Finally, concert clusters based on the songs of top artists and related artists from endpoint 2 will be returned in get_bins through latitude and longitude parameters. The date range as well as the radius around the given location, and the top and related artists can be adjusted accordingly. 


# Disclaimer

This is not an official Spotify product.

# Contact information

For help or issues using Gigscovery, please submit a GitHub issue.
