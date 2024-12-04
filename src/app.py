from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks
import nltk
nltk.download('stopwords')


# Inicializar la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Generador de Playlist"
server = app.server

# Configurar el diseño
app.layout = create_layout(app)

# Registrar callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
