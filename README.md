# Gigscovery API

What is Gigscovery?
Gigscovery is a personalized concert discovery service using Spotify data to provide users with concerts for both known and related artists. Gigscovery was designed according to "privacy by design" principles and does not store any Spotify-related user data on our servers. 

Gigscovery's concert recommendation logic was built using the Spotify API and BandsInTown API.

The user logs in Gigscovery using the Spotify OAuth 2.0 powered login procedure, which provides our service with a token which is issued for one hour and contains a limited ["scope"](https://developer.spotify.com/documentation/general/guides/scopes/). In our case, we only request the [*user-top-read*](https://developer.spotify.com/documentation/general/guides/scopes/#user-top-read) scope to retrieve the user's top artists, which represent the user's music taste.

Within the two abovementioned API's, the following endpoints were used: 

**Spotify API:**

- [Get User's Top Artists and Tracks](https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/)

To retrieve the top artists of the currently logged in user. 

- [Get an Artist's Related Artists](https://developer.spotify.com/console/get-artist-related-artists/)

To retrieve the related artists for each of the retrieved top artists. We do this to also search for concerts of the artists the user does not directly listen to but might enjoy based on the genre / music features.

- [Get Audio Features for Several Tracks](https://developer.spotify.com/console/get-audio-features-several-tracks/)

To retrieve the audio features of the songs of the relevant artists. We use these features to cluster within the "interest domain" of a user, to create various multiple mixes of concerts, based on similar music.


**BandsInTown API:**

- [Get Artist's Events](https://rest.bandsintown.com/artists/{artistName}/events?app_id=yourkey)

To retrieve the performances of a certain artist, within a certain date range.

---

## What has been released in this repository?

We are releasing the following: 

- **Endpoint 1:** /artists/get_user_artists

  **Query parameters:** 
  
  *n_of_top_artists*: Number of **top** artists retrieved for the current user. *Default = 5*  
  *n_related_artists*: Number of **related** artists per top artist retrieved for the current user. *Default = 5*  
  *token*: The issued, scoped Spotify token for the current user.

This endpoint will return both top and related artists based on a Spotify user token, the parameters number of top and related artists can be changed accordingly. 

- **Endpoint 2:** /tracks/features

  **Query parameters:** 
  
  *n_of_top_artists*: *float* Number of **top** artists retrieved for the current user. *Default = 5*  
  *n_related_artists*: *float* Number of **related** artists per top artist retrieved for the current user. *Default = 5*  
  *token*: *string* The issued, scoped Spotify token for the current user.

This endpoint will return the musical track features for the artists returned from the first endpoint above. 

- **Endpoint 3:** /get_bins

  **Query parameters:** 
  
  *latitude*: *float* The latitude coordinate of the location where we search for concerts.  
  *longitude*: *float* The longitude coordinate of the location where we search for concerts.  
  *date_begin*: *string* The starting date of the date range for our concert search.  
  *date_end*: *string* The starting date of the date range for our concert search.  
  *radius*: *int* The radius in kilometers around the search coordinates within which we search for concerts. *Default = 25*  
  *top_artists*: *float* Number of **top** artists retrieved for the current user. *Default = 5*  
  *related_artists*: *float* Number of **related** artists per top artist retrieved for the current user. *Default = 5*  
  *token*: *string* The issued, scoped Spotify token for the current user.

Our main endpoint which combines all the needed steps (retrieving top artists, filling with related artists, retrieving the music features, clustering the artists based on those features, retrieving the concerts for each of the cluster and finally formatting the final "bins"). We call a single concert cluster a "bin" and it is formed by concerts of the artists which produce similar music, based on the musical features.

# Usage

Assuming a clean environment that has Python 3.6+ installed, perform the following steps to start the API:

1) Clone this repository and cd into it:

   `git clone https://github.com/mabergerx/gigscovery_backend.git && cd gigscovery_backend`

2) (Optional) Create a virtual environment for the project by using [`virtualenv`](https://virtualenv.pypa.io/en/latest/):

   `virtualenv -p python3.6 ../.gigscovery_venv`

   Once created, activate the environment by using `source ../.gigscovery_venv/bin/activate` 
3) Install the requirements:  
   
   `pip install -r requirements.txt`
  
4) Once the requirements are all installed, start the server through [`uvicorn`](https://www.uvicorn.org/):

   `uvicorn main:gigscovery_app --reload`
   
5) Now, browse to http://localhost:8000/docs to access the Swagger documentation for the API. There, you can try out the endpoints and get the corresponding `curl` statements. 

# Disclaimer

This is not an official Spotify product.

# Contact information

For help or issues using Gigscovery, please submit a GitHub issue.
