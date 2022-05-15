import requests
from pprint import pprint
import json


def create_playlist(user_id, date):
    with open("token.txt", "r") as token_file:
        token = json.load(token_file)
    print(token)

    playlist_ep = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    header_playlist = {
        'Authorization': f"{token['token_type']} {token['access_token']}"
    }

    create_pl_parameters = {
        'name': f"{date} BillBoard 100",
        'public': False,
        'description': f"Top 100 songs from the year {date[0:4]}"
    }

    pl_response = requests.post(
        url=playlist_ep,
        headers=header_playlist,
        json=create_pl_parameters
    )

    print(f"Playlist response: {pl_response.status_code}")
    print(pl_response.text)
    pprint(pl_response.json())
    play_id = pl_response.json()
    print(play_id)

    pprint(f"Playlist ID: {play_id['id']}")
    return play_id['id']


def add_tracks(playlist_id, track_uri):
    with open("token.txt", "r") as token_file:
        token = json.load(token_file)
    print(token)

    add_tracks_endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    add_tracks_header = {
        'Authorization': f"Bearer {token['access_token']}",
        'Content-Type': 'application/json'}
    add_tracks_params = {'uris': track_uri}

    response_add_tracks = requests.post(
        url=add_tracks_endpoint,
        headers=add_tracks_header,
        json=add_tracks_params
    )

    print(response_add_tracks.status_code)
    print(response_add_tracks.raise_for_status())

