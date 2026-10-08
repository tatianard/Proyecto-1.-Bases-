import pandas as pd

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


