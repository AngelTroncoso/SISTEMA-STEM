# 🔬 Analista Multiagente STEM

Sistema de análisis de datos con 4 agentes especializados que evalúan datasets desde perspectivas complementarias: Tecnología, Matemáticas, Ciencia e Ingeniería.

## Instalación

```bash
pip install -r requirements.txt
python generate_sample.py
```

## Uso

```bash
streamlit run app.py
```

## Características

- **Agente Tecnología**: calidad de datos, nulos, duplicados, tipos de dato
- **Agente Matemáticas**: estadística descriptiva, correlaciones, outliers, tests de normalidad
- **Agente Ciencia**: formulación y contraste de hipótesis con tests estadísticos
- **Agente Ingeniería**: limpieza automática, modelo ML baseline, feature importance

## Opcional: IA

Configura `GEMINI_API_KEY` en `.env` o en la barra lateral para mejorar resúmenes con IA generativa.
