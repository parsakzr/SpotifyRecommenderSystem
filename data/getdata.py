import spotipy as sp
import dotenv
import os

dotenv.load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

from spotipy.oauth2 import SpotifyClientCredentials


#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = sp.Spotify(client_credentials_manager = client_credentials_manager)

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
    features



if __name__ == '__main__':
    #Get playlist tracks
    # https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=94adbb8e865e4d78
    # https://open.spotify.com/playlist/1h0CEZCm6IbFTbxThn6Xcs?si=07769dd26a374589
    playlist_id = "1h0CEZCm6IbFTbxThn6Xcs"
    tracks = get_playlist_tracks(playlist_id)
    print(len(tracks))

    #Get track audio features
    for i, track in enumerate(tracks):
        track_id = track['track']['id']
        track_audio_features = get_track_audio_features(track_id)
        print(f"{i} {track_audio_features}")