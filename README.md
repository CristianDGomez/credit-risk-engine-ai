# 🏦 Motor de Evaluación Crediticia de Alto Caudal con IA (`credit-risk-engine-ai`)

Pipeline analítico diseñado para procesar, limpiar y evaluar **500.000 solicitudes de crédito comercial** en menos de 1 segundo utilizando **Python + DuckDB (SQL)**, integrando **Gemini IA** como copiloto analítico para redactar dictámenes de riesgo en operaciones de zona gris.

---

### 🎯 Problema de Negocio que Resuelve

En empresas comerciales, distribuidoras y entidades financieras, evaluar manualmente miles de solicitudes de cuenta corriente o líneas de crédito genera cuellos de botella operativos y aumenta el riesgo de morosidad. 

Este proyecto demuestra una arquitectura híbrida en 3 etapas:
1. **Ingesta Masiva (Big Data Local):** Generación y almacenamiento columnar en formato `.parquet` de **500.000 registros** de clientes (flotas, talleres, distribuidores y consumidores finales).
2. **Motor de Scoring en SQL / DuckDB:** Evaluación vectorizada en milisegundos aplicando reglas de negocio (ratio de endeudamiento, historial de mora a 12 meses, cheques rechazados y antigüedad comercial).
3. **Copiloto de Riesgo con IA (Gemini API):** Automatización del análisis cualitativo únicamente para los casos que caen en *revisión manual*, optimizando costos de API y tiempo del analista.

---

### 🏗️ Arquitectura del Pipeline

```text
[ 1_generador_datos.py ] ──▶ cartera_clientes_500k.parquet (500.000 filas)
                                      │
                                      ▼
[ 2_motor_scoring_sql.py ] ──▶ DuckDB Engine (< 0.5 seg)
                                      │
                 ┌────────────────────┼────────────────────┐
                 ▼                    ▼                    ▼
       APROBADO AUTOMÁTICO   RECHAZADO AUTOMÁTICO   REVISIÓN ANALISTA IA
                                                           │
                                                           ▼
                                              [ 3_analista_ia_gemini.py ]
                                                           │
                                                           ▼
                                               Dictamen Técnico Ejecutivo

### 4. Alerta Preventiva de Cobranza y Control de Exposición (`4_alerta_cobranza_preventiva.py`)
Módulo de monitoreo continuo diseñado para auditar carteras masivas (550.000+ registros) en milisegundos utilizando consultas analíticas en **DuckDB** sin saturar la memoria RAM.

* **Segmentación de Mora Temprana:** Clasifica automáticamente las cuentas activas según su comportamiento de pago (`1 a 7 días` para alerta preventiva y `8 a 30 días` para gestión de cobranza activa).
* **Bloqueo Preventivo de Despacho:** Identifica cuentas con mora superior a 30 días o con un uso del cupo crediticio igual o mayor al **85%**, permitiendo frenar nuevos despachos antes de que se agrave el incobrable.
* **Cuantificación de Capital en Riesgo:** Agrupa por rubro comercial y calcula en tiempo real el capital total expuesto (en millones de ARS), priorizando los sectores críticos para la toma de decisiones del área de créditos y cobranzas.
