from os import environ
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
DEBUG=environ.get('DEBUG', False)
HOSTNAME=environ.get('HOSTNAME', 'http://localhost:8000')

# Rutas de archivos
ARCHIVO_DATASET=environ.get('ARCHIVO_DATASET', 'dataset.csv')
ARCHIVO_X_TRAIN=environ.get('ARCHIVO_X_TRAIN', 'X_train.csv')
ARCHIVO_X_TEST=environ.get('ARCHIVO_X_TEST', 'X_test.csv')
ARCHIVO_Y_TRAIN=environ.get('ARCHIVO_Y_TRAIN', 'y_train.csv')
ARCHIVO_Y_TEST=environ.get('ARCHIVO_Y_TEST', 'y_test.csv')
ARCHIVO_MODELO_RF=environ.get('ARCHIVO_MODELO_RF', 'rf_model.joblib')
ARCHIVO_MODELO_SVM=environ.get('ARCHIVO_MODELO_SVM', 'svm_model.joblib')
ARCHIVO_MODELO_RN=environ.get('ARCHIVO_MODELO_RN', 'nn_model.keras')
ARCHIVO_PREPROCESADOR=environ.get('ARCHIVO_PREPROCESADOR', 'preprocessor.joblib')

# Configuración de limpieza de datos
MIN_PRICE=int(environ.get('MIN_PRICE', 100000))
MAX_PRICE=int(environ.get('MAX_PRICE', 5000000))
MIN_SIZE_TERRAIN=int(environ.get('MIN_SIZE_TERRAIN', 0))
MAX_SIZE_TERRAIN=int(environ.get('MAX_SIZE_TERRAIN', 10000))
MIN_SIZE_CONSTRUCTION=int(environ.get('MIN_SIZE_CONSTRUCTION', 0))
MAX_SIZE_CONSTRUCTION=int(environ.get('MAX_SIZE_CONSTRUCTION', 1000))
MIN_ROOMS=int(environ.get('MIN_ROOMS', 0))
MAX_ROOMS=int(environ.get('MAX_ROOMS', 6))
MIN_BATHROOMS=int(environ.get('MIN_BATHROOMS', 1))
MAX_BATHROOMS=int(environ.get('MAX_BATHROOMS', 6))
MIN_PARKING=int(environ.get('MIN_PARKING', 0))
MAX_PARKING=int(environ.get('MAX_PARKING', 6))
MIN_AGE=int(environ.get('MIN_AGE', 0))
MAX_AGE=int(environ.get('MAX_AGE', 200))
MIN_LAT=float(environ.get('MIN_LAT', 19.1))
MAX_LAT=float(environ.get('MAX_LAT', 19.6))
MIN_LNG=float(environ.get('MIN_LNG', -99.4))
MAX_LNG=float(environ.get('MAX_LNG', -98.9))
TASA_CAMBIO_USD_MXN=float(environ.get('TASA_CAMBIO_USD_MXN', 20.0))

# Configuración de entrenamiento de modelos
RANDOM_STATE=int(environ.get('RANDOM_STATE', 42))
TEST_SIZE=float(environ.get('TEST_SIZE', 0.25))

# Lista de Alcaldías
municipalities = ['Alvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán', 'Cuajimalpa', 'Cuauhtémoc',
                  'Gustavo A. Madero', 'Iztacalco', 'Iztapalapa', 'Magdalena Contreras', 'Miguel Hidalgo',
                  'Milpa Alta', 'Tláhuac', 'Tlalpan', 'Venustiano Carranza', 'Xochimilco']
