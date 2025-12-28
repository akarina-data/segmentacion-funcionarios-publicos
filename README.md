# Segmentación de Funcionarios Públicos a Contrata - Chile 2022

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Demo-red.svg)](https://streamlit.io/)
[![CRISP-DM](https://img.shields.io/badge/Metodología-CRISP--DM-purple.svg)](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)

## Descripción

Proyecto de **aprendizaje no supervisado (clustering)** para segmentar funcionarios públicos a contrata de municipalidades chilenas. El objetivo es identificar grupos homogéneos que permitan análisis exploratorio y priorización de revisiones.

> **Nota:** Este proyecto fue desarrollado en el bootcamp **X-Academy** ("Data Science para la Industria Bancaria") y está documentado siguiendo la metodología CRISP-DM.

---

## Resultados Principales

| Modelo | Silhouette Score | Clusters | Cobertura |
|--------|------------------|----------|-----------|
| **K-Means** | **0.375** | 5 | 100% |
| DBSCAN | 0.283 | Variable | ~70% |
| OPTICS | -0.044 | Variable | ~60% |

### Segmentos Identificados

| Cluster | Descripción | % |
|---------|-------------|---|
| 0 | Baja antigüedad y baja renta | ~25% |
| 1 | Media antigüedad y renta | ~35% |
| 2 | Alta variación de renta | ~15% |
| 3 | Renta alta (profesionales/jefaturas) | ~10% |
| 4 | Mayor antigüedad, renta estancada | ~15% |

---

## Quickstart

### 1. Clonar e instalar dependencias

```bash
git clone https://github.com/akarina-data/segmentacion-funcionarios-publicos.git
cd segmentacion-funcionarios-publicos

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### 2. Ejecutar el notebook

```bash
jupyter notebook Segmentacion_Funcionarios_Publicos_CRISPDM.ipynb
```

Ejecutar **Kernel → Restart & Run All** para garantizar reproducibilidad.

### 3. Ejecutar demo interactiva (Streamlit)

```bash
streamlit run app.py
```

---

## Metodología CRISP-DM

```
┌─────────────────────────────────────────────────────────────┐
│  1. Business Understanding                                   │
│     └── Problema: transparencia en sector público            │
├─────────────────────────────────────────────────────────────┤
│  2. Data Understanding                                       │
│     └── EDA, detección de outliers, análisis de distribución│
├─────────────────────────────────────────────────────────────┤
│  3. Data Preparation                                         │
│     ├── Winsorización de outliers (percentiles 1-99)        │
│     ├── Log-transform para variables asimétricas            │
│     └── RobustScaler para estandarización                   │
├─────────────────────────────────────────────────────────────┤
│  4. Modeling                                                 │
│     └── Comparación: K-Means vs DBSCAN vs OPTICS            │
├─────────────────────────────────────────────────────────────┤
│  5. Evaluation                                               │
│     └── Silhouette, Calinski-Harabasz, Davies-Bouldin       │
├─────────────────────────────────────────────────────────────┤
│  6. Deployment                                               │
│     └── Modelo exportado + Demo Streamlit                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Estructura del Proyecto

```
segmentacion-funcionarios-publicos/
├── Segmentacion_Funcionarios_Publicos_CRISPDM.ipynb  # Notebook principal
├── app.py                          # Demo interactiva (Streamlit)
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                        # Datos originales (no versionados)
│   └── processed/                  # Datos procesados (no versionados)
├── models/
│   └── kmeans_funcionarios.joblib  # Modelo entrenado (generado por notebook)
└── reports/
    └── *.png                       # Gráficos generados
```

> **Nota:** Los directorios `data/`, `models/` y `reports/` se generan al ejecutar el notebook. No se versionan en Git (ver `.gitignore`).

---

## Variables del Modelo

| Variable | Descripción | Transformación |
|----------|-------------|----------------|
| `Remuneracion_bruta_mensualizada` | Sueldo bruto mensual (CLP) | Log-transform |
| `Antiguedad` | Años de servicio | - |
| `renta_2022_prom` | Promedio anual del funcionario | Log-transform |
| `ratio_renta_prom_muni` | Renta / Promedio municipalidad | - |
| `ratio_renta_prom_cargo` | Renta / Promedio del cargo | - |
| `ratio_variacion_renta` | (Max - Min) / Promedio | - |

---

## Decisiones Técnicas

### ¿Por qué Winsorización (no eliminar outliers)?
- Reduce impacto de valores extremos sin perder registros
- Importante cuando necesitas cobertura completa (todos los funcionarios)

### ¿Por qué Log-transform?
- Las remuneraciones tienen distribución asimétrica (cola derecha)
- Reduce skewness, mejorando el rendimiento de K-Means

### ¿Por qué distancia Euclidiana (no Coseno)?
- La magnitud importa: $1M ≠ $3M de sueldo
- Coseno ignora magnitud, solo mide "dirección" del vector

---

## Limitaciones y Consideraciones

⚠️ **Importante:**

1. **Clustering NO detecta corrupción**: Solo identifica grupos/patrones. Cualquier uso para auditoría requiere validación adicional y contexto.

2. **Datos sintéticos**: Si la API de datos.gob.cl no está disponible, el notebook genera datos sintéticos realistas para demostración.

3. **Reproducibilidad**: Los resultados dependen de la calidad de datos y decisiones de preprocesamiento.

---

## Skills Demostradas

### Data Analyst Jr
- EDA completo con visualizaciones
- Control de calidad de datos
- Comunicación de hallazgos

### Data Scientist Jr
- Pipeline CRISP-DM end-to-end
- Preprocesamiento robusto (outliers, transformaciones)
- Comparación de algoritmos con métricas

### Data Engineer Jr
- Proyecto reproducible con estructura estándar
- Exportación de artefactos (modelo, datos, reportes)
- Demo desplegable con Streamlit

---

## Tecnologías

- **Python 3.9+**
- **Pandas / NumPy** - Manipulación de datos
- **Scikit-learn** - Algoritmos de ML
- **Matplotlib / Seaborn** - Visualización
- **SciPy** - Estadísticas
- **Streamlit** - Demo interactiva

---

## Autor

**Ana Karina Muñoz**
- GitHub: [@akarina-data](https://github.com/akarina-data)
- LinkedIn: [Ana Karina Muñoz](https://linkedin.com/in/anakarinamunoz)

---

## Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.
