import plotly.express as px
import plotly.graph_objects as go

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
