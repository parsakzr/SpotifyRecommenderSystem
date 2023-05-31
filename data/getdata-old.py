import spotipy as sp
import dotenv
import os
import csv

dotenv.load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

from spotipy.oauth2 import SpotifyClientCredentials


#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = sp.Spotify(client_credentials_manager = client_credentials_manager, requests_timeout=5, retries=3, status_retries=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])

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

    # playlist_id = '3Aq8DXOh7GZ0UrQ3dlXz4X'
    # tracks = get_playlist_tracks(playlist_id)
    # print(f"{len(tracks)} tracks")

    # Get playlist urls from playlist_urls.txt
    with open('playlist_urls.txt', 'r') as f:
        playlist_urls = f.readlines()
        # https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=94adbb8e865e4d78
        # playlist id = 37i9dQZF1DWXRqgorJj26U
    playlist_ids = [url.split('/')[-1].split('?')[0] for url in playlist_urls]
    print(f"Total playlists: {len(playlist_ids)}")


    for i, playlist_id in enumerate(playlist_ids):
        playlist_name = spotify.playlist(playlist_id)['name']
        print(f"{i+1}. Getting playlist {playlist_name}'s tracks...")
        tracks = get_playlist_tracks(playlist_id)
        print(f"{len(tracks)} tracks")

    #Get track audio features
        for j, track in enumerate(tracks):
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_artist = track['track']['artists'][0]['name']
            track_audio_features = get_track_audio_features(track_id)
            print(f"\t--- {j+1} ---")
            print(f"\tTrack: {track_name}")
            print(f"\tArtist: {track_artist}")
            print(f"\tAudio features: {track_audio_features}")
            artist = spotify.artist(track["track"]["artists"][0]["uri"])
            track_genres = artist['genres']
            print(f"\tGenres: {track_genres}")

            #Add to data
            data.append({'id': track_id, 'name': track_name, 'artist': track_artist, 'genres': track_genres, **track_audio_features})

    
        #Write to csv
        print(data)
        write_to_csv('data.csv', data)
