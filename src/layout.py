from dash import dcc, html
import dash_bootstrap_components as dbc

def create_layout(app):
    return html.Div(
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
            # Formulario
            dbc.Container(
                children=[
                    dbc.Row([ 
                        dbc.Col(html.Label("Edad:", style={'color': 'white', 'fontSize': '18px'}), width=2),
                        dbc.Col(dcc.Input(id='edad', type='number', placeholder="Introduce tu edad",
                                          style={'width': '99%', 'padding': '10px', 'borderRadius': '8px'}), width=10)
                    ], style={'marginTop': '30px', 'marginLeft':'0.5px'}),
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
                    html.Div(id='playlist-output', style={'marginTop': '50px'}),
                    # Contenedor para mostras los demás gráficos
                    html.Div(id='visualizations-output', style={'marginTop': '50px'})

                ],
                fluid=True,
                style={'padding': '50px', 'backgroundColor': '#121212', 'borderRadius': '15px'}
            )
        ],
        style={'backgroundColor': '#121212', 'height': '100vh'}
    )
