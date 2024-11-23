import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from layout import app_layout
from model import update_playlist

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Generador de Playlist"

# Definir el layout
app.layout = app_layout

# Configurar callback
app.callback(
    Output('playlist-output', 'children'),
    [Input('generar-btn', 'n_clicks')],
    [State('edad', 'value'),
     State('mood', 'value'),
     State('energia-input', 'value'),
     State('localizacion', 'value')]
)(update_playlist)

if __name__ == '__main__':
    app.run_server(debug=True)
