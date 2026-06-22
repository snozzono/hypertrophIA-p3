import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
DB_PATH = Path("data/gold/hypertrophia.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. EJERCICIOS
# ============================================================
ejercicios_data = [
    (1, "Sentadilla", "Cuádriceps", "Piernas", "Compuesto", "Barra", 85, 4),
    (2, "Press Banca", "Pectoral Mayor", "Pecho", "Compuesto", "Barra", 90, 3),
    (3, "Peso Muerto", "Isquiotibiales", "Piernas", "Compuesto", "Barra", 95, 5),
    (4, "Dominada", "Dorsal Ancho", "Espalda", "Compuesto", "Barra", 80, 4),
    (5, "Press Militar", "Deltoides Anterior", "Hombros", "Compuesto", "Barra", 75, 3),
    (6, "Remo con Barra", "Dorsal Ancho", "Espalda", "Compuesto", "Barra", 80, 3),
    (7, "Curl Bíceps", "Bíceps Braquial", "Brazos", "Aislamiento", "Mancuerna", 60, 2),
    (8, "Extensión Tríceps", "Tríceps Braquial", "Brazos", "Aislamiento", "Mancuerna", 55, 2),
    (9, "Elevación Lateral", "Deltoides Lateral", "Hombros", "Aislamiento", "Mancuerna", 40, 2),
    (10, "Femoral Acostado", "Isquiotibiales", "Piernas", "Aislamiento", "Máquina", 65, 2),
    (11, "Extensión Cuádriceps", "Cuádriceps", "Piernas", "Aislamiento", "Máquina", 65, 2),
    (12, "Press Piernas", "Cuádriceps", "Piernas", "Compuesto", "Máquina", 85, 3),
    (13, "Remo Polea Baja", "Dorsal Ancho", "Espalda", "Compuesto", "Máquina", 75, 3),
    (14, "Pullover", "Pectoral Mayor", "Pecho", "Aislamiento", "Mancuerna", 50, 2),
    (15, "Aperturas", "Pectoral Mayor", "Pecho", "Aislamiento", "Mancuerna", 45, 2),
    (16, "Prensa Hombros", "Deltoides Anterior", "Hombros", "Compuesto", "Máquina", 70, 3),
    (17, "Curl Femoral", "Isquiotibiales", "Piernas", "Aislamiento", "Máquina", 55, 2),
    (18, "Remo Alta", "Trapecio", "Espalda", "Aislamiento", "Barra", 60, 3),
    (19, "Sentadilla Búlgara", "Cuádriceps", "Piernas", "Compuesto", "Mancuerna", 70, 4),
    (20, "Fondos", "Tríceps Braquial", "Brazos", "Compuesto", "Paralelas", 75, 4),
]

df_ejercicios = pd.DataFrame(ejercicios_data,
    columns=["id_ejercicio", "nombre_ejercicio", "nombre_musculo",
             "nombre_grupo_muscular", "nombre_tipo_ejercicio",
             "nombre_equipamiento", "porcentaje_estimulo", "dificultad"])

# ============================================================
# 2. USUARIOS — perfiles variados con distintos niveles de riesgo
# ============================================================
N_USUARIOS = 80
paises = ["Chile", "Argentina", "Perú", "Colombia", "México", "España"]
sexos = ["Masculino", "Femenino"]

# Perfiles de riesgo base por usuario
perfiles_lesion = np.random.beta(2, 5, N_USUARIOS)
perfiles_lesion = (perfiles_lesion - perfiles_lesion.min()) / (perfiles_lesion.max() - perfiles_lesion.min())

usuarios = []
for uid in range(1, N_USUARIOS + 1):
    sexo = np.random.choice(sexos, p=[0.6, 0.4])
    if sexo == "Masculino":
        peso = round(np.random.normal(78, 10), 1)
        estatura = round(np.random.normal(175, 7), 1)
    else:
        peso = round(np.random.normal(62, 9), 1)
        estatura = round(np.random.normal(162, 6), 1)
    peso = np.clip(peso, 45, 150)
    estatura = np.clip(estatura, 140, 200)

    edad = int(np.clip(np.random.normal(30, 8), 18, 65))

    usuarios.append({
        "id_usuario": uid,
        "nombre_usuario": f"Usuario_{uid}",
        "correo_electronico": f"usuario{uid}@email.com",
        "nombre_sexo": sexo,
        "nombre_pais": np.random.choice(paises),
        "peso_corporal_kg": peso,
        "estatura_cm": estatura,
        "edad": edad,
        "riesgo_base": round(float(perfiles_lesion[uid - 1]), 4),
        "fecha_registro": f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,28):02d}"
    })

df_usuarios = pd.DataFrame(usuarios)

# ============================================================
# 3. RUTINAS, SESIONES, REGISTROS
# ============================================================
N_SESIONES = 1200
enfoques = ["Fuerza", "Hipertrofia", "Resistencia", "Potencia"]
ejercicios_por_enfoque = {
    "Fuerza": [(1, 4, 5), (2, 4, 5), (3, 3, 5), (5, 4, 5)],
    "Hipertrofia": [(1, 3, 12), (2, 3, 12), (4, 3, 10), (7, 3, 15), (8, 3, 15)],
    "Resistencia": [(12, 3, 20), (13, 3, 20), (11, 3, 20), (10, 3, 20)],
    "Potencia": [(1, 5, 3), (3, 5, 3), (20, 5, 5)],
}

registros = []
rid = 1

