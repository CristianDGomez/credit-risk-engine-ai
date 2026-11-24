import time
import duckdb

inicio = time.time()

print("🔄 Analizando cartera activa y aging de cobranzas sobre 550.000 cuentas...")

reporte_cobranza = duckdb.sql("""
    WITH cartera_activa AS (
        SELECT
            rubro,
            facturacion_mensual_ars,
            deuda_sistema_ars,
            linea_solicitada_ars,
            dias_mora_max_12m,
            cheques_rechazados,
            ROUND((deuda_sistema_ars / NULLIF(facturacion_mensual_ars, 0)) * 100, 1) AS pct_uso_cupo
        FROM read_csv_auto('base_clientes_550k.txt', delim='\t')
        WHERE cheques_rechazados = 0
    )
    SELECT
        rubro,
        COUNT(*) AS cuentas_activas,
        SUM(CASE WHEN dias_mora_max_12m BETWEEN 1 AND 7 THEN 1 ELSE 0 END) AS alerta_preventiva_1_7d,
        SUM(CASE WHEN dias_mora_max_12m BETWEEN 8 AND 30 THEN 1 ELSE 0 END) AS gestion_mora_8_30d,
        SUM(CASE WHEN dias_mora_max_12m > 30 OR pct_uso_cupo >= 85 THEN 1 ELSE 0 END) AS bloqueo_despacho_preventivo,
        ROUND(SUM(CASE WHEN dias_mora_max_12m > 30 OR pct_uso_cupo >= 85 THEN deuda_sistema_ars ELSE 0 END) / 1000000, 1) AS capital_en_riesgo_millones_ars
    FROM cartera_activa
    GROUP BY rubro
    ORDER BY capital_en_riesgo_millones_ars DESC
""").df()

print(f"\n✅ Cartera auditada en {round(time.time() - inicio, 3)} segundos:\n")
print(reporte_cobranza.to_string(index=False))
