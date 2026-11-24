import duckdb
import time

inicio = time.time()

resultado = duckdb.sql("""
    SELECT 
        rubro,
        COUNT(*) AS total_solicitudes,
        SUM(CASE WHEN cheques_rechazados >= 1 OR dias_mora_max_12m >= 60 THEN 1 ELSE 0 END) AS rechazados_automaticos,
        SUM(CASE WHEN cheques_rechazados = 0 AND dias_mora_max_12m <= 7 AND (deuda_sistema_ars + linea_solicitada_ars)/facturacion_mensual_ars <= 0.50 THEN 1 ELSE 0 END) AS aprobados_automaticos,
        SUM(CASE WHEN NOT (cheques_rechazados >= 1 OR dias_mora_max_12m >= 60) AND NOT (cheques_rechazados = 0 AND dias_mora_max_12m <= 7 AND (deuda_sistema_ars + linea_solicitada_ars)/facturacion_mensual_ars <= 0.50) THEN 1 ELSE 0 END) AS revision_manual_ia
    FROM read_csv_auto('base_clientes_550k.txt', delim='\t')
    GROUP BY rubro
    ORDER BY total_solicitudes DESC
""").df()

print(f"\n✅ 550.000 clientes evaluados en {round(time.time() - inicio, 3)} segundos:\n")
print(resultado.to_string(index=False))
