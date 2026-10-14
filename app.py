"""Aplicación Streamlit: Analista Multiagente STEM."""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

from utils.loader import load_data_file, get_excel_sheets, sample_large_dataframe
from agents.orchestrator import Orchestrator

st.set_page_config(
    page_title="Analista Multiagente STEM",
    page_icon="🔬",
    layout="wide"
)

# Inicializar session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_clean' not in st.session_state:
    st.session_state.df_clean = None

# Sidebar
st.sidebar.title("⚙️ Configuración")

uploaded_file = st.sidebar.file_uploader(
    "Sube tu archivo",
    type=['csv', 'xlsx', 'xls'],
    help="Formatos: CSV, XLS, XLSX (máx 200 MB)"
)

sheet_name = None
if uploaded_file and Path(uploaded_file.name).suffix.lower() in ['.xlsx', '.xls']:
    sheets = get_excel_sheets(uploaded_file)
    if len(sheets) > 1:
        sheet_name = st.sidebar.selectbox("Selecciona hoja", sheets)
    else:
        sheet_name = sheets[0] if sheets else None

# Opción de usar datos de ejemplo
if not uploaded_file:
    if st.sidebar.button("🎲 Probar con datos de ejemplo"):
        if Path("sample_data.csv").exists():
            st.session_state.df = pd.read_csv("sample_data.csv")
            st.session_state.results = None
            st.rerun()
        else:
            st.sidebar.error("Ejecuta primero: python generate_sample.py")

target_col = None
use_ai = st.sidebar.checkbox("🤖 Usar IA (opcional)", value=False)
api_key = None

if use_ai:
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Opcional: mejora los resúmenes con IA"
    )

# Main content
st.title("🔬 Analista Multiagente STEM")
st.markdown("Sistema de análisis de datos con 4 agentes especializados: Tecnología, Matemáticas, Ciencia e Ingeniería")

# Cargar datos
if uploaded_file:
    try:
        with st.spinner("Cargando datos..."):
            df = load_data_file(uploaded_file, sheet_name)
            df, was_sampled = sample_large_dataframe(df)
            st.session_state.df = df
            st.session_state.results = None
            
            if was_sampled:
                st.warning("⚠️ Dataset muy grande. Se muestrearon 100,000 filas para el análisis.")
                
    except Exception as e:
        st.error(f"❌ Error al cargar archivo: {str(e)}")
        st.stop()

