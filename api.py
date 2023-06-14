import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Get Client Secret from .env file
load_dotenv()
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

def get_spotify_oauth(client_secret):
    # Create Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b86d857ac9514aacb46cbc596c4f6bbc",
                                                   client_secret=client_secret,
                                                   redirect_uri="http://localhost:8890/callback",
                                                   scope="user-top-read playlist-read-private user-library-read"))
    return sp

def get_user_playlists(sp,user):
    """
    Returns all playlists for a user
    """
    return sp.user_playlists(user)

def get_playlist_tracks(sp,playlist_id):
    """
    Returns all tracks in a playlist
    """
    results = sp.playlist(playlist_id)
    tracks = results['tracks']['items']

    results_next = results['tracks']

    # Fetch additional tracks if the playlist has more than 100 tracks
    while results_next['next']:
        results_next = sp.next(results_next)
        tracks.extend(results_next['items'])

    return tracks

def get_user_saved_tracks(sp):
    """
    Returns all tracks a user has liked
    """
    return sp.current_user_saved_tracks()


def get_user_top_artists_and_tracks(sp,time_range='medium_term', limit=20):
    """
    Returns top artists and tracks for a user.
    time_range: Valid-values:
                long_term (calculated from several years of data and including all new data as it becomes available),
                medium_term (approximately last 6 months),
                short_term (approximately last 4 weeks).
                Default: medium_term
    limit: The number of entities to return. Default: 20.
           Minimum: 1. Maximum: 50. For example, for 'current_user_saved_tracks(limit=50)',
           a Playlist object will be returned with maximum 50 items.
    """
    top_artists = sp.current_user_top_artists(time_range=time_range, limit=limit)
    top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=limit)

    return top_artists, top_tracks

def get_audio_features(sp,track_ids):
    audio_features = []

    for i in range(0, len(track_ids), 50):
        # Get audio features from batch of 50 tracks
        batch = track_ids[i:i+50]
        audio_features.extend(sp.audio_features(batch))

    return audio_features