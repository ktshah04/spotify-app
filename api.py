import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Get Client Secret from .env file
load_dotenv()
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Create Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b86d857ac9514aacb46cbc596c4f6bbc",
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8890/callback",
                                               scope="playlist-read-private"))

def get_playlist_tracks(playlist_id):
    results = sp.playlist(playlist_id)
    tracks = results['tracks']['items']

    results_next = results['tracks']

    # Fetch additional tracks if the playlist has more than 100 tracks
    while results_next['next']:
        results_next = sp.next(results_next)
        tracks.extend(results_next['items'])

    return tracks

def get_audio_features(track_ids):
    audio_features = []

    for i in range(0, len(track_ids), 50):
        # Get audio features from batch of 50 tracks
        batch = track_ids[i:i+50]
        audio_features.extend(sp.audio_features(batch))

    return audio_features