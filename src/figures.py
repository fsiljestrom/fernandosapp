import plotly.express as px

def create_keyword_bar_chart(keywords, song_title):
    fig = px.bar(
        x=[kw[0] for kw in keywords],
        y=[kw[1] for kw in keywords],
        labels={"x": "Palabra clave", "y": "Frecuencia"},
        title=f"Palabras clave: {song_title}"
    )
    fig.update_layout(template="plotly_dark")
    return fig
