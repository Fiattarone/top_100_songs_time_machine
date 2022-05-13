import requests
from bs4 import BeautifulSoup

TIME_MACHINE_URL = "https://www.billboard.com/charts/hot-100"

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