import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from pprint import pprint
from spotify import add_tracks, create_playlist

TIME_MACHINE_URL = "https://www.billboard.com/charts/hot-100"
CLIENT_ID: str
CLIENT_SECRET: str

time_ = input("Time travel to what year? (YYYY-MM-DD)\n")

response = requests.get(f"{TIME_MACHINE_URL}/{time_}")
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# print(soup.prettify())

songs = soup.select(selector="li h3")
artists = soup.select(selector="div div ul li ul li span")

song_list = [song.getText().replace("\n", "").replace("\t", "") for song in songs][:100]
artist_list = [artist.getText().replace("\n", "").replace("\t", "")
               for artist in artists if len(artist.getText().replace("\n", "").replace("\t", "")) > 2]
songs_to_artists = {song_list[i]: artist_list[i] for i in range(len(song_list))}

# print(songs_to_artists)

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []

for song, artist in songs_to_artists.items():
    query = sp.search(q=f"track: {song} year: {time_[0:4]}", type="track")
    # pprint(query)
    try:
        uri = query["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify.")
print(song_uris)

playlist = create_playlist(user_id=user_id, date=time_)

# for song in song_uris:
print(sp.playlist_add_items(playlist_id=playlist, items=song_uris))
