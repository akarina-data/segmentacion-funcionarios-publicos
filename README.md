# Segmentación de Funcionarios Públicos - Chile 2022

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)
[![CKAN API](https://img.shields.io/badge/API-datos.gob.cl-green.svg)](https://datos.gob.cl/)
[![CRISP-DM](https://img.shields.io/badge/Metodología-CRISP--DM-purple.svg)](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)

Proyecto de **clustering (aprendizaje no supervisado)** para segmentar funcionarios públicos a contrata de municipalidades chilenas.

> 📚 Proyecto desarrollado en el bootcamp **X-Academy** - "Data Science para la Industria Bancaria"

---

## Resultados

| Modelo | Silhouette | Clusters | Cobertura |
|--------|------------|----------|-----------|
| **K-Means** | **0.375** | 5 | 100% |
| DBSCAN | 0.283 | Variable | ~70% |
| OPTICS | -0.044 | Variable | ~60% |

### Segmentos Identificados

| # | Nombre | Descripción |
|---|--------|-------------|
| 0 | Nuevos ingresos | Baja antigüedad, baja renta |
| 1 | Estándar | Media antigüedad y renta |
| 2 | **Alta variación** | Variabilidad salarial sospechosa |
| 3 | Profesionales | Renta alta justificada |
| 4 | Veteranos | Alta antigüedad, renta estancada |

---

## Fuente de Datos: API datos.gob.cl

El proyecto conecta a la **API CKAN** del Portal de Datos Abiertos de Chile:

```python
# Endpoints utilizados
https://datos.gob.cl/api/3/action/package_search    # Buscar datasets
https://datos.gob.cl/api/3/action/package_show      # Metadata de dataset
https://datos.gob.cl/api/3/action/datastore_search  # Descargar datos
```

### Flujo de carga de datos:

```
┌─────────────────────────────────────┐
│  1. ¿Existe cache local?            │
│     → Sí: Cargar parquet            │
├─────────────────────────────────────┤
│  2. Conectar a API datos.gob.cl     │
│     → Buscar "funcionarios"         │
│     → Descargar CSV                 │
├─────────────────────────────────────┤
│  3. Fallback: datos sintéticos      │
│     → Si API no disponible          │
└─────────────────────────────────────┘
```

Para forzar conexión a la API (ignorar cache):
```python
df = loader.load_data(use_cache=False, force_api=True)
```

---

## Quickstart

```bash
# 1. Clonar
git clone https://github.com/akarina-data/segmentacion-funcionarios-publicos.git
cd segmentacion-funcionarios-publicos

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar notebook
jupyter notebook Segmentacion_Funcionarios_CRISPDM.ipynb

# 4. (Opcional) Demo interactiva
streamlit run app.py
```

---

## Estructura del Proyecto

```
segmentacion-funcionarios-publicos/
├── Segmentacion_Funcionarios_CRISPDM.ipynb   # Notebook principal
├── app.py                                      # Demo Streamlit
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                 # Datos de API (cache)
│   └── processed/           # Datos procesados
├── models/                  # Modelo entrenado
└── reports/                 # Gráficos
```

---

## Metodología CRISP-DM

| Fase | Contenido |
|------|-----------|
| 1. Business Understanding | Problema de transparencia en sector público |
| 2. Data Understanding | Conexión API + EDA + detección de outliers |
| 3. Data Preparation | Winsorización, log-transform, RobustScaler |
| 4. Modeling | K-Means vs DBSCAN vs OPTICS |
| 5. Evaluation | Métricas + interpretación de clusters |
| 6. Deployment | Exportación de artefactos |

---

## Variables del Modelo

| Variable | Descripción | Transformación |
|----------|-------------|----------------|
| `Remuneracion_bruta_mensualizada` | Sueldo bruto mensual (CLP) | Log-transform |
| `Antiguedad` | Años de servicio | - |
| `renta_2022_prom` | Promedio anual | Log-transform |
| `ratio_renta_prom_muni` | Renta / Promedio municipalidad | - |
| `ratio_renta_prom_cargo` | Renta / Promedio del cargo | - |
| `ratio_variacion_renta` | Variabilidad salarial | - |

---

## Decisiones Técnicas

| Decisión | Por qué |
|----------|---------|
| **API CKAN** | Datos oficiales actualizados del gobierno |
| **Winsorización** | Preserva registros, reduce outliers |
| **Log-transform** | Reduce asimetría de salarios |
| **RobustScaler** | Menos sensible a outliers |
| **Distancia Euclidiana** | Magnitud del sueldo SÍ importa |

---

## Limitaciones

⚠️ **Importante:**
- Clustering **NO detecta corrupción**, solo identifica patrones
- Si la API no responde, se usan datos sintéticos de demostración
- Resultados dependen de calidad de datos

---

## Tecnologías

`Python` `Pandas` `NumPy` `Scikit-learn` `Requests` `Matplotlib` `Seaborn` `Streamlit`

---

## Autor

**Ana Karina Muñoz** - [@akarina-data](https://github.com/akarina-data)

## Licencia

MIT
