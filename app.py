"""Aplicación Streamlit: Analista Multiagente STEM - UI Futurista."""
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

from utils.loader import load_data_file, get_excel_sheets, sample_large_dataframe
from utils.llm import LLMEnhancer
from agents.orchestrator import Orchestrator
from ui.theme import inject_css, get_plotly_template, AGENT_COLORS, COLORS
from ui.components import hero_banner, agent_card, metric_card, section_title, badge, steps_guide

st.set_page_config(
    page_title="SISTEMA-STEM · Analista Multiagente",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS
inject_css()

# Inicializar session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        'Tecnología': 'idle',
        'Matemáticas': 'idle',
        'Ciencia': 'idle',
        'Ingeniería': 'idle'
    }

# Sidebar
st.sidebar.markdown(f"<h2 style='color: {COLORS['accent_cyan']}; font-family: Orbitron;'>⚙️ Configuración</h2>", 
                    unsafe_allow_html=True)

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

# Configuración de IA
st.sidebar.markdown("---")
st.sidebar.markdown(f"<h3 style='color: {COLORS['accent_violet']}; font-family: Orbitron;'>🤖 IA Generativa</h3>", 
                    unsafe_allow_html=True)

use_ai = st.sidebar.checkbox("Activar Gemini 3", value=False)
api_key = None

if use_ai:
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="GEMINI_API_KEY o GOOGLE_API_KEY"
    )
    
    if api_key:
        llm = LLMEnhancer(api_key=api_key)
        if st.sidebar.button("🔌 Probar conexión"):
            success, message = llm.test_connection()
            if success:
                st.sidebar.success(f"✅ {message}")
            else:
                st.sidebar.error(f"❌ {message}")

# Main content
if st.session_state.df is None:
    # Pantalla de inicio
    hero_banner()
    
    # Tarjetas de agentes
    st.markdown(f"<h3 style='text-align: center; color: {COLORS['text_primary']}; "
                f"font-family: Orbitron; margin: 3rem 0 2rem 0;'>Nuestros Agentes Especializados</h3>",
                unsafe_allow_html=True)
    
    cols = st.columns(4)
    with cols[0]:
        agent_card("Ciencia", "science_icon.svg", "Formula y contrasta hipótesis científicas", "idle")
    with cols[1]:
        agent_card("Tecnología", "tech_icon.svg", "Evalúa calidad técnica de datos", "idle")
    with cols[2]:
        agent_card("Ingeniería", "eng_icon.svg", "Limpia datos y entrena modelos ML", "idle")
    with cols[3]:
        agent_card("Matemáticas", "math_icon.svg", "Análisis estadístico profundo", "idle")
    
    # Guía de pasos
    steps_guide()
    
    # Botón de ejemplo
    if not uploaded_file:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎲 Probar con Datos de Ejemplo", use_container_width=True):
                if Path("sample_data.csv").exists():
                    st.session_state.df = pd.read_csv("sample_data.csv")
                    st.session_state.results = None
                    st.rerun()
                else:
                    st.error("Ejecuta: python generate_sample.py")

# Cargar datos
if uploaded_file and st.session_state.df is None:
    try:
        with st.spinner("Cargando datos..."):
            df = load_data_file(uploaded_file, sheet_name)
            df, was_sampled = sample_large_dataframe(df)
            st.session_state.df = df
            st.session_state.results = None
            
            if was_sampled:
                st.warning("⚠️ Dataset muy grande. Se muestrearon 100,000 filas.")
            st.rerun()
                
    except Exception as e:
        st.error(f"❌ Error al cargar archivo: {str(e)}")
        st.stop()

