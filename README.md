# Gigscovery API

What is Gigscovery?
Gigscovery is a personalized concert discovery service using Spotify data to provide users with concerts for both known and related artists. Gigscovery was designed according to privacy by design principles and does not store any spotify-related user data on our servers. 

Gigscovery was built with the Spotify API and BandsinTown API using the following endpoints: 

Spotify:
- Get User's Top Artists and Tracks
- Get Audio Features for Several Tracks

Bands in Town:

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

- #ENDPOINT 1: USERS ARTIST (TOP + RELATED)

This endpoint will return both top and related artists based on a Spotify user token, the parameters number of top and related artists can be changed accordingly. 

- #ENDPOINT 2: USER'S TRACKs FEATURE SPACE

This endpoint will return certain track features for the artists returned from the first endpoint above. 

Finally, concert clusters based on the songs of top artists and related artists from endpoint 2 will be returned in get_bins through latitude and longitude parameters. The date range as well as the radius of the top and related artists can be adjusted accordingly. 


# Disclaimer

This is not an official Spotify product.

# Contact information

For help or issues using Gigscovery, please submit a GitHub issue.
