import pandas as pd
import numpy as np
from pathlib import Path
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

# Incorporación de anomalías sintéticas
PROPORCION_ANOMALIAS = 0.01  #Seleccionamos aleatoriamente el 1% de las mediciones

n_anomalias = int(
    len(df_mediciones) * PROPORCION_ANOMALIAS
)

# Marcar todas las observaciones como normales
df_mediciones["es_anomalia"] = False

# Seleccionar observaciones aleatoriamente
indices_anomalos = rng.choice(
    df_mediciones.index,
    size=n_anomalias,
    replace=False
)

# Introducir valores anómalos de presión
df_mediciones.loc[indices_anomalos, "presion"] = 8.0  # Cambiamos su presión

# Marcar las observaciones alteradas
df_mediciones.loc[indices_anomalos, "es_anomalia"] = True

# Verificar mediciones generadas

print("\nPrimeras mediciones:")
print(df_mediciones.head())

print("\nTotal de mediciones:", len(df_mediciones))


# Verificar anomalías
print("\nResumen de anomalías:")
print(df_mediciones["es_anomalia"].value_counts())
print("\nPorcentaje de anomalías:")
print(df_mediciones["es_anomalia"].mean() * 100)




# Validación de la consistencia de los datos

# 1. Cantidad de sensores
print("\nSensores únicos:")
print(df_mediciones["sensor_id"].nunique())

# 2. Total de mediciones
print("\nTotal de mediciones:")
print(len(df_mediciones))

# 3. Mediciones por sensor
mediciones_por_sensor = df_mediciones.groupby(
    "sensor_id"
).size()

print("\nResumen de mediciones por sensor:")
print(mediciones_por_sensor.describe())

# 4. Valores faltantes
print("\nValores faltantes por variable:")
print(df_mediciones.isnull().sum())

# 5. Registros duplicados
duplicados = df_mediciones.duplicated(
    subset=["sensor_id", "timestamp"]
).sum()

print("\nRegistros duplicados:", duplicados)

# 6. Proporcion de anomalías
porcentaje_anomalias = (
    df_mediciones["es_anomalia"].mean() * 100
)

print("\nPorcentaje de anomalías:")
print(round(porcentaje_anomalias, 2))

# 7. Comprobaciones automáticas
assert df_mediciones["sensor_id"].nunique() == 1000
assert len(df_mediciones) == 1000000
assert mediciones_por_sensor.eq(1000).all()
assert not df_mediciones.isnull().any().any()
assert duplicados == 0
assert df_mediciones["es_anomalia"].sum() == 10000




# Exportación de datos a CSV

# Crear carpeta para los datos generados
carpeta_datos = Path("data")
carpeta_datos.mkdir(exist_ok=True)

# Exportar sensores
df_sensores.to_csv(
    carpeta_datos / "sensores.csv",
    index=False
)

# Exportar mediciones
df_mediciones.to_csv(
    carpeta_datos / "mediciones.csv",
    index=False
)
















