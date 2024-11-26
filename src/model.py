import pandas as pd
from sklearn.cluster import KMeans
from rake_nltk import Rake
from nltk.corpus import stopwords
import re
from collections import Counter

# Cargar dataset
df = pd.read_csv('../tracks.csv')

def preprocess_lyrics(lyrics):
    if pd.isna(lyrics) or len(lyrics.strip()) == 0:
        return []
    cleaned_text = re.sub(r'[^\w\s]', '', lyrics.lower())
    tokens = cleaned_text.split()
    combined_stopwords = set(stopwords.words('spanish')).union(set(stopwords.words('english')))
    return [word for word in tokens if word not in combined_stopwords]

def extract_keywords_from_lyrics(lyrics):
    tokens = preprocess_lyrics(lyrics)
    word_counts = Counter(tokens)
    return word_counts.most_common(10)

def apply_clustering(data, n_clusters=5):
    clustering_model = KMeans(n_clusters=n_clusters)
    data['cluster'] = clustering_model.fit_predict(data[['energia']])
    return data, clustering_model
