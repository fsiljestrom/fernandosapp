import pandas as pd
from sklearn.cluster import KMeans
from rake_nltk import Rake
from nltk.corpus import stopwords
import re
from collections import Counter
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Cargar dataset
df = pd.read_csv('../tracks.csv')

# Configura la autenticación de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = '69e38690efcb4887a3935eb14af7c3ec',
    client_secret = 'a045c33f491b44ada745ecb925d68f64',
    redirect_uri = 'http://localhost:8889/callback',
    scope = "playlist-modify-private playlist-modify-public"
))

def preprocess_lyrics(lyrics):
    if pd.isna(lyrics) or len(lyrics.strip()) == 0:
        return []
    cleaned_text = re.sub(r'[^\w\s]', '', lyrics.lower())
    tokens = cleaned_text.split()
    combined_stopwords = set(stopwords.words('spanish')).union(set(stopwords.words('english')))
    return [word for word in tokens if word not in combined_stopwords]

def create_spotify_playlist(playlist):
    # Crear una nueva playlist en la cuenta autenticada
    user_id = sp.current_user()["id"]
    playlist_name = "Mi Playlist Generada"
    playlist_description = "Playlist generada automáticamente por la app."
    
    # Crear la playlist
    new_playlist = sp.user_playlist_create(user=user_id, 
                                           name=playlist_name, 
                                           public=False, 
                                           description=playlist_description)
    
    if 'id' not in playlist.columns:
        raise ValueError("El DataFrame debe contener una columna 'id' para crear URIs de canciones.")
    
    # Crear la columna 'uri' basada en 'id', si no existe
    if 'uri' not in playlist.columns:
        playlist['uri'] = 'spotify:track:' + playlist['id']

    # Validar que la columna 'uri' contiene datos válidos
    if playlist['uri'].isnull().any():
        raise ValueError("Existen valores nulos en la columna 'uri'. Revisa el DataFrame de entrada.")

    # Convertir la columna 'uri' en una lista
    track_uris = playlist['uri'].tolist()
    
    # Crear una nueva playlist en la cuenta del usuario autenticado
    user_id = sp.current_user()['id']
    playlist_name = "Mi Playlist Generada"
    playlist_description = "Playlist generada automáticamente con Spotipy"
    new_playlist = sp.user_playlist_create(user=user_id, 
                                           name=playlist_name, 
                                           public=False, 
                                           description=playlist_description)
    
    # Agregar las canciones a la nueva playlist
    sp.playlist_add_items(playlist_id=new_playlist['id'], items=track_uris)
    
    # Retornar el enlace a la playlist creada
    return new_playlist['external_urls']['spotify']
    

def extract_keywords_from_lyrics(lyrics):
    tokens = preprocess_lyrics(lyrics)
    word_counts = Counter(tokens)
    return word_counts.most_common(10)

def apply_clustering(data, n_clusters=5):
    clustering_model = KMeans(n_clusters=n_clusters)
    data['cluster'] = clustering_model.fit_predict(data[['energia']])
    return data, clustering_model
