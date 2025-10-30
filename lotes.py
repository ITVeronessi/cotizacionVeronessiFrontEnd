import pandas as pd
import requests
import time
import os

# === CONFIGURACIÓN ===
API_URL = "https://cotizacionveronessi.onrender.com/medicamentos"  # tu endpoint FastAPI
EXCEL_FILE = r"C:\Users\ale_d\Documents\Veronessi\Medic.xlsx"
CSV_FILE = "Medic.csv"

# === 1️⃣ Convertir Excel a CSV ===
if not os.path.exists(EXCEL_FILE):
    print(f"⚠️ No se encontró el archivo {EXCEL_FILE}")
    exit()

print("📄 Convirtiendo Excel a CSV...")
df = pd.read_excel(EXCEL_FILE)
df.to_csv(CSV_FILE, index=False)
print(f"✅ Archivo CSV generado: {CSV_FILE}")

# === 2️⃣ Leer CSV y enviar uno por uno a la API ===
print("🚀 Enviando datos a la API...")

# Solo las columnas que tu modelo espera
data = pd.read_csv(CSV_FILE, usecols=["nombremedicamento", "precio"]).to_dict(orient="records")

total = len(data)
success, errors = 0, 0

for i, row in enumerate(data, start=1):
    try:
        response = requests.post(API_URL, json=row)
        if response.status_code in [200, 201]:
            print(f"✅ ({i}/{total}) Registro insertado correctamente")
            success += 1
        else:
            print(f"❌ ({i}/{total}) Error {response.status_code}: {response.text}")
            errors += 1
        time.sleep(0.1)
    except Exception as e:
        print(f"⚠️ ({i}/{total}) Error inesperado: {e}")
        errors += 1

print("\n🎯 Proceso completado.")
print(f"✅ Registros exitosos: {success}")
print(f"❌ Registros con error: {errors}")
