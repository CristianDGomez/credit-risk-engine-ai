import pandas as pd
import numpy as np
import time

print("Generando 500,000 registros de operaciones crediticias...")
inicio = time.time()

np.random.seed(42)
n_registros = 500_000

df = pd.DataFrame({
    "cliente_id": np.arange(100000, 100000 + n_registros),
    "segmento": np.random.choice(
        ["Flota Transporte", "Taller Mecánico", "Consumidor Final", "Distribuidor"],
        n_registros,
        p=[0.25, 0.20, 0.45, 0.10]
    ),
    "antiguedad_meses": np.random.randint(1, 120, n_registros),
    "facturacion_mensual_usd": np.round(np.random.lognormal(mean=8.2, sigma=0.9, size=n_registros), 2),
    "deuda_actual_usd": np.round(np.random.exponential(scale=1800, size=n_registros), 2),
    "dias_mora_max_12m": np.random.choice([0, 5, 15, 30, 60, 90], n_registros, p=[0.55, 0.15, 0.12, 0.08, 0.06, 0.04]),
    "cheques_rechazados": np.random.choice([0, 1, 2, 3], n_registros, p=[0.88, 0.08, 0.03, 0.01]),
    "monto_solicitado_usd": np.round(np.random.uniform(500, 15000, n_registros), 2)
})

df.to_parquet("cartera_clientes_500k.parquet", index=False)
print(f"Archivo Parquet generado en {round(time.time() - inicio, 2)} segundos.")
