import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="38f291d7ebbb41aaabbbcff7483f6dfb",
                                               client_secret="913b3f6f4eba47d98aa4113e5075ef77",
                                               redirect_uri="http://127.0.0.1:8000",
                                               scope="user-library-read"))

