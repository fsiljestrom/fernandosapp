
# trainer.py
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd

# predictor.py
def predict_genre(model, year, month, categories):
    season = (month % 12 + 3) // 3
    prediction = model.predict([[year, month, season]])
    
    # Convertir el código de predicción a género usando las categorías
    genre = categories[prediction[0]]
    return genre


def train_genre_model(df):
    X = df[['year', 'month', 'season']]
    y = df['genre_encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print("Precisión del modelo:", accuracy)
    
    return model
'''
def prepare_data_for_energy_model(df):
    df['season'] = df['month'].apply(lambda x: (x % 12 + 3) // 3)
    return df[['year', 'month', 'season', 'genre', 'energy']]

def train_energy_model(df):
    X = df[['year', 'month', 'season', 'genre']]
    y = df['energy']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = pd.get_dummies(X_train, columns=['genre'])
    X_test = pd.get_dummies(X_test, columns=['genre'])
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Precisión del modelo de energía:", model.score(X_test, y_test))
    return model

'''