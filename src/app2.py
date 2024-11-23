import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from rake_nltk import Rake
from nltk.corpus import stopwords
from collections import Counter
import re
import nltk

# Cargar el dataset
df = pd.read_csv('../tracks.csv')  # Ajusta la ruta según sea necesario

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Generador de Playlist"

# Estilos personalizados
app.layout = html.Div(
    children=[
        # Cabecera
        html.Header(
            children=[
                html.H1(
                    "Genera tu playlist",
                    style={
                        'textAlign': 'center',
                        'fontSize': '36px',
                        'color': '#1DB954',
                        'fontFamily': 'Circular, sans-serif',
                        'marginTop': '10px',
                        'marginBottom': '10px'
                    }
                ),
                html.Img(
                    src='/assets/spoti.png',
                    style={
                        'width': '100px',
                        'display': 'block',
                        'margin': 'auto'
                    }
                )
            ],
            style={
                'backgroundColor': 'black',
                'padding': '10px',
                'borderRadius': '10px'
            }
        ),

        # Contenedor del formulario
        dbc.Container(
            children=[
                dbc.Row([ 
                    dbc.Col(html.Label("Edad:", style={'color': 'white', 'fontSize': '18px'}), width=2),
                    dbc.Col(dcc.Input(id='edad', type='number', placeholder="Introduce tu edad",
                                      style={'width': '100%', 'padding': '10px', 'borderRadius': '8px'}), width=10)
                ], style={'marginTop': '30px'}),

                dbc.Row([ 
                    dbc.Col(html.Label("Mood:", style={'color': 'white', 'fontSize': '18px'}), width=2),
                    dbc.Col(dcc.Dropdown(id='mood', options=[
                        {'label': 'Feliz', 'value': 'happy'},
                        {'label': 'Triste', 'value': 'sad'},
                        {'label': 'Relajado', 'value': 'chill'}
                    ], placeholder="Selecciona tu estado de ánimo", style={'borderRadius': '8px', 'padding': '10px'}), width=10)
                ], style={'marginTop': '30px'}),

                dbc.Row([ 
                    dbc.Col(html.Label("Energía:", style={'color': 'white', 'fontSize': '18px'}), width=2),
                    dbc.Col(
                        html.Div(
                            dcc.Slider(
                                id='energia-input',
                                min=0, max=1, step=0.01, value=0.5,
                                marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            ),
                            style={'marginTop': '10px'}
                        ),
                        width=10
                    )
                ], style={'marginTop': '30px'}),

                dbc.Row([ 
                    dbc.Col(html.Label("¿Dónde te encuentras?", style={'color': 'white', 'fontSize': '18px'}), width=2),
                    dbc.Col(dcc.Dropdown(id='localizacion', options=[
                        {'label': 'Gimnasio', 'value': 'gym'},
                        {'label': 'Estudiando', 'value': 'studying'},
                        {'label': 'Con amigos', 'value': 'friends'},
                        {'label': 'En familia', 'value': 'family'},
                        {'label': 'Pasando el rato', 'value': 'chilling'}
                    ], placeholder="Selecciona la localización", style={'borderRadius': '8px', 'padding': '10px'}), width=10)
                ], style={'marginTop': '30px'}),

                dbc.Row([ 
                    dbc.Col(html.Button("Generar Playlist", id='generar-btn', n_clicks=0, className="btn btn-success",
                                        style={
                                            'backgroundColor': '#1DB954',
                                            'color': 'white',
                                            'padding': '15px 30px',
                                            'borderRadius': '50px',
                                            'fontSize': '20px',
                                            'border': 'none',
                                            'marginTop': '40px',
                                            'width': '100%' }
                                        ), width=12),
                ], style={'textAlign': 'center'}),

                # Contenedor para mostrar la playlist generada
                html.Div(id='playlist-output', style={'marginTop': '50px'})
            ],
            fluid=True,
            style={'padding': '50px', 'backgroundColor': '#121212', 'borderRadius': '15px'}
        )
    ],
    style={'backgroundColor': '#121212', 'height': '100vh'}
)


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


@app.callback(
    Output('playlist-output', 'children'),
    [Input('generar-btn', 'n_clicks')],
    [State('edad', 'value'),
     State('mood', 'value'),
     State('energia-input', 'value'),
     State('localizacion', 'value')]
)
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

    playlist = filtered_df.sample(5) if len(filtered_df) >= 5 else filtered_df

    playlist_cards = []
    for _, row in playlist.iterrows():
        # Extraer palabras clave para cada canción solo si tiene letra
        if row['letra']:  # Solo si hay letra disponible
            top_keywords = extract_keywords_from_lyrics(row['letra'])
        else:
            top_keywords = []  # Si no hay letra, no hay palabras clave

        # Crear visualización con las palabras clave
        fig = px.bar(
            x=[kw[0] for kw in top_keywords],
            y=[kw[1] for kw in top_keywords],
            labels={"x": "Palabra clave", "y": "Frecuencia"},
            title=f"Palabras clave: {row['nombre']}"
        )
        fig.update_layout(template="plotly_dark")
        
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


if __name__ == '__main__':
    app.run_server(debug=True)