if st.session_state.df is not None:
    df = st.session_state.df
    
    # Selector de variable objetivo
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    target_col = None
    if numeric_cols:
        target_col_opt = st.sidebar.selectbox(
            "Variable objetivo (opcional)",
            ["Automático"] + numeric_cols,
            help="Para el modelo de ML"
        )
        target_col = None if target_col_opt == "Automático" else target_col_opt
    
    # Vista previa
    section_title("📊 Vista Previa de Datos", COLORS['accent_cyan'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Filas", f"{len(df):,}", COLORS['accent_cyan'])
    with col2:
        metric_card("Columnas", str(len(df.columns)), COLORS['accent_violet'])
    with col3:
        mem_mb = df.memory_usage(deep=True).sum() / 1024**2
        metric_card("Memoria", f"{mem_mb:.1f} MB", COLORS['accent_magenta'])
    
    st.dataframe(df.head(50), use_container_width=True)
    
    # Botón de análisis
    if st.button("🚀 Iniciar Análisis STEM", type="primary", use_container_width=False):
        # Preparar LLM si está activo
        llm = LLMEnhancer(api_key=api_key) if use_ai and api_key else None
        
        orchestrator = Orchestrator()
        
        # Contenedor para estado de agentes
        status_container = st.container()
        progress_bar = st.progress(0)
        
        with status_container:
            cols = st.columns(4)
            status_placeholders = {
                'Tecnología': cols[0].empty(),
                'Matemáticas': cols[1].empty(),
                'Ciencia': cols[2].empty(),
                'Ingeniería': cols[3].empty()
            }
        
        def update_status(agent_name, status):
            st.session_state.agent_status[agent_name] = status
            icon_map = {
                'Tecnología': 'tech_icon.svg',
                'Matemáticas': 'math_icon.svg',
                'Ciencia': 'science_icon.svg',
                'Ingeniería': 'eng_icon.svg'
            }
            desc_map = {
                'Tecnología': 'Calidad de datos',
                'Matemáticas': 'Estadística',
                'Ciencia': 'Hipótesis',
                'Ingeniería': 'Modelado ML'
            }
            with status_placeholders[agent_name]:
                agent_card(agent_name, icon_map[agent_name], desc_map[agent_name], status)
        
        def progress_callback(agent_name, current, total):
            update_status(agent_name, 'analyzing')
            progress = (current + 1) / total
            progress_bar.progress(progress)
        
        with st.spinner("Analizando datos con agentes STEM..."):
            results = orchestrator.run_analysis(df, target_col, progress_callback)
            
            # Mejorar resúmenes con IA si está disponible
            if llm and llm.enabled:
                for branch, result in results.items():
                    if not result.error:
                        result.summary = llm.enhance_summary(
                            result.agent_name,
                            result.findings,
                            result.metrics
                        )
            
            # Aplicar template de plotly a todas las figuras
            plot_template = get_plotly_template()
            for result in results.values():
                if not result.error:
                    for fig in result.figures:
                        fig.update_layout(**plot_template['layout'])
            
            st.session_state.results = results
            
            # Actualizar estados finales
            for agent_name, result in results.items():
                status = 'error' if result.error else 'done'
                update_status(agent_name, status)
        
        progress_bar.empty()
        st.success("✅ Análisis completado")
        st.rerun()

    # Mostrar resultados
    if st.session_state.results:
        results = st.session_state.results
        
        section_title("📈 Resultados del Análisis", COLORS['accent_cyan'])
        
        tabs = st.tabs(["🔬 Ciencia", "💻 Tecnología", "⚙️ Ingeniería", "📐 Matemáticas", "📋 Informe Final"])
        
        # Función auxiliar para mostrar resultados
        def show_agent_result(result, color):
            if result.error:
                st.error(f"❌ Error: {result.error}")
            else:
                # Resumen
                st.markdown(f"""
                <div class="glass-card fade-in" style="border-color: {color};">
                    <p style="font-size: 1.1rem; line-height: 1.6; color: {COLORS['text_primary']};">
                        {result.summary}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Métricas
                if result.metrics:
                    st.markdown(f"<h4 style='color: {color}; margin-top: 2rem;'>📊 Métricas</h4>", 
                                unsafe_allow_html=True)
                    cols = st.columns(min(4, len(result.metrics)))
                    for i, (key, value) in enumerate(result.metrics.items()):
                        with cols[i % len(cols)]:
                            metric_card(key, str(value), color)
                
                # Hallazgos
                if result.findings:
                    st.markdown(f"<h4 style='color: {color}; margin-top: 2rem;'>🔍 Hallazgos</h4>", 
                                unsafe_allow_html=True)
                    for finding in result.findings:
                        st.markdown(f"<div style='margin: 0.5rem 0;'>"
                                    f"<span style='color: {color};'>●</span> "
                                    f"<span style='color: {COLORS['text_primary']};'>{finding}</span>"
                                    f"</div>", unsafe_allow_html=True)
                
                # Visualizaciones
                if result.figures:
                    st.markdown(f"<h4 style='color: {color}; margin-top: 2rem;'>📈 Visualizaciones</h4>", 
                                unsafe_allow_html=True)
                    for fig in result.figures:
                        st.plotly_chart(fig, use_container_width=True)
                
                # Advertencias
                if result.warnings:
                    st.markdown(f"<h4 style='color: {COLORS['accent_magenta']}; margin-top: 2rem;'>⚠️ Advertencias</h4>", 
                                unsafe_allow_html=True)
                    for warning in result.warnings:
                        st.warning(warning)
                
                # Recomendaciones
                if result.recommendations:
                    st.markdown(f"<h4 style='color: {COLORS['accent_green']}; margin-top: 2rem;'>💡 Recomendaciones</h4>", 
                                unsafe_allow_html=True)
                    for rec in result.recommendations:
                        st.markdown(badge(rec), unsafe_allow_html=True)
        
        # Tab Ciencia
        with tabs[0]:
            result = results.get('Ciencia')
            if result:
                show_agent_result(result, COLORS['accent_violet'])
        
        # Tab Tecnología
        with tabs[1]:
            result = results.get('Tecnología')
            if result:
                show_agent_result(result, COLORS['accent_cyan'])
        
        # Tab Ingeniería
        with tabs[2]:
            result = results.get('Ingeniería')
            if result:
                show_agent_result(result, COLORS['accent_magenta'])
        
        # Tab Matemáticas
        with tabs[3]:
            result = results.get('Matemáticas')
            if result:
                show_agent_result(result, COLORS['accent_green'])
        
        # Tab Informe Final
        with tabs[4]:
            section_title("📋 Informe Ejecutivo STEM", COLORS['accent_cyan'])
            
            orchestrator = Orchestrator()
            report = orchestrator.generate_executive_report(results)
            
            # Resumen en tarjeta destacada
            st.markdown(f"""
            <div class="glass-card fade-in" style="border-color: {COLORS['accent_cyan']}; 
                 box-shadow: 0 8px 32px {COLORS['glow_cyan']};">
                <h3 style="color: {COLORS['accent_cyan']}; font-family: 'Orbitron', sans-serif;">
                    📝 Resumen General
                </h3>
                <p style="font-size: 1.1rem; line-height: 1.8; color: {COLORS['text_primary']};">
                    {report['summary']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Puntaje de calidad (gauge)
            tech_result = results.get('Tecnología')
            if tech_result and not tech_result.error:
                quality_score = tech_result.metrics.get('Calidad de datos', 0)
                
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=quality_score,
                    title={'text': "Calidad de Datos", 
                           'font': {'size': 20, 'family': 'Orbitron', 'color': COLORS['accent_cyan']}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': COLORS['text_secondary']},
                        'bar': {'color': COLORS['accent_cyan']},
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(255, 43, 214, 0.2)'},
                            {'range': [50, 80], 'color': 'rgba(139, 92, 246, 0.2)'},
                            {'range': [80, 100], 'color': 'rgba(57, 255, 136, 0.2)'}
                        ],
                        'threshold': {
                            'line': {'color': COLORS['accent_green'], 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(**get_plotly_template()['layout'])
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Hallazgos clave
            if report['key_findings']:
                st.markdown(f"<h3 style='color: {COLORS['accent_violet']}; font-family: Orbitron; "
                            f"margin-top: 2rem;'>🎯 Hallazgos Clave</h3>", unsafe_allow_html=True)
                for finding in report['key_findings']:
                    st.markdown(f"<div style='margin: 0.75rem 0;'>"
                                f"<span style='color: {COLORS['accent_violet']};'>▶</span> "
                                f"<span style='color: {COLORS['text_primary']};'>{finding}</span>"
                                f"</div>", unsafe_allow_html=True)
            
            # Advertencias
            if report['warnings']:
                st.markdown(f"<h3 style='color: {COLORS['accent_magenta']}; font-family: Orbitron; "
                            f"margin-top: 2rem;'>⚠️ Riesgos y Advertencias</h3>", unsafe_allow_html=True)
                for warning in report['warnings']:
                    st.warning(warning)
            
            # Recomendaciones
            if report['recommendations']:
                st.markdown(f"<h3 style='color: {COLORS['accent_green']}; font-family: Orbitron; "
                            f"margin-top: 2rem;'>💡 Recomendaciones Prioritarias</h3>", unsafe_allow_html=True)
                for rec in report['recommendations']:
                    st.markdown(badge(rec), unsafe_allow_html=True)
            
            # Próximos pasos
            st.markdown(f"<h3 style='color: {COLORS['accent_cyan']}; font-family: Orbitron; "
                        f"margin-top: 2rem;'>🚀 Próximos Pasos</h3>", unsafe_allow_html=True)
            for step in report['next_steps']:
                st.markdown(f"<div style='margin: 0.5rem 0;'>"
                            f"<span style='color: {COLORS['accent_cyan']};'>→</span> "
                            f"<span style='color: {COLORS['text_primary']};'>{step}</span>"
                            f"</div>", unsafe_allow_html=True)
            
            # Botón de descarga
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
                mime="text/markdown",
                use_container_width=True
            )
