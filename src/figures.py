import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

def create_keyword_bar_chart(keywords, song_title, lyrics=""):
    if not lyrics.strip():
        # Mostrar mensaje si no hay letras disponibles
        fig = go.Figure()
        fig.add_annotation(
            text="No hay letras disponibles para esta canción.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="white")
        )
        fig.update_layout(
            title=f"Título: {song_title}",
            template="plotly_dark",
            plot_bgcolor="black",
            paper_bgcolor="black"
        )
        return fig

    if keywords == [("letra", 1), ("disponible", 1), ("encontró", 1), ("canción", 1)]:
        # Palabras clave genéricas, mostrar mensaje
        fig = go.Figure()
        fig.add_annotation(
            text="Palabras clave no relevantes generadas.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="white")
        )
        fig.update_layout(
            title=f"Título: {song_title}",
            template="plotly_dark",
            plot_bgcolor="black",
            paper_bgcolor="black"
        )
        return fig

    # Crear el gráfico de barras si hay palabras clave válidas
    fig = px.bar(
        x=[kw[0] for kw in keywords],
        y=[kw[1] for kw in keywords],
        labels={"x": "Palabra clave", "y": "Frecuencia"},
        color_discrete_sequence=["#1DB954"],
        title=f"Título: {song_title}"
    )
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="black",
        paper_bgcolor="black",
        xaxis=dict(tickangle=-45),
        yaxis=dict(gridcolor="gray"),
    )
    return fig

# 1. Gráfico circular para géneros
def create_genre_pie_chart(genres):
    genre_counts = {genre: genres.count(genre) for genre in set(genres)}
    fig = px.pie(
        names=list(genre_counts.keys()), 
        values=list(genre_counts.values()), 
        title="Distribución de Géneros",
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    return fig

# 2. Nube de palabras
def create_wordcloud(keywords):
    wordcloud = WordCloud(
        width=800, height=400, background_color='black', colormap='Greens'
    ).generate(' '.join(keywords))
    
    # Crear imagen con matplotlib
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Convertir imagen a base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    encoded_image = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Crear figura en Plotly sin cuadrícula
    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source=f'data:image/png;base64,{encoded_image}',
            xref="paper", yref="paper",
            x=0.5, y=0.5, sizex=1, sizey=1,
            xanchor="center", yanchor="middle",
            layer="below"
        )
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        template="plotly_dark",
        title="Nube de Palabras Clave",
        title_x=0.5,
        title_font=dict(size=20, color="#1DB954"),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig

# 4. Línea de tiempo de canciones
def create_timeline(playlist):
    fig = px.scatter(
        playlist, x="energia", y="nombre", color="genero",
        labels={"energia": "Energía", "nombre": "Canción"},
        title="Línea de Tiempo: Canciones por Energía"
    )
    fig.update_layout(template="plotly_dark", yaxis=dict(showgrid=False))
    return fig