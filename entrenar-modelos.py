# @Author: Humberto Alejandro Ortega Alcocer
# @Date: 2021-05-02
# @Description: Script para entrenar modelos de aprendizaje automático y guardarlos en archivos
# joblib y h5.
# @Usage: python entrenar-modelos.py
# @Output: Archivos rf_model.joblib, svm_model.joblib, nn_model.h5, preprocessor.joblib
# con los modelos entrenados y el preprocesador.
# @Dependencies: pandas, numpy, scikit-learn, tensorflow, joblib
# @Dataset: dataset.csv
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
#from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from joblib import dump
from constants import *
import numpy as np
from scikeras.wrappers import KerasRegressor
import keras as keras

print("Script de entrenamiento de modelos")
print("Cargando datos...")

# Cargar el dataset
df = pd.read_csv(ARCHIVO_DATASET)
print(f'Dimensiones del dataset: {df.shape}')

# Convertir aquellos precios en USD a pesos mexicanos usando la tasa de cambio en constants
df.loc[df['Currency'] == 'USD', 'Price'] *= TASA_CAMBIO_USD_MXN

# Convertir 'USD' a 'MN' en la columna 'Currency'
df.loc[df['Currency'] == 'USD', 'Currency'] = 'MN'
print(f'Valores únicos en Currency: \n{df["Currency"].unique()}')

# Eliminar filas duplicadas a partir de la columna 'ID'
df = df.drop_duplicates(subset='ID')
print(f'Dimensiones del dataset después de eliminar duplicados: {df.shape}')

# Eliminar columnas no numéricas
columnas_numericas = ['Price', 'Size_Terrain', 'Size_Construction', 'Rooms', 'Bathrooms', 'Parking', 'Age', 'Lat', 'Lng']
df = df[['Municipality',*columnas_numericas]]
print(f'Columnas después de eliminar columnas no numéricas: {df.columns}')

# Validar que Municipality sea una alcalía de la CDMX, o tratar de aproximarla, si no es posible, eliminar la fila
df = df[df['Municipality'].isin(municipalities)]
print(f'Dimensiones del dataset después de filtrar por alcaldías: {df.shape}')

# Sustituir infinitos por NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)
print(f'Valores nulos después de sustituir infinitos: \n{df.isnull().sum()}')

# Eliminar columnas no numéricas
for columna in columnas_numericas:
    df[columna] = pd.to_numeric(df[columna], errors='coerce')
print(f'Dimensiones del dataset después de eliminar columnas no numéricas: {df.shape}')

# Sustituir NaN por la media en columnas numéricas de baja cardinalidad
for columna in ['Rooms', 'Bathrooms', 'Parking']:
    if df[columna].isnull().sum() > 0:
        df[columna].fillna(df[columna].mean(), inplace=True)
print(f'Valores nulos después de sustituir NaN por la media: \n{df.isnull().sum()}')

# Eliminar filas con NaN
df.dropna(inplace=True)
print(f'Dimensiones del dataset después de eliminar NaN: {df.shape}')

# Algunos valores en 'Age' no corresponden a la antiguedad sino al año de construcción, identificarlos y corregirlos
year = pd.to_datetime('today').year
df['Age'] = df['Age'].apply(lambda x: year - x if x > 1000 else x)

# Filtrar filas que cumplen con los rangos deseados
df = df[
    (df['Price'] >= MIN_PRICE) & (df['Price'] <= MAX_PRICE) &
    (df['Size_Terrain'] >= MIN_SIZE_TERRAIN) & (df['Size_Terrain'] <= MAX_SIZE_TERRAIN) &
    (df['Size_Construction'] >= MIN_SIZE_CONSTRUCTION) & (df['Size_Construction'] <= MAX_SIZE_CONSTRUCTION) &
    (df['Rooms'] >= MIN_ROOMS) & (df['Rooms'] <= MAX_ROOMS) &
    (df['Bathrooms'] >= MIN_BATHROOMS) & (df['Bathrooms'] <= MAX_BATHROOMS) &
    (df['Parking'] >= MIN_PARKING) & (df['Parking'] <= MAX_PARKING) &
    (df['Age'] >= MIN_AGE) & (df['Age'] <= MAX_AGE) &
    (df['Lat'] >= MIN_LAT) & (df['Lat'] <= MAX_LAT) &
    (df['Lng'] >= MIN_LNG) & (df['Lng'] <= MAX_LNG)
]
print(f'Estadísticas después de aplicar límites:\n {df.describe()}')

