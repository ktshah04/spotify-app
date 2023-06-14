import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Get Client Secret from .env file
load_dotenv()
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b86d857ac9514aacb46cbc596c4f6bbc",
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8890/callback",
                                               scope="playlist-read-private"))

# def playlist_test()

def get_track_ids(playlist_id):
    track_features = {}
    results = sp.playlist(playlist_id)
    tracks = results['tracks']['items']

    results_next = results['tracks']

    # Fetch additional tracks if the playlist has more than 100 tracks
    while results_next['next']:
        # print("results", results_next)
        results_next = sp.next(results_next)
        tracks.extend(results_next['items'])

        print(len(tracks))
        # time.sleep(10)


    for item in tracks:
        track = item['track']

        name = track['name']
        artist = [artist['name'] for artist in track['artists']]
        track_features[track['id']] = {}
        track_features[track['id']]['name'] = name
        track_features[track['id']]['artists'] = artist
        track_features[track['id']]['popularity'] = track['popularity']
        track_features[track['id']]['duration_ms'] = track['duration_ms']

    return results, track_features

# cocktail060722: 04JWClfMen29JEjTa44WhM
# woo chillay: 0x309opBADcBO0hQkSqSyo

def get_track_features(track_features):

    track_ids = list(track_features.keys())

    for i in range(0, len(track_ids), 50):
        # Get audio features from batch of 50 tracks
        batch = track_ids[i:i+50]
        audio_features = sp.audio_features(batch)

        # update features for tracks
        for t,track in enumerate(audio_features):
            track_features[track_ids[t+i]].update(track)

    return track_features

def get_playlist_features(uri):
    results, track_features = get_track_ids(uri)
    track_features = get_track_features(track_features)

    features_df = pd.DataFrame(track_features).T

    return track_features, features_df

track_features, features_df = get_playlist_features("0x309opBADcBO0hQkSqSyo")

features_df.to_csv("woo_chillay_features.csv")