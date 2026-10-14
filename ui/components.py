"""Componentes UI reutilizables."""
import streamlit as st
import base64
from pathlib import Path
from ui.theme import COLORS, AGENT_COLORS, AGENT_GLOWS


def hero_banner():
    """Muestra el banner hero principal."""
    hero_path = Path("assets/hero.svg")
    
    if hero_path.exists():
        with open(hero_path, 'r', encoding='utf-8') as f:
            hero_svg = f.read()
        
        st.markdown(f"""
        <div class="fade-in" style="margin-bottom: 2rem;">
            {hero_svg}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, {COLORS['accent_cyan']}, {COLORS['accent_violet']}, {COLORS['accent_magenta']});
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">
            SISTEMA-STEM
        </h1>
        <p style="font-size: 1.25rem; color: {COLORS['text_secondary']}; margin-top: 0;">
            Analista Multiagente · Análisis de Datos desde 4 Perspectivas
        </p>
    </div>
    """, unsafe_allow_html=True)


def agent_card(agent_name: str, icon_name: str, description: str, status: str = "idle"):
    """
    Muestra una tarjeta de agente.
    
    Args:
        agent_name: Nombre del agente
        icon_name: Nombre del archivo de ícono
        description: Descripción breve
        status: idle, analyzing, done, error
    """
    color = AGENT_COLORS.get(agent_name, COLORS['accent_cyan'])
    glow = AGENT_GLOWS.get(agent_name, COLORS['glow_cyan'])
    
    status_icons = {
        'idle': '⏳',
        'analyzing': '⚡',
        'done': '✅',
        'error': '⚠️'
    }
    
    status_icon = status_icons.get(status, '')
    pulse_class = 'pulse' if status == 'analyzing' else ''
    
    icon_path = Path(f"assets/{icon_name}")
    icon_html = ""
    if icon_path.exists():
        with open(icon_path, 'r', encoding='utf-8') as f:
            icon_svg = f.read()
        icon_html = f'<div style="margin-bottom: 1rem;">{icon_svg}</div>'
    
    st.markdown(f"""
    <div class="glass-card fade-in {pulse_class}" 
         style="border-color: {color}; box-shadow: 0 8px 32px {glow};">
        {icon_html}
        <h3 style="color: {color}; margin-bottom: 0.5rem; font-size: 1.5rem;">
            {status_icon} {agent_name}
        </h3>
        <p style="color: {COLORS['text_secondary']}; margin: 0; line-height: 1.5;">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, color: str = None):
    """Muestra una métrica en una tarjeta."""
    if color is None:
        color = COLORS['accent_cyan']
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; 
                  text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;">
            {label}
        </p>
        <p style="color: {color}; font-size: 2rem; font-family: 'Orbitron', sans-serif; 
                  font-weight: 700; margin: 0; text-shadow: 0 0 10px {color};">
            {value}
        </p>
    </div>
    """, unsafe_allow_html=True)


def section_title(text: str, color: str = None):
    """Muestra un título de sección estilizado."""
    if color is None:
        color = COLORS['accent_cyan']
    
    st.markdown(f"""
    <h2 style="color: {color}; font-family: 'Orbitron', sans-serif; 
               font-size: 1.75rem; margin: 2rem 0 1rem 0; 
               text-shadow: 0 0 10px {color};">
        {text}
    </h2>
    """, unsafe_allow_html=True)


def badge(text: str, color: str = None):
    """Muestra un badge estilizado."""
    if color is None:
        color = COLORS['accent_cyan']
    
    return f"""<span style="display: inline-block; padding: 0.25rem 0.75rem; 
                           background: {color}22; border: 1px solid {color}; 
                           border-radius: 20px; color: {color}; font-size: 0.85rem;
                           font-weight: 600; margin: 0.25rem;">
                {text}
            </span>"""


def steps_guide():
    """Muestra la guía de 3 pasos."""
    st.markdown(f"""
    <div style="margin: 3rem 0;">
        <h3 style="text-align: center; color: {COLORS['text_primary']}; 
                   font-family: 'Orbitron', sans-serif; margin-bottom: 2rem;">
            Cómo Funciona
        </h3>
        <div style="display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center;">
            <div class="glass-card" style="flex: 1; min-width: 200px; max-width: 300px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                <h4 style="color: {COLORS['accent_cyan']}; font-family: 'Orbitron', sans-serif;">
                    1. Sube tu Archivo
                </h4>
                <p style="color: {COLORS['text_secondary']};">
                    CSV, XLS o XLSX con tus datos
                </p>
            </div>
            <div class="glass-card" style="flex: 1; min-width: 200px; max-width: 300px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h4 style="color: {COLORS['accent_violet']}; font-family: 'Orbitron', sans-serif;">
                    2. Los Agentes Analizan
                </h4>
                <p style="color: {COLORS['text_secondary']};">
                    4 perspectivas complementarias
                </p>
            </div>
            <div class="glass-card" style="flex: 1; min-width: 200px; max-width: 300px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4 style="color: {COLORS['accent_magenta']}; font-family: 'Orbitron', sans-serif;">
                    3. Recibe tu Informe
                </h4>
                <p style="color: {COLORS['text_secondary']};">
                    Insights accionables y visualizaciones
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def logo_svg():
    """Retorna el logo SVG incrustado."""
    logo_path = Path("assets/logo.svg")
    if logo_path.exists():
        with open(logo_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""