for sesion_id in range(1, N_SESIONES + 1):
    uid = np.random.randint(1, N_USUARIOS + 1)
    enfoque = np.random.choice(enfoques)
    user = df_usuarios.iloc[uid - 1]
    edad = int(user["edad"])
    peso_corporal = float(user["peso_corporal_kg"])
    riesgo_base = float(user["riesgo_base"])

    fecha_creacion = f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,28):02d}"
    fecha_sesion = pd.to_datetime(fecha_creacion) + pd.Timedelta(days=np.random.randint(0, 60))

    duracion = int(np.clip(np.random.normal(55, 15), 20, 120))

    ej_rutina = ejercicios_por_enfoque[enfoque]
    for orden, (id_ej, series, reps_plan) in enumerate(ej_rutina, 1):
        ej_row = df_ejercicios[df_ejercicios["id_ejercicio"] == id_ej].iloc[0]
        dificultad = int(ej_row["dificultad"])
        pct_estimulo = int(ej_row["porcentaje_estimulo"])

        for nserie in range(1, series + 1):
            rpe_base = 3 + dificultad * 0.8 + nserie * 0.5 + np.random.normal(0, 1)
            rpe = int(np.clip(round(rpe_base), 1, 10))

            peso_ej = peso_corporal * (pct_estimulo / 100) * np.random.uniform(0.8, 1.2)
            peso_ej = round(np.clip(peso_ej, 5, 300), 1)

            fatiga = max(0, (rpe - 5) * 0.1)
            reps_logradas = max(1, int(reps_plan * (1 - fatiga * np.random.uniform(0, 0.5))))

            registros.append({
                "id_registro_serie": rid,
                "id_sesion": sesion_id,
                "id_ejercicio": id_ej,
                "numero_serie": nserie,
                "repeticiones_logradas": reps_logradas,
                "peso_levantado_kg": peso_ej,
                "rpe": rpe,
                "id_usuario": uid,
                "edad": edad,
                "peso_corporal_kg": peso_corporal,
                "riesgo_base": riesgo_base,
                "nombre_enfoque": enfoque,
                "duracion_minutos": int(duracion),
                "dificultad": dificultad,
                "porcentaje_estimulo": pct_estimulo,
                "cantidad_series": series,
                "cantidad_repeticiones": reps_plan,
                "orden_ejercicio": orden,
                "fecha_sesion": fecha_sesion.strftime("%Y-%m-%d"),
            })
            rid += 1

df_registros = pd.DataFrame(registros)

# ============================================================
# 4. GENERAR VARIABLE OBJETIVO: lesion (0/1)
#    Modelo logístico con señal fuerte y realista
# ============================================================
# Factores de riesgo modelados:
#   - RPE alto: más esfuerzo → más riesgo
#   - Peso relativo (peso_levantado / peso_corporal): cargas pesadas → más riesgo
#   - Volumen de la serie: fatiga acumulada
#   - Edad: mayor edad → mayor riesgo
#   - Dificultad del ejercicio: ejercicios complejos → más riesgo
#   - Número de serie: fatiga acumulada en la sesión
#   - Riesgo base del usuario: susceptibilidad individual

def prob_lesion(row):
    peso_rel = row["peso_levantado_kg"] / max(row["peso_corporal_kg"], 1)

    volumen = row["repeticiones_logradas"] * row["peso_levantado_kg"]

    duracion_riesgo = (row["duracion_minutos"] - 45) / 30

    z = (
        -9.5
        + 0.50 * row["rpe"]
        + 1.50 * peso_rel
        + 0.002 * volumen
        + 0.03 * row["edad"]
        + 0.30 * row["dificultad"]
        + 0.15 * row["numero_serie"]
        + 0.30 * duracion_riesgo
        + 2.00 * row["riesgo_base"]
    )
    return 1 / (1 + np.exp(-z))

df_registros["prob_lesion"] = df_registros.apply(prob_lesion, axis=1)
df_registros["lesion"] = (np.random.random(len(df_registros)) < df_registros["prob_lesion"]).astype(int)

print(f"Total registros generados: {len(df_registros)}")
print(f"Distribución lesion: 0={df_registros['lesion'].value_counts().get(0, 0)}, "
      f"1={df_registros['lesion'].value_counts().get(1, 0)}")
print(f"Tasa de lesion: {df_registros['lesion'].mean():.2%}")
print(f"Probabilidad promedio de lesion: {df_registros['prob_lesion'].mean():.2%}")

# ============================================================
# 5. ESCRIBIR SQLITE
# ============================================================
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(str(DB_PATH))

df_ejercicios.to_sql("ejercicio", conn, index=False, if_exists="replace")
df_usuarios.drop(columns=["riesgo_base"]).to_sql("usuario", conn, index=False, if_exists="replace")

columnas_gold = [
    "id_registro_serie", "id_usuario", "id_sesion", "id_ejercicio",
    "numero_serie", "repeticiones_logradas", "peso_levantado_kg", "rpe",
    "dificultad", "porcentaje_estimulo",
    "cantidad_series", "cantidad_repeticiones", "orden_ejercicio",
    "duracion_minutos", "edad", "peso_corporal_kg", "lesion"
]

df_gold = df_registros[columnas_gold]
df_gold.to_sql("gold", conn, index=False, if_exists="replace")

conn.close()
print(f"\nBase SQLite guardada en: {DB_PATH}")
print(f"Tabla gold: {len(df_gold)} filas, {len(columnas_gold)-1} features + target 'lesion'")
