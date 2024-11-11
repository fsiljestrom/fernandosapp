# visual.py
import plotly.express as px
import pandas as pd

def create_genre_trend_plot(df):
    genre_counts = df.groupby(['month', 'genre']).size().unstack(fill_value=0)
    genre_counts = genre_counts.reset_index()
    genre_counts = pd.melt(genre_counts, id_vars=['month'], value_name='count', var_name='genre')
    fig = px.line(genre_counts, x='month', y='count', color='genre',
                  title="Tendencia de Géneros Musicales por Mes")
    return fig

def create_genre_trend_plot(df):
    genre_counts = df.groupby(['month', 'genre']).size().unstack(fill_value=0)
    genre_counts = genre_counts.reset_index()
    genre_counts = pd.melt(genre_counts, id_vars=['month'], value_name='count', var_name='genre')
    fig = px.line(genre_counts, x='month', y='count', color='genre', title="Tendencia de Géneros Musicales por Mes")
    return fig

def create_heatmap(df):
    df['day_of_week'] = df['played_at'].dt.dayofweek
    df['hour'] = df['played_at'].dt.hour
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)
    fig = px.imshow(heatmap_data, labels=dict(x="Hora", y="Día de la Semana", color="Escuchas"),
                    x=heatmap_data.columns, y=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                    title="Patrón de Escucha por Día y Hora")
    return fig

def create_radar_chart(df):
    genre_counts = df['genre'].value_counts()
    fig = px.line_polar(r=genre_counts.values, theta=genre_counts.index, line_close=True,
                        title="Distribución de Géneros Musicales", template="plotly_dark")
    return fig

def create_energy_popularity_scatter(df):
    fig = px.scatter(df, x="energy", y="popularity", color="genre",
                     title="Comparación de Energía y Popularidad por Género",
                     labels={"energy": "Energía", "popularity": "Popularidad"})
    return fig
