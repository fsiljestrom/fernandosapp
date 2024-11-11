# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Importar módulos personalizados
import etl
import trainer
import visual

# Inicializar la aplicación de Dash
app = dash.Dash(__name__)
server = app.server

# Paso 1: Cargar y transformar los datos
data = etl.get_user_top_tracks()
transformed_data = etl.transform_data(data)

# Paso 2: Preparar y entrenar el modelo
model_genre_data = etl.prepare_data_for_model(transformed_data)
genre_model = trainer.train_genre_model(model_genre_data)
model_energy_data = etl.prepare_data_for_energy_model(transformed_data)
#energy_model = trainer.train_energy_model(model_energy_data)
categories = transformed_data['genre'].astype('category').cat.categories

# Crear la gráfica inicial
genre_trend_fig = visual.create_genre_trend_plot(transformed_data)

app = dash.Dash(__name__)
data = etl.get_user_top_tracks()

genre_trend_fig = visual.create_genre_trend_plot(transformed_data)
#heatmap_fig = visual.create_heatmap(transformed_data)
radar_fig = visual.create_radar_chart(transformed_data)
scatter_fig = visual.create_energy_popularity_scatter(transformed_data)

# Layout de la aplicación Dash
app.layout = html.Div([
    html.H1("Predicción de Género Musical por Época del Año", style={'textAlign': 'center'}),
    
    dcc.Graph(
        id='genre-trend-plot',
        figure=genre_trend_fig
    ),
    
    html.Div([
        html.Label("Selecciona Año:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in transformed_data['year'].unique()],
            value=transformed_data['year'].min()
        ),
        html.Label("Selecciona Mes:"),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': str(month), 'value': month} for month in transformed_data['month'].unique()],
            value=1
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(id='prediction-output', style={'textAlign': 'center', 'fontSize': 20, 'marginTop': 20})
])

@app.callback(
    Output('prediction-output', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_prediction(year, month):
    # Crear un DataFrame con los nombres de las columnas exactos
    input_data = pd.DataFrame({
        'year': [year],
        'month': [month],
        'season': [(month % 12 + 3) // 3],  # Calcula la estación
        'genre': [None]  # Puedes asignar un valor predeterminado si se espera esta columna
    })
    
    # Realizar la predicción
    try:
        #genre_prediction = energy_model.predict(input_data)
        return "Hola"
        #f"Predicción de Género: {genre_prediction[0]}"
    except Exception as e:
        return f"Error en la predicción: {e}"
# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
