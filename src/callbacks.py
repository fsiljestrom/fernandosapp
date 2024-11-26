from dash import Input, Output, State
from model import df, extract_keywords_from_lyrics
from figures import create_keyword_bar_chart
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

def register_callbacks(app):
    @app.callback(
        Output('playlist-output', 'children'),
        [Input('generar-btn', 'n_clicks')],
        [State('edad', 'value'), State('mood', 'value'),
         State('energia-input', 'value'), State('localizacion', 'value')]
    )
    def update_playlist(n_clicks, edad, mood, energia, localizacion):
        if n_clicks == 0:
            return ""
        if not all([edad, mood, energia, localizacion]):
            return "Por favor, completa todos los campos."

        mood_map = {'happy': 'pop', 'sad': 'rock', 'chill': 'jazz'}
        localizacion_map = {'gym': 'rock', 'studying': 'classical', 
                            'friends': 'pop', 'family': 'classical', 'chilling': 'jazz'}
        genre = mood_map.get(mood, 'pop')
        genre = localizacion_map.get(localizacion, genre)

        filtered_df = df[(df['energia'] >= energia - 0.3) & (df['energia'] <= energia + 0.3)]

        if filtered_df.empty:
            return "No hay canciones que coincidan con los filtros aplicados. Intenta con otros valores."

        playlist = filtered_df.sample(10) if len(filtered_df) >= 10 else filtered_df

        playlist_cards = []
        for _, row in playlist.iterrows():
            keywords = extract_keywords_from_lyrics(row.get('letra', ''))
            fig = create_keyword_bar_chart(keywords, row['nombre'], row.get('letra', ''))
            playlist_cards.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H5(row['nombre'], className="card-title"),
                        html.P(f"Artista: {row['artista']}", className="card-text"),
                        dcc.Graph(figure=fig)
                    ]),
                    style={"marginBottom": "20px"}
                )
            )
        return playlist_cards
