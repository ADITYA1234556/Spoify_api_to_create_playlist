import requests
from bs4 import BeautifulSoup
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth
redirect_url = "https://localhost:8888/callback"
ID = "YOUR SPOTIFY ID"
PLAYLIST_URL = f"https://api.spotify.com/v1/users/{ID}/playlists"
USERNAME = "YOUR SPOTIFY USERNAME"
CLIENT_ID = "YOUR SPOTIFY CLIENT ID"
CLIENT_SECRET = "YOUR SPOTIFY CLIENT SECRET"
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

year = input("Which year do you want to travel to? Type the date in this format = YYYY-MM-DD:")
endpoint = BILLBOARD_URL + year

response = requests.get(url=endpoint)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")
song_link = soup.select("li ul li h3")
song_list = [tags.text.strip() for tags in song_link]
print(song_list)

auth_manager = SpotifyOAuth(client_id= CLIENT_ID, client_secret= CLIENT_SECRET, redirect_uri= redirect_url, scope="playlist-modify-private", show_dialog=True, cache_path=".cache", username= USERNAME)
sp = spotipy.Spotify(auth_manager = auth_manager)
playlist_create = sp.user_playlist_create(ID,name=f'{year}',public= False, collaborative= False, description='mypythonplaylist')
pprint.pprint(playlist_create)
print(playlist_create['id'])
links = []
try:
    with open ("song_links.txt", "a") as file:
        for names in song_list:
            print(names)
            result = sp.search(f"{names}")
            links.append(result["tracks"]["items"][0]["uri"])
            file.write(f"{result["tracks"]["items"][0]["uri"]}\n")
            pprint.pprint(result)
except FileNotFoundError:
    with open("song_links.txt", "w") as file:
        for names in song_list:
            print(names)
            result = sp.search(f"{names}")
            links.append(result["tracks"]["items"][0]["uri"])
            file.write(f"{result["tracks"]["items"][0]["uri"]}\n" )
            pprint.pprint(result)
else:
    pass

sp.playlist_add_items(playlist_id=playlist_create['id'], items=links)


