import pandas as pd
from collections import Counter
import re
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from nltk.corpus import stopwords
from rake_nltk import Rake
from figures import create_keywords_figure  # Importar la función

# Cargar el dataset
df = pd.read_csv('../tracks.csv')  # Ajusta la ruta según sea necesario

def extract_keywords_from_lyrics(lyrics):
    if pd.isna(lyrics) or len(lyrics.strip()) == 0:  # Verificar si la letra está vacía o es NaN
        return []  # Devolver una lista vacía si no hay letra
    
    # Preprocesar texto: eliminar caracteres especiales y convertir a minúsculas
    cleaned_text = re.sub(r'[^\w\s]', '', lyrics.lower())
    
    # Tokenizar texto y filtrar stopwords
    tokens = cleaned_text.split()
    filtered_tokens = [word for word in tokens if word not in stopwords.words('spanish')]
    
    # Contar frecuencia de palabras
    word_counts = Counter(filtered_tokens)
    
    # Retornar las 10 palabras más comunes
    return word_counts.most_common(10)

def update_playlist(n_clicks, edad, mood, energia, localizacion):
    if n_clicks == 0:
        return ""
    if not all([edad, mood, energia, localizacion]):
        return "Por favor, completa todos los campos."

    filtered_df = df.copy()
    mood_map = {'happy': 'pop', 'sad': 'rock', 'chill': 'jazz'}
    localizacion_map = {'gym': 'rock', 'studying': 'classical', 'friends': 'pop', 'family': 'classical', 'chilling': 'jazz'}
    genre = mood_map.get(mood, 'pop')
    genre = localizacion_map.get(localizacion, genre)

    filtered_df = filtered_df[(filtered_df['energia'] >= energia - 0.3) & 
                               (filtered_df['energia'] <= energia + 0.3)]

    if filtered_df.empty:
        return "No hay canciones que coincidan con los filtros aplicados. Intenta con otros valores."

    playlist = filtered_df.sample(20) if len(filtered_df) >= 20 else filtered_df
    return playlist_cards(playlist)

def playlist_cards(playlist):
    playlist_cards = []
    for _, row in playlist.iterrows():
        # Extraer palabras clave para cada canción solo si tiene letra
        if row['letra']:  # Solo si hay letra disponible
            top_keywords = extract_keywords_from_lyrics(row['letra'])
        else:
            top_keywords = []  # Si no hay letra, no hay palabras clave
        
        # Crear la visualización
        fig = create_keywords_figure(top_keywords, row['nombre'])
        playlist_cards.append(
            html.Div([
                dbc.Card(
                    dbc.CardBody([ 
                        html.H5(row['nombre'], className="card-title"),
                        html.P(f"Artista: {row['artista']}", className="card-text"),
                        dcc.Graph(figure=fig, style={"height": "300px"})
                    ]),
                    style={"marginBottom": "20px"}
                )
            ])
        )

    return playlist_cards
