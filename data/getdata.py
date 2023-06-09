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

def filter_important_audio_features(audio_features):
    feature_cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                    'liveness', 'valence', 'tempo', 'duration_ms', 'key', 'mode', 'time_signature']
    if audio_features is None or len(audio_features) == 0:
        return None
    return {k: audio_features[k] for k in feature_cols}

def format_genres(genres):
    return ','.join(genres)

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
        num_tracks = len(tracks)
        print(f"{num_tracks} tracks")

        # get several track artists at once to reduce api calls
        artist_ids = [track['track']['artists'][0]['id'] for track in tracks] # get main artist ids, one-to-one mapping with tracks
        artist_id_chunks = [artist_ids[i:i+50] for i in range(0, len(artist_ids), 50)] # max 50 artists per request
        artists = []
        for artist_id_chunk in artist_id_chunks:
            artists.extend(spotify.artists(artist_id_chunk)['artists'])
        
        print(f"{len(artists)} artist details retrieved")

        # get several audio features at once to reduce api calls
        track_ids = [track['track']['id'] for track in tracks]
        track_id_chunks = [track_ids[i:i+50] for i in range(0, len(track_ids), 50)] # max 50 tracks per request
        audio_features = []
        for track_id_chunk in track_id_chunks:
            audio_features.extend(spotify.audio_features(track_id_chunk))

        print(f"{len(audio_features)} track audio features retrieved")

        #Get track info and audio features
        for j, track in enumerate(tracks):
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_artist_id = track['track']['artists'][0]['id']
            track_artist_name = track['track']['artists'][0]['name']
            track_genres = format_genres(artists[j]['genres']) # one-to-one mapping with tracks
            track_audio_features = filter_important_audio_features(audio_features[j]) # one-to-one mapping with tracks
            
            print(f"\t--- {j+1} / {num_tracks} ---")
            print(f"\tTrack: {track_name} @ {track_id}")
            print(f"\tArtist: {track_artist_name} @ {artists[j]['id']}")
            print(f"\tAudio features: {track_audio_features}")
            print(f"\tGenres: {track_genres}")

            #Add to data
            data.append({'id': track_id, 'name': track_name,
                         'artist_id':track_artist_id, 'artist': track_artist_name,
                         'playlist_id': playlist_id, 'playlist': playlist_name,
                         'genres': track_genres, **track_audio_features})

    
        #Write to csv
        print("playlist checkpoint: writing to csv...")
        write_to_csv('data.csv', data)
