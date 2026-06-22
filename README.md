# HypertrophIA — Parcial 3

**ITY1101 Gestión de Datos para IA**  
Predicción de riesgo de lesión en series de entrenamiento usando variables del pipeline.

## Estructura del proyecto

```
hypertrophia-p3/
├── data/
│   ├── generate_dataset.py    ← generación sintética del dataset gold
│   └── gold/
│       └── hypertrophia.db    ← dataset listo para entrenar
├── 3.1_modelo/
│   └── modelo_lesion.ipynb    ← notebook: EDA + modelos + métricas
├── .venv/                     ← entorno virtual
└── requirements.txt           ← dependencias
```

## Dataset

Dataset sintético de registros de entrenamiento con ~17.000 series etiquetadas con **lesión (0/1)**.  
Tasa de lesión: ~31%. Variables predictoras: RPE, peso levantado, edad, dificultad, volumen, etc.

## Modelos

- **Regresión Logística** con regularización L1 (Lasso) y L2 (Ridge)
- **Random Forest** con 150 árboles, profundidad máxima 12

## Resultados esperados

| Modelo | AUC | Gini |
|--------|-----|------|
| Random Forest | ~0.735 | ~0.470 |
| Logistic Regression (L2) | ~0.741 | ~0.481 |

## Uso

```bash
# Crear y activar entorno virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Generar dataset
python data/generate_dataset.py

# Abrir notebook
# 3.1_modelo/modelo_lesion.ipynb
```

## Créditos

Proyecto académico — ITY1101 Gestión de Datos para IA.