if st.session_state.df is not None:
    df = st.session_state.df
    
    # Selector de variable objetivo
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        target_col = st.sidebar.selectbox(
            "Variable objetivo (opcional)",
            ["Automático"] + numeric_cols,
            help="Para el modelo de ML"
        )
        if target_col != "Automático":
            target_col = target_col
        else:
            target_col = None
    
    # Vista previa
    st.subheader("📊 Vista Previa de Datos")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Filas", f"{len(df):,}")
    with col2:
        st.metric("Columnas", len(df.columns))
    with col3:
        st.metric("Memoria", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    st.dataframe(df.head(50), use_container_width=True)
    
    # Botón de análisis
    if st.button("🚀 Iniciar Análisis STEM", type="primary"):
        orchestrator = Orchestrator()
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def progress_callback(agent_name, current, total):
            progress = (current + 1) / total
            progress_bar.progress(progress)
            status_text.text(f"Ejecutando agente: {agent_name}...")
        
        with st.spinner("Analizando datos con agentes STEM..."):
            results = orchestrator.run_analysis(df, target_col, progress_callback)
            st.session_state.results = results
            
            # Guardar df_clean si existe
            for branch, result in results.items():
                if hasattr(result, 'error') and not result.error:
                    continue
        
        progress_bar.empty()
        status_text.empty()
        st.success("✅ Análisis completado")
        st.rerun()

    # Mostrar resultados
    if st.session_state.results:
        results = st.session_state.results
        
        tabs = st.tabs(["🔬 Ciencia", "💻 Tecnología", "⚙️ Ingeniería", "📐 Matemáticas", "📋 Informe Final"])
        
        # Tab Ciencia
        with tabs[0]:
            result = results.get('Ciencia')
            if result:
                if result.error:
                    st.error(f"Error: {result.error}")
                else:
                    st.markdown(f"### {result.agent_name}")
                    st.info(result.summary)
                    
                    if result.findings:
                        st.markdown("#### 🔍 Hipótesis Contrastadas")
                        for finding in result.findings:
                            st.markdown(finding)
                    
                    if result.metrics:
                        st.markdown("#### 📊 Métricas")
                        cols = st.columns(len(result.metrics))
                        for i, (key, value) in enumerate(result.metrics.items()):
                            cols[i].metric(key, value)
                    
                    if result.figures:
                        st.markdown("#### 📈 Visualizaciones")
                        for fig in result.figures:
                            st.plotly_chart(fig, use_container_width=True)
                    
                    if result.warnings:
                        st.markdown("#### ⚠️ Advertencias")
                        for warning in result.warnings:
                            st.warning(warning)
                    
                    if result.recommendations:
                        st.markdown("#### 💡 Recomendaciones")
                        for rec in result.recommendations:
                            st.markdown(f"- {rec}")
        
        # Tab Tecnología
        with tabs[1]:
            result = results.get('Tecnología')
            if result:
                if result.error:
                    st.error(f"Error: {result.error}")
                else:
                    st.markdown(f"### {result.agent_name}")
                    st.info(result.summary)
                    
                    if result.metrics:
                        st.markdown("#### 📊 Métricas Técnicas")
                        cols = st.columns(min(4, len(result.metrics)))
                        for i, (key, value) in enumerate(result.metrics.items()):
                            cols[i % len(cols)].metric(key, value)
                    
                    if result.findings:
                        st.markdown("#### 🔍 Hallazgos")
                        for finding in result.findings:
                            st.markdown(f"- {finding}")
                    
                    if result.figures:
                        st.markdown("#### 📈 Visualizaciones")
                        for fig in result.figures:
                            st.plotly_chart(fig, use_container_width=True)
                    
                    if result.warnings:
                        st.markdown("#### ⚠️ Advertencias")
                        for warning in result.warnings:
                            st.warning(warning)
                    
                    if result.recommendations:
                        st.markdown("#### 💡 Recomendaciones")
                        for rec in result.recommendations:
                            st.markdown(f"- {rec}")

        # Tab Ingeniería
        with tabs[2]:
            result = results.get('Ingeniería')
            if result:
                if result.error:
                    st.error(f"Error: {result.error}")
                else:
                    st.markdown(f"### {result.agent_name}")
                    st.info(result.summary)
                    
                    if result.metrics:
                        st.markdown("#### 📊 Métricas del Modelo")
                        cols = st.columns(min(4, len(result.metrics)))
                        for i, (key, value) in enumerate(result.metrics.items()):
                            cols[i % len(cols)].metric(key, value)
                    
                    if result.findings:
                        st.markdown("#### 🔍 Hallazgos")
                        for finding in result.findings:
                            st.markdown(f"- {finding}")
                    
                    if result.figures:
                        st.markdown("#### 📈 Visualizaciones")
                        for fig in result.figures:
                            st.plotly_chart(fig, use_container_width=True)
                    
                    if result.warnings:
                        st.markdown("#### ⚠️ Advertencias")
                        for warning in result.warnings:
                            st.warning(warning)
                    
                    if result.recommendations:
                        st.markdown("#### 💡 Recomendaciones")
                        for rec in result.recommendations:
                            st.markdown(f"- {rec}")
        
        # Tab Matemáticas
        with tabs[3]:
            result = results.get('Matemáticas')
            if result:
                if result.error:
                    st.error(f"Error: {result.error}")
                else:
                    st.markdown(f"### {result.agent_name}")
                    st.info(result.summary)
                    
                    if result.metrics:
                        st.markdown("#### 📊 Estadísticas")
                        cols = st.columns(min(5, len(result.metrics)))
                        for i, (key, value) in enumerate(result.metrics.items()):
                            cols[i % len(cols)].metric(key, value)
                    
                    if result.findings:
                        st.markdown("#### 🔍 Hallazgos Estadísticos")
                        for finding in result.findings:
                            st.markdown(finding)
                    
                    if result.figures:
                        st.markdown("#### 📈 Visualizaciones")
                        for fig in result.figures:
                            st.plotly_chart(fig, use_container_width=True)
                    
                    if result.warnings:
                        st.markdown("#### ⚠️ Advertencias")
                        for warning in result.warnings:
                            st.warning(warning)
                    
                    if result.recommendations:
                        st.markdown("#### 💡 Recomendaciones")
                        for rec in result.recommendations:
                            st.markdown(f"- {rec}")

        # Tab Informe Final
        with tabs[4]:
            st.markdown("### 📋 Informe Ejecutivo STEM")
            
            orchestrator = Orchestrator()
            report = orchestrator.generate_executive_report(results)
            
            st.markdown("#### 📝 Resumen General")
            st.info(report['summary'])
            
            if report['key_findings']:
                st.markdown("#### 🎯 Hallazgos Clave (Top 5)")
                for finding in report['key_findings']:
                    st.markdown(f"- {finding}")
            
            if report['warnings']:
                st.markdown("#### ⚠️ Riesgos y Advertencias")
                for warning in report['warnings']:
                    st.warning(warning)
            
            if report['recommendations']:
                st.markdown("#### 💡 Recomendaciones Prioritarias")
                for rec in report['recommendations']:
                    st.markdown(f"- {rec}")
            
            st.markdown("#### 🚀 Próximos Pasos")
            for step in report['next_steps']:
                st.markdown(f"- {step}")
            
            # Descargar informe
            report_md = f"""# Informe Ejecutivo STEM

## Resumen General
{report['summary']}

## Hallazgos Clave
{chr(10).join(['- ' + f for f in report['key_findings']])}

## Advertencias
{chr(10).join(['- ' + w for w in report['warnings']])}

## Recomendaciones
{chr(10).join(['- ' + r for r in report['recommendations']])}

## Próximos Pasos
{chr(10).join(['- ' + s for s in report['next_steps']])}
"""
            st.download_button(
                label="📥 Descargar Informe (Markdown)",
                data=report_md,
                file_name="informe_stem.md",
                mime="text/markdown"
            )

else:
    st.info("👈 Sube un archivo CSV/Excel en la barra lateral o prueba con datos de ejemplo")
