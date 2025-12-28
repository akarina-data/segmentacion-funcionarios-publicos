"""
Demo Streamlit - Segmentación de Funcionarios Públicos
======================================================
Ejecutar con: streamlit run app.py

Si no hay datos procesados, genera datos de ejemplo automáticamente.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import joblib

# Configuración
st.set_page_config(
    page_title="Segmentación Funcionarios",
    page_icon="📊",
    layout="wide"
)

# Rutas
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "kmeans_funcionarios.joblib"
DATA_PATH = BASE_DIR / "data" / "processed" / "funcionarios_segmentados.parquet"


def generate_demo_data(n=1000):
    """Genera datos de ejemplo si no existen los datos procesados."""
    np.random.seed(42)
    
    clusters_config = {
        0: {'remu': (450000, 80000), 'ant': (0.5, 0.3), 'var': 0.05, 'nombre': 'Nuevos ingresos'},
        1: {'remu': (900000, 150000), 'ant': (3, 1), 'var': 0.10, 'nombre': 'Estándar'},
        2: {'remu': (1100000, 200000), 'ant': (4, 2), 'var': 0.35, 'nombre': 'Alta variación'},
        3: {'remu': (2200000, 400000), 'ant': (5, 2), 'var': 0.08, 'nombre': 'Profesionales'},
        4: {'remu': (750000, 100000), 'ant': (8, 3), 'var': 0.05, 'nombre': 'Veteranos'}
    }
    
    probs = [0.25, 0.35, 0.15, 0.10, 0.15]
    clusters = np.random.choice(list(clusters_config.keys()), n, p=probs)
    
    data = []
    for c in clusters:
        cfg = clusters_config[c]
        data.append({
            'Remuneracion': np.clip(np.random.normal(*cfg['remu']), 350000, 5000000),
            'Antiguedad': np.clip(np.random.normal(*cfg['ant']), 0.1, 30),
            'Variacion': np.random.uniform(cfg['var'] - 0.05, cfg['var'] + 0.15),
            'cluster': c,
            'cluster_nombre': cfg['nombre']
        })
    
    return pd.DataFrame(data)


def load_data():
    """Carga datos procesados o genera demo."""
    if DATA_PATH.exists():
        df = pd.read_parquet(DATA_PATH)
        return df, "procesados"
    else:
        return generate_demo_data(), "demo"


# ===== INTERFAZ =====

st.title("📊 Segmentación de Funcionarios Públicos")
st.caption("Chile 2022 | K-Means Clustering | CRISP-DM")

# Cargar datos
df, source = load_data()

if source == "demo":
    st.info("📌 Mostrando **datos de demostración**. Ejecuta el notebook para ver resultados reales.")

# Métricas
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Total Funcionarios", f"{len(df):,}")
col2.metric("Clusters", df['cluster'].nunique())
col3.metric("Fuente", "Notebook" if source == "procesados" else "Demo")

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Visualización", "📊 Distribución", "📋 Datos"])

with tab1:
    st.subheader("Remuneración vs Antigüedad")
    
    # Detectar columnas
    remu_col = 'Remuneracion_bruta_mensualizada' if 'Remuneracion_bruta_mensualizada' in df.columns else 'Remuneracion'
    ant_col = 'Antiguedad'
    color_col = 'cluster_nombre' if 'cluster_nombre' in df.columns else 'cluster'
    
    fig = px.scatter(
        df, x=ant_col, y=remu_col, color=color_col,
        labels={ant_col: 'Antigüedad (años)', remu_col: 'Remuneración (CLP)'},
        height=500, opacity=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Funcionarios por Cluster")
        counts = df['cluster'].value_counts().sort_index()
        fig_bar = px.bar(x=counts.index, y=counts.values, 
                         labels={'x': 'Cluster', 'y': 'Cantidad'})
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("Proporción")
        if 'cluster_nombre' in df.columns:
            fig_pie = px.pie(df, names='cluster_nombre')
        else:
            fig_pie = px.pie(df, names='cluster')
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("Muestra de Datos")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Descarga
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", csv, "funcionarios_segmentados.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("Desarrollado por Ana Karina Muñoz | [GitHub](https://github.com/akarina-data)")
