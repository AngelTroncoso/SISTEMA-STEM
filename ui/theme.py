"""Tema futurista cyberpunk para la aplicación."""
import streamlit as st

# Paleta de colores
COLORS = {
    'bg_dark': '#0A0E1A',
    'bg_medium': '#11162B',
    'bg_card': 'rgba(17, 22, 43, 0.6)',
    'border': 'rgba(0, 229, 255, 0.3)',
    'accent_cyan': '#00E5FF',
    'accent_violet': '#8B5CF6',
    'accent_magenta': '#FF2BD6',
    'accent_green': '#39FF88',
    'text_primary': '#E8EAF6',
    'text_secondary': '#B0B4C5',
    'glow_cyan': 'rgba(0, 229, 255, 0.4)',
    'glow_violet': 'rgba(139, 92, 246, 0.4)',
    'glow_magenta': 'rgba(255, 43, 214, 0.4)',
    'glow_green': 'rgba(57, 255, 136, 0.4)',
}

# Colores por agente
AGENT_COLORS = {
    'Ciencia': COLORS['accent_violet'],
    'Tecnología': COLORS['accent_cyan'],
    'Ingeniería': COLORS['accent_magenta'],
    'Matemáticas': COLORS['accent_green'],
    'Arte': '#FFA726',  # Naranja artístico
}

AGENT_GLOWS = {
    'Ciencia': COLORS['glow_violet'],
    'Tecnología': COLORS['glow_cyan'],
    'Ingeniería': COLORS['glow_magenta'],
    'Matemáticas': COLORS['glow_green'],
    'Arte': 'rgba(255, 167, 38, 0.4)',
}


def inject_css():
    """Inyecta CSS futurista en la aplicación."""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');
    
    /* Variables globales */
    :root {{
        --bg-dark: {COLORS['bg_dark']};
        --bg-medium: {COLORS['bg_medium']};
        --accent-cyan: {COLORS['accent_cyan']};
        --accent-violet: {COLORS['accent_violet']};
        --accent-magenta: {COLORS['accent_magenta']};
        --accent-green: {COLORS['accent_green']};
    }}
    
    /* Fondo degradado */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg_dark']} 0%, {COLORS['bg_medium']} 100%);
        font-family: 'Inter', sans-serif;
        color: {COLORS['text_primary']};
    }}
    
    /* Títulos */
    h1, h2, h3 {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 0.05em;
    }}
    
    /* Tarjetas glass */
    .glass-card {{
        background: {COLORS['bg_card']};
        backdrop-filter: blur(10px);
        border: 1px solid {COLORS['border']};
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        border-color: {COLORS['accent_cyan']};
        box-shadow: 0 8px 32px {COLORS['glow_cyan']};
        transform: translateY(-2px);
    }}
    
    /* Botones */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['accent_cyan']} 0%, {COLORS['accent_violet']} 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-family: 'Orbitron', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 15px {COLORS['glow_cyan']};
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 6px 25px {COLORS['glow_cyan']}, 0 0 20px {COLORS['glow_violet']};
        transform: translateY(-2px);
    }}
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-family: 'Orbitron', sans-serif;
        color: {COLORS['text_secondary']};
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        border-color: {COLORS['accent_cyan']};
        color: {COLORS['accent_cyan']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['accent_cyan']}22 0%, {COLORS['accent_violet']}22 100%);
        border-color: {COLORS['accent_cyan']};
        color: {COLORS['accent_cyan']};
        box-shadow: 0 0 15px {COLORS['glow_cyan']};
    }}
    
    /* Métricas */
    [data-testid="stMetricValue"] {{
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['accent_cyan']};
        text-shadow: 0 0 10px {COLORS['glow_cyan']};
    }}
    
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif;
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
    }}
    
    /* Barra de progreso */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {COLORS['accent_cyan']} 0%, {COLORS['accent_magenta']} 100%);
        box-shadow: 0 0 10px {COLORS['glow_cyan']};
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['bg_dark']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {COLORS['accent_cyan']} 0%, {COLORS['accent_violet']} 100%);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['accent_cyan']};
    }}
    
    /* Animaciones */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.6; }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    /* Respetar preferencias de movimiento reducido */
    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['bg_dark']} 0%, {COLORS['bg_medium']} 100%);
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Info boxes */
    .stAlert {{
        background: {COLORS['bg_card']};
        backdrop-filter: blur(10px);
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        color: {COLORS['text_primary']};
    }}
    
    /* Dataframe */
    [data-testid="stDataFrame"] {{
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        overflow: hidden;
    }}
    
    /* Download button */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {COLORS['accent_green']} 0%, {COLORS['accent_cyan']} 100%);
    }}
    
    .stDownloadButton > button:hover {{
        box-shadow: 0 6px 25px {COLORS['glow_green']};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def get_plotly_template():
    """Retorna plantilla de plotly con tema futurista."""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(17,22,43,0.3)',
            'font': {
                'family': 'Inter, sans-serif',
                'color': COLORS['text_primary'],
                'size': 12
            },
            'title': {
                'font': {
                    'family': 'Orbitron, sans-serif',
                    'size': 18,
                    'color': COLORS['accent_cyan']
                }
            },
            'xaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'zerolinecolor': 'rgba(255,255,255,0.2)',
                'color': COLORS['text_secondary']
            },
            'yaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'zerolinecolor': 'rgba(255,255,255,0.2)',
                'color': COLORS['text_secondary']
            },
            'colorway': [
                COLORS['accent_cyan'],
                COLORS['accent_violet'],
                COLORS['accent_magenta'],
                COLORS['accent_green'],
                '#FFA726',  # Naranja Arte
                '#AB47BC'
            ]
        }
    }
