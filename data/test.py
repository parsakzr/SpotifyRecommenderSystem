import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import dotenv
import os
import csv

dotenv.load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = sp.Spotify(client_credentials_manager = client_credentials_manager, requests_timeout=1, retries=1)

#Get data
def get_playlist_tracks(playlist_id):
    results = spotify.user_playlist_tracks("spotify", playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks

def get_track_audio_features(track_id):
    features =  spotify.audio_features(track_id)
    feature_cols = ['id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
    if features is None or len(features) == 0 or features[0] is None:
        return None
    return {k: v for k, v in features[0].items() if k in feature_cols}


def get_track_genres(track_id):
    artist_id = spotify.track(track_id)['artists'][0]['id']
    genres = spotify.artist(artist_id)['genres']
    return genres

def write_to_csv(filename, data):
    # list of dictionary of each track: 
    # write to csv
    columns = data[0].keys()
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for track in data:
            writer.writerow(track)


if __name__ == '__main__':
    data = []

    playlist_id = '37i9dQZF1DWSYVW0BVc4a3'
    tracks = get_playlist_tracks(playlist_id)
    artists = []
    for track in tracks:
        artist_id = track['track']['artists'][0]['id']
        artists.append(artist_id)
    print(artists)

    # get several artists' genres
    artists = spotify.artists(artists)
    genres = [artist['genres'] for artist in artists['artists']]

    print(genres)
    