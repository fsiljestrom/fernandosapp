import plotly.express as px

def create_keywords_figure(top_keywords, song_name):
    fig = px.bar(
        x=[kw[0] for kw in top_keywords],
        y=[kw[1] for kw in top_keywords],
        labels={"x": "Palabra clave", "y": "Frecuencia"},
        title=f"Palabras clave: {song_name}"
    )
    fig.update_layout(template="plotly_dark")
    return fig
