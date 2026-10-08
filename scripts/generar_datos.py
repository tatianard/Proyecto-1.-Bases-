import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parámetros del proyecto
NUM_SENSORES = 1000
NUM_ZONAS = 20

# Generación de sensores
sensores = []

for i in range(NUM_SENSORES):
    sensor = {
        'sensor_id': f'S{i+1:04d}',
        'zona_id': f'Z{(i % NUM_ZONAS) + 1:02d}',
    }
    sensores.append(sensor)

# Conversión a DataFrame
df_sensores = pd.DataFrame(sensores)    

# Resultados
print(df_sensores.head())
print(f"\nTotal de sensores: {len(df_sensores)}")
print("\nSensores por zona:")
print(df_sensores["zona_id"].value_counts().sort_index())






# Generación de mediciones
NUM_MEDICIONES = 1000
SEMILLA = 42

rng = np.random.default_rng(SEMILLA)
fecha_inicio = datetime(2026, 1, 1)

mediciones = []

for sensor in sensores:

    for j in range(NUM_MEDICIONES):

        medicion = {
            "sensor_id": sensor["sensor_id"],
            "zona_id": sensor["zona_id"],
            "timestamp": fecha_inicio + timedelta(hours=j),
            "caudal": round(rng.normal(12, 2), 2),
            "presion": round(rng.normal(3.5, 0.4), 2),
            "temperatura": round(rng.normal(24, 2), 2),
            "calidad": 1
        }

        mediciones.append(medicion)

df_mediciones = pd.DataFrame(mediciones)

print("\nPrimeras mediciones:")
print(df_mediciones.head())

print("\nTotal de mediciones:", len(df_mediciones))