# Esperar a que el usuario presione una tecla
input("Presiona una tecla para continuar...")

# Dividir el dataset en conjuntos de entrenamiento y prueba
X = df[['Municipality','Size_Terrain', 'Size_Construction', 'Rooms', 'Bathrooms', 'Parking', 'Age', 'Lat', 'Lng']]
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)
print(f'Dimensiones de los conjuntos de entrenamiento y prueba: {X_train.shape}, {X_test.shape}')

# Guardar los conjuntos de entrenamiento y prueba
X_train.to_csv(ARCHIVO_X_TRAIN, index=False)
X_test.to_csv(ARCHIVO_X_TEST, index=False)
y_train.to_csv(ARCHIVO_Y_TRAIN, index=False)
y_test.to_csv(ARCHIVO_Y_TEST, index=False)
print(f'Conjuntos de entrenamiento y prueba guardados en {ARCHIVO_X_TRAIN}, {ARCHIVO_X_TEST}, {ARCHIVO_Y_TRAIN}, {ARCHIVO_Y_TEST}')

# Crear un preprocesador para las columnas numéricas
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Obtener las columnas numéricas
numeric_features=columnas_numericas[1:]

# Crear un preprocesador para las columnas categóricas
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(categories=[municipalities]), ['Municipality']),
        ('num', numeric_transformer,numeric_features),
    ])

# Mensaje de inicio de entrenamiento
print("Entrenando modelos...")

# Redes Neuronales
print("Entrenando Red Neuronal...")

# Preprocesar los datos para la red neuronal
X_train_preprocessed = preprocessor.fit_transform(X_train)

## Crear una función que construya el modelo
#def build_nn_model(n_units=64, optimizer='adam', initializer='glorot_uniform', activation='relu'):
#    nn_model = Sequential()
#    nn_model.add(Input(shape=(X_train_preprocessed.shape[1],)))
#    nn_model.add(Dense(n_units, kernel_initializer=initializer, activation=activation))
#    nn_model.add(Dense(n_units, kernel_initializer=initializer, activation=activation))
#    nn_model.add(Dense(1, kernel_initializer=initializer))
#    #nn_model.compile(optimizer=optimizer, loss='mean_squared_error')
#    return nn_model
#
#
## Envolver el modelo Keras para que funcione con scikit-learn
#nn_keras = KerasRegressor(model=build_nn_model, loss='mse', n_units=64, optimizer='adam', initializer='glorot_uniform', activation='relu')
#
## Parámetros a buscar
##param_grid_nn = {
##    'batch_size': [50, 100, 150],
##    'epochs': [50, 100],
##    'model__n_units': [64, 128, 256],
##    'model__optimizer': ['adam', 'rmsprop']
##}
#param_grid_nn = {
#    'batch_size': [50],
#    'epochs': [50],
#    'model__n_units': [64],
#    'model__optimizer': ['adam'],
#    'model__initializer': ['glorot_uniform'],
#    'model__activation': ['relu'],
#    'loss': ['mse']
#}
#
## Crear el objeto GridSearchCV
#grid_search_nn = GridSearchCV(estimator=nn_keras, param_grid=param_grid_nn, cv=5, verbose=2,n_jobs=-1)

def get_reg(meta, hidden_layer_sizes, dropout):
    n_features_in_ = meta["n_features_in_"]
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=(n_features_in_,)))
    for hidden_layer_size in hidden_layer_sizes:
        model.add(keras.layers.Dense(hidden_layer_size, activation="relu"))
        model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Dense(1))
    return model

reg = KerasRegressor(
    model=get_reg,
    loss=keras.losses.MeanSquaredError,
    optimizer=keras.optimizers.Adam,
    metrics=[keras.metrics.R2Score],
    hidden_layer_sizes=(100,),
    dropout=0.5,
)

