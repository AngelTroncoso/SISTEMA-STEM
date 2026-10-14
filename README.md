# 🔬 SISTEMA-STEAM · Analista Multiagente

Sistema de análisis de datos con **interfaz futurista** y **5 agentes especializados** que evalúan datasets desde perspectivas complementarias: Ciencia, Tecnología, Ingeniería, Matemáticas y **Arte**.

## ⚡ Instalación

```bash
pip install -r requirements.txt
python generate_sample.py
python generate_assets.py
```

## 🎨 Características

- **UI Futurista**: Tema cyberpunk con glassmorphism, degradados neón y animaciones suaves
- **Agente Ciencia**: Formula y contrasta hipótesis científicas con tests estadísticos
- **Agente Tecnología**: Evalúa calidad técnica, detecta nulos, duplicados y outliers
- **Agente Matemáticas**: Estadística descriptiva, correlaciones, normalidad, ANOVA
- **Agente Ingeniería**: Limpieza automática, modelo ML baseline y feature importance
- **Agente Arte**: Visualizaciones artísticas, storytelling de datos y narrativa visual
- **IA Generativa**: Integración opcional con **Gemini 3** para resúmenes mejorados

## 🔑 Variables de Entorno (Opcional)

Crea un archivo `.env` para usar IA:

```
GEMINI_API_KEY=tu_clave_aqui
GEMINI_MODEL=gemini-3-flash-preview
```

Alternativamente, ingresa la API key en la barra lateral.

## 🚀 Uso

```bash
streamlit run app.py
```

Sube un archivo CSV/Excel o prueba con datos de ejemplo.
