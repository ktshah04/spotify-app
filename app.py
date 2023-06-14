import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, session
import api

# Get Client Secret from .env file
load_dotenv()
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


app = Flask(__name__)

# Your Spotify OAuth object
sp_oauth = api.get_spotify_oauth(client_secret)


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # Save the access token in the session
    session['token_info'] = token_info

    return redirect('/playlists')


@app.route('/playlists')
def playlists():
    # Get the access token from the session
    token_info = session.get('token_info')

    if token_info is None:
        # The user isn't logged in
        return redirect('/login')

    # Update the Spotify OAuth object with the new token
    sp_oauth.set_access_token(token_info['access_token'])

    # Get the user's playlists
    playlists = api.get_user_playlists(sp_oauth,sp_oauth.get_username())

    return playlists