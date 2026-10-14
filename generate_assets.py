"""Genera assets SVG para la interfaz."""
from pathlib import Path

# Crear directorio si no existe
Path("assets").mkdir(exist_ok=True)

# Hero banner: red neuronal con degradado
hero_svg = """<svg width="100%" height="200" viewBox="0 0 1200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00E5FF;stop-opacity:0.8" />
      <stop offset="50%" style="stop-color:#8B5CF6;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#FF2BD6;stop-opacity:0.8" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Rejilla de fondo -->
  <g opacity="0.1">
    <line x1="0" y1="50" x2="1200" y2="50" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="0" y1="100" x2="1200" y2="100" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="0" y1="150" x2="1200" y2="150" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="200" y1="0" x2="200" y2="200" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="400" y1="0" x2="400" y2="200" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="600" y1="0" x2="600" y2="200" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="800" y1="0" x2="800" y2="200" stroke="#00E5FF" stroke-width="0.5"/>
    <line x1="1000" y1="0" x2="1000" y2="200" stroke="#00E5FF" stroke-width="0.5"/>
  </g>
  
  <!-- Red neuronal -->
  <g filter="url(#glow)">
    <!-- Conexiones -->
    <line x1="150" y1="100" x2="350" y2="60" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="150" y1="100" x2="350" y2="140" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="350" y1="60" x2="600" y2="100" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="350" y1="140" x2="600" y2="100" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="600" y1="100" x2="850" y2="60" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="600" y1="100" x2="850" y2="140" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="850" y1="60" x2="1050" y2="100" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    <line x1="850" y1="140" x2="1050" y2="100" stroke="url(#heroGrad)" stroke-width="2" opacity="0.6"/>
    
    <!-- Nodos -->
    <circle cx="150" cy="100" r="10" fill="#00E5FF"/>
    <circle cx="350" cy="60" r="8" fill="#8B5CF6"/>
    <circle cx="350" cy="140" r="8" fill="#8B5CF6"/>
    <circle cx="600" cy="100" r="12" fill="#FF2BD6"/>
    <circle cx="850" cy="60" r="8" fill="#8B5CF6"/>
    <circle cx="850" cy="140" r="8" fill="#8B5CF6"/>
    <circle cx="1050" cy="100" r="10" fill="#00E5FF"/>
  </g>
</svg>"""

# Ícono Ciencia: matraz
science_svg = """<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sciGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#6D28D9;stop-opacity:1" />
    </linearGradient>
    <filter id="sciGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#sciGlow)">
    <path d="M25 10 L25 25 L15 45 C15 52 20 55 30 55 C40 55 45 52 45 45 L35 25 L35 10 Z" 
          fill="none" stroke="url(#sciGrad)" stroke-width="3"/>
    <circle cx="30" cy="45" r="3" fill="#8B5CF6"/>
    <circle cx="25" cy="40" r="2" fill="#8B5CF6" opacity="0.7"/>
    <circle cx="35" cy="42" r="2.5" fill="#8B5CF6" opacity="0.8"/>
    <line x1="22" y1="10" x2="38" y2="10" stroke="url(#sciGrad)" stroke-width="3"/>
  </g>
</svg>"""

# Ícono Tecnología: chip
tech_svg = """<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="techGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00E5FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0091EA;stop-opacity:1" />
    </linearGradient>
    <filter id="techGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#techGlow)">
    <rect x="18" y="18" width="24" height="24" rx="2" fill="none" stroke="url(#techGrad)" stroke-width="3"/>
    <rect x="25" y="25" width="10" height="10" rx="1" fill="#00E5FF"/>
    <!-- Pines -->
    <line x1="12" y1="23" x2="18" y2="23" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="12" y1="30" x2="18" y2="30" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="12" y1="37" x2="18" y2="37" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="42" y1="23" x2="48" y2="23" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="42" y1="30" x2="48" y2="30" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="42" y1="37" x2="48" y2="37" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="23" y1="12" x2="23" y2="18" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="30" y1="12" x2="30" y2="18" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="37" y1="12" x2="37" y2="18" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="23" y1="42" x2="23" y2="48" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="30" y1="42" x2="30" y2="48" stroke="url(#techGrad)" stroke-width="2"/>
    <line x1="37" y1="42" x2="37" y2="48" stroke="url(#techGrad)" stroke-width="2"/>
  </g>
</svg>"""

# Ícono Ingeniería: engranaje
eng_svg = """<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="engGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#FF2BD6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#C026D3;stop-opacity:1" />
    </linearGradient>
    <filter id="engGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#engGlow)">
    <path d="M30 10 L35 15 L40 13 L42 18 L47 20 L45 25 L50 30 L45 35 L47 40 L42 42 L40 47 L35 45 L30 50 
             L25 45 L20 47 L18 42 L13 40 L15 35 L10 30 L15 25 L13 20 L18 18 L20 13 L25 15 Z" 
          fill="none" stroke="url(#engGrad)" stroke-width="3"/>
    <circle cx="30" cy="30" r="8" fill="none" stroke="url(#engGrad)" stroke-width="3"/>
    <circle cx="30" cy="30" r="4" fill="#FF2BD6"/>
  </g>
</svg>"""

# Ícono Matemáticas: símbolos
math_svg = """<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="mathGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#39FF88;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#10B981;stop-opacity:1" />
    </linearGradient>
    <filter id="mathGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g filter="url(#mathGlow)" fill="url(#mathGrad)" font-family="serif" font-size="24" font-weight="bold">
    <text x="12" y="25">Σ</text>
    <text x="35" y="25">π</text>
    <text x="18" y="48">∞</text>
    <circle cx="45" cy="42" r="6" fill="none" stroke="url(#mathGrad)" stroke-width="2"/>
    <line x1="45" y1="36" x2="45" y2="48" stroke="url(#mathGrad)" stroke-width="2"/>
  </g>
</svg>"""

# Logo SISTEMA-STEM
logo_svg = """<svg width="200" height="60" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00E5FF;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#8B5CF6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF2BD6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <text x="10" y="40" font-family="Orbitron, sans-serif" font-size="32" font-weight="900" 
        fill="url(#logoGrad)">STEM</text>
  <circle cx="160" cy="30" r="8" fill="#00E5FF" opacity="0.8"/>
  <circle cx="175" cy="25" r="6" fill="#8B5CF6" opacity="0.8"/>
  <circle cx="188" cy="30" r="7" fill="#FF2BD6" opacity="0.8"/>
</svg>"""

# Guardar archivos
with open("assets/hero.svg", "w", encoding="utf-8") as f:
    f.write(hero_svg)

with open("assets/science_icon.svg", "w", encoding="utf-8") as f:
    f.write(science_svg)

with open("assets/tech_icon.svg", "w", encoding="utf-8") as f:
    f.write(tech_svg)

with open("assets/eng_icon.svg", "w", encoding="utf-8") as f:
    f.write(eng_svg)

with open("assets/math_icon.svg", "w", encoding="utf-8") as f:
    f.write(math_svg)

with open("assets/logo.svg", "w", encoding="utf-8") as f:
    f.write(logo_svg)

print("✓ Assets SVG generados en assets/:")
print("  - hero.svg")
print("  - science_icon.svg")
print("  - tech_icon.svg")
print("  - eng_icon.svg")
print("  - math_icon.svg")
print("  - logo.svg")
