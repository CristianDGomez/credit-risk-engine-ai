import os
import pandas as pd
from google import genai

client = genai.Client()
df_revision = pd.read_csv("casos_revision_ia.csv")
caso = df_revision.iloc[0].to_dict()

prompt = f"""
Actúa como un Analista Senior de Riesgo Crediticio Comercial. 
Evalúa la siguiente solicitud que cayó en zona de revisión manual y emite un dictamen técnico breve (máximo 4 líneas) indicando:
1. Riesgo principal detectado.
2. Recomendación (Aprobar con límite reducido, pedir garantía o rechazar).

Datos del solicitante:
{caso}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

print(f"--- DICTAMEN IA PARA CLIENTE #{int(caso['cliente_id'])} ---")
print(response.text)