grid_search_nn = GridSearchCV(
    estimator=reg,
    param_grid={
        "hidden_layer_sizes": [(100,)],# (100, 100), (100, 100, 100)],
        "dropout": [0.5],# 0.7],
        # Now loss, batch size, epochs, optimizer, etc. can be specified as well
        "batch_size": [50],
        "epochs": [50],
        #"optimizer": [keras.optimizers.Adam],
        "optimizer__learning_rate": [0.1],#, 0.01, 0.001],
        #"loss": [keras.losses.MeanSquaredError],
        #"loss": ["mean_squared_error"],
        #"metrics": ["mean_squared_error"],
        #"metrics": [keras.metrics.MeanSquaredError],
        #"model__activation": ["relu", "tanh", "sigmoid"],
        #"model__initializer": ["glorot_uniform", "he_normal", "he_uniform"],
    },
    refit=False,
    cv=5,
    verbose=2,
    n_jobs=-1,
)

# Debido a que el preprocesamiento ya está hecho, podemos usar X_train_preprocessed directamente aquí
grid_search_nn.fit(X_train_preprocessed, y_train)

# Obtener los mejores parámetros
mejores_parametros = grid_search_nn.best_params_

# Imprimir los mejores Parámetros
print(f"\t- Mejores parámetros: {mejores_parametros}")

# Entrenar el modelo con los mejores parámetros
nn_model = reg.set_params(**mejores_parametros)
nn_model.fit(X_train_preprocessed, y_train)

print("Modelo Red Neuronal entrenado")

# Random Forest
print("Entrenando Random Forest...")
# Crear el pipeline
rf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('regressor', RandomForestRegressor(random_state=42, oob_score=True))])

# Parámetros a buscar
param_grid_rf = {
    'regressor__n_estimators': [100, 500, 1000],
    'regressor__max_depth': [None, 10, 20, 30],
    'regressor__min_samples_split': [2, 5, 10]
}

# Crear el objeto GridSearchCV
grid_search_rf = GridSearchCV(rf_pipeline, param_grid=param_grid_rf, cv=5, verbose=2, n_jobs=-1)

# Ejecutar la búsqueda
grid_search_rf.fit(X_train, y_train)

# Obtener el mejor modelo
rf_pipeline = grid_search_rf.best_estimator_

# Imprimir los mejores parámetros
print(f"\t- Mejores parámetros: {grid_search_rf.best_params_}")
print("Modelo Random Forest entrenado")

# Máquina de Soporte Vectorial
print("Entrenando SVM...")
# Crear el pipeline
svm_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('svr', SVR())])

# Parámetros a buscar
param_grid_svm = {
    'svr__C': [0.1, 1, 100, 1000],
    'svr__gamma': ['scale', 'auto', 0.01, 0.001],
    'svr__epsilon': [0.01, 0.1, 1]
}

# Crear el objeto GridSearchCV
grid_search_svm = GridSearchCV(svm_pipeline, param_grid=param_grid_svm, cv=5, verbose=2, n_jobs=-1)

# Ejecutar la búsqueda
grid_search_svm.fit(X_train, y_train)

# Obtener el mejor modelo
svm_pipeline = grid_search_svm.best_estimator_

# Imprimir los mejores parámetros
print(f"\t- Mejores parámetros: {grid_search_svm.best_params_}")
print("Modelo SVM entrenado")

# Guardar los modelos
print("Guardando modelos...")
dump(rf_pipeline, ARCHIVO_MODELO_RF)
dump(svm_pipeline, ARCHIVO_MODELO_SVM)
nn_model.save(ARCHIVO_MODELO_RN)
dump(preprocessor, ARCHIVO_PREPROCESADOR)
print(f"Modelos guardados en archivos {ARCHIVO_MODELO_RF}, {ARCHIVO_MODELO_SVM}, {ARCHIVO_MODELO_RN}, {ARCHIVO_PREPROCESADOR}")

# Validar los modelos e imprimir sus resultados
def validate_model(model, X, y, name):
    predictions = model.predict(X)
    mae = mean_absolute_error(y, predictions)
    print(f'\t- MAE de {name}: {mae}')

print("Validando modelos...")
validate_model(rf_pipeline, X_test, y_test, 'Random Forest')
validate_model(svm_pipeline, X_test, y_test, 'SVM')
validate_model(nn_model, preprocessor.transform(X_test), y_test, 'Red Neuronal')
print("Modelos validados")

# Fin del script
print("Fin del script")