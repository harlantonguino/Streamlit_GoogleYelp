
# importar librerias
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

import streamlit as st

st.write("""
# Deploy Modelo de Clasificacion 
## sklearn LinearSVC
""")

# get data
df = pd.read_parquet('Cluster_result.parquet')

# Seleccionar variables predictoras X - variable a predecir y
X = df['review processed']
y = df['cluster']

# obtener datos de entrenamiento - datos de prueba (split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1, stratify=y)

# pipeline
from sklearn.pipeline import Pipeline
clf_model = Pipeline([('tfidf_v', TfidfVectorizer(ngram_range=(1, 1))), ('clf_m', LinearSVC(C=2, loss='squared_hinge'))])

# entrenar modelo
clf_model.fit(X_train, y_train)

# evaluar modelo
pred_test = clf_model.predict(X_test)

from sklearn.metrics import accuracy_score

print('Exactitud:', accuracy_score(y_test, pred_test))

# test
index = X_test.index[897]
review = df['review processed'][index]
st.write('review a evaluar: ', review)

result = clf_model.predict([review])[0]
if result == 0:
    st.write('### Resultado de la Clasificacion: ', '## Conocedor')
else:
    st.write('### Resultado de la Clasificacion: ', '## Consumidor Casual')