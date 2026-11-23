import duckdb
import time

inicio = time.time()
con = duckdb.connect()

query = """
WITH metricas_riesgo AS (
    SELECT 
        cliente_id,
        segmento,
        antiguedad_meses,
        facturacion_mensual_usd,
        deuda_actual_usd,
        dias_mora_max_12m,
        cheques_rechazados,
        monto_solicitado_usd,
        ROUND((deuda_actual_usd + monto_solicitado_usd) / NULLIF(facturacion_mensual_usd, 0), 2) AS ratio_endeudamiento,
        (1000 
         - (dias_mora_max_12m * 4) 
         - (cheques_rechazados * 150) 
         - CASE WHEN (deuda_actual_usd / NULLIF(facturacion_mensual_usd, 0)) > 0.6 THEN 180 ELSE 0 END
         + CASE WHEN antiguedad_meses > 24 THEN 80 ELSE 0 END
        ) AS score_crediticio
    FROM 'cartera_clientes_500k.parquet'
)
SELECT 
    *,
    CASE 
        WHEN cheques_rechazados >= 2 OR dias_mora_max_12m >= 60 THEN 'RECHAZADO_AUTOMATICO'
        WHEN score_crediticio >= 750 AND ratio_endeudamiento <= 0.50 THEN 'APROBADO_AUTOMATICO'
        ELSE 'REVISION_ANALISTA_IA'
    END AS dictamen_motor
FROM metricas_riesgo
"""

df_resultado = con.execute(query).df()
tiempo_total = round(time.time() - inicio, 3)

print(f"500,000 solicitudes evaluadas en {tiempo_total} segundos.\n")
print("Distribución de dictámenes:")
print(df_resultado["dictamen_motor"].value_counts())

casos_revision = df_resultado[df_resultado["dictamen_motor"] == "REVISION_ANALISTA_IA"].head(10)
casos_revision.to_csv("casos_revision_ia.csv", index=False)
