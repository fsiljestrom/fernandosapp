# etl.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

client_id = '69e38690efcb4887a3935eb14af7c3ec'
client_secret = 'a045c33f491b44ada745ecb925d68f64'
redirect_uri = 'http://localhost:8889/callback'

# Autenticación con Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-top-read"))


def get_genre_from_artist(artist_id):
    artist = sp.artist(artist_id)
    if 'genres' in artist and artist['genres']:
        return artist['genres'][0]  # Usamos el primer género
    return 'Unknown'


def prepare_data_for_model(df):
    df['season'] = df['month'].apply(lambda x: (x%12 + 3)//3)  # 1=Winter, 2=Spring, 3=Summer, 4=Fall
    df['genre_encoded'] = df['genre'].astype('category').cat.codes
    return df[['year', 'month', 'season', 'genre_encoded']]

def prepare_data_for_energy_model(df):
    df['season'] = df['month'].apply(lambda x: (x % 12 + 3) // 3)
    return df[['year', 'month', 'season', 'genre', 'energy']]

def get_user_top_tracks(time_range='long_term', limit=50):
    top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    track_data = []
    
    for item in top_tracks['items']:
        track_info = {
            'track_name': item['name'],
            'track_id': item['id'],
            'artist_name': item['artists'][0]['name'],
            'artist_id': item['artists'][0]['id'],
            'album': item['album']['name'],
            'played_at': item['album']['release_date'],
            'popularity': item['popularity'],
            'energy': sp.audio_features(item['id'])[0]['energy'],
            'valence': sp.audio_features(item['id'])[0]['valence'],
            'danceability': sp.audio_features(item['id'])[0]['danceability']
        }
        track_data.append(track_info)
    
    return pd.DataFrame(track_data)

def transform_data(df):
    df['played_at'] = pd.to_datetime(df['played_at'])
    df['year'] = df['played_at'].dt.year
    df['month'] = df['played_at'].dt.month
    df['genre'] = df['artist_id'].apply(get_genre_from_artist)
    return df

