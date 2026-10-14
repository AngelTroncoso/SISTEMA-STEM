"""Genera datos de ejemplo para probar el sistema."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n_rows = 500
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 730)) for _ in range(n_rows)]

categorias = np.random.choice(['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Deportes'], n_rows)
regiones = np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Centro'], n_rows)

precios = []
for cat in categorias:
    if cat == 'Electrónica':
        precios.append(np.random.normal(500, 200))
    elif cat == 'Ropa':
        precios.append(np.random.normal(50, 20))
    elif cat == 'Alimentos':
        precios.append(np.random.normal(15, 5))
    elif cat == 'Hogar':
        precios.append(np.random.normal(120, 40))
    else:
        precios.append(np.random.normal(80, 30))

precios = np.maximum(precios, 1)
cantidades = np.random.poisson(3, n_rows) + 1
descuentos = np.random.beta(2, 5, n_rows) * 30

satisfaccion_base = np.random.normal(4, 0.8, n_rows)
satisfaccion = satisfaccion_base - descuentos * 0.02
satisfaccion = np.clip(satisfaccion, 1, 5)

df = pd.DataFrame({
    'fecha': dates,
    'categoria': categorias,
    'region': regiones,
    'precio': precios,
    'cantidad': cantidades,
    'descuento': descuentos,
    'satisfaccion': satisfaccion
})

df['ingreso_total'] = df['precio'] * df['cantidad'] * (1 - df['descuento'] / 100)

df.loc[df.sample(frac=0.05, random_state=42).index, 'satisfaccion'] = np.nan
df.loc[df.sample(frac=0.03, random_state=43).index, 'descuento'] = np.nan

outlier_idx = df.sample(frac=0.02, random_state=44).index
df.loc[outlier_idx, 'precio'] = df.loc[outlier_idx, 'precio'] * 5

df = df.sample(frac=1, random_state=45).reset_index(drop=True)

df.to_csv('sample_data.csv', index=False)
print(f"✓ Generado sample_data.csv: {len(df)} filas × {len(df.columns)} columnas")
print(f"  Columnas: {', '.join(df.columns.tolist())}")
print(f"  Nulos: {df.isnull().sum().sum()} valores")
