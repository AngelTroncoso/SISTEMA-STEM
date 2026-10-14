"""Capa de IA usando Google Gemini 3."""
import os
from typing import Optional
import json
import streamlit as st

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# Prompts de sistema por agente
SYSTEM_PROMPTS = {
    'Ciencia': """Eres un científico de datos experto. Analiza hallazgos desde una perspectiva científica,
    enfocándote en hipótesis, evidencia estadística y conclusiones basadas en datos. Resume en español,
    de forma clara y precisa, en 3-6 frases.""",
    
    'Tecnología': """Eres un técnico de datos senior. Analiza la calidad técnica de los datos,
    detecta problemas de integridad y recomienda mejoras. Resume en español, de forma clara y directa,
    en 3-6 frases.""",
    
    'Ingeniería': """Eres un ingeniero de machine learning. Analiza desde la perspectiva de implementación,
    modelado y optimización de sistemas. Resume en español, de forma práctica y accionable, en 3-6 frases.""",
    
    'Matemáticas': """Eres un matemático especializado en estadística. Analiza distribuciones, correlaciones
    y patrones matemáticos. Resume en español, de forma rigurosa pero accesible, en 3-6 frases."""
}


class LLMEnhancer:
    """Mejora resúmenes de agentes usando Gemini 3."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        self.model = os.getenv('GEMINI_MODEL', 'gemini-3-flash-preview')
        self.enabled = GENAI_AVAILABLE and self.api_key is not None and len(self.api_key) > 10
        self.client = None
        
        if self.enabled:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.enabled = False
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Prueba la conexión con Gemini.
        
        Returns:
            Tupla (éxito, mensaje)
        """
        if not GENAI_AVAILABLE:
            return False, "Módulo google-genai no instalado"
        
        if not self.api_key or len(self.api_key) < 10:
            return False, "API key no configurada o inválida"
        
        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents="Di 'Conexión exitosa' en español.",
                config={'max_output_tokens': 20, 'temperature': 0}
            )
            return True, "Conexión exitosa con Gemini"
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower():
                return False, "Cuota de API excedida"
            elif "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                return False, "API key inválida"
            else:
                return False, f"Error: {error_msg[:100]}"
    
    def enhance_summary(self, agent_name: str, findings: list[str], metrics: dict) -> str:
        """
        Mejora el resumen de un agente usando Gemini.
        
        Args:
            agent_name: Nombre del agente
            findings: Lista de hallazgos
            metrics: Métricas calculadas
            
        Returns:
            Resumen mejorado o resumen por plantilla si falla
        """
        # Revisar cache
        cache_key = f"llm_summary_{agent_name}_{hash(str(findings[:5]) + str(metrics))}"
        if cache_key in st.session_state:
            return st.session_state[cache_key]
        
        if not self.enabled or not self.client:
            return self._template_summary(agent_name, findings, metrics)
        
        try:
            # Preparar datos agregados (nunca enviar datos crudos)
            data_summary = {
                'hallazgos': findings[:10],  # Limitar a 10
                'metricas': {k: str(v) for k, v in list(metrics.items())[:10]}
            }
            
            system_prompt = SYSTEM_PROMPTS.get(agent_name, SYSTEM_PROMPTS['Ciencia'])
            
            user_prompt = f"""Resume los siguientes hallazgos del análisis de datos:

Hallazgos principales:
{chr(10).join(['- ' + f for f in data_summary['hallazgos'][:5]])}

Métricas clave:
{chr(10).join([f'- {k}: {v}' for k, v in list(data_summary['metricas'].items())[:5]])}

Resume en 3-6 frases claras y profesionales, destacando lo más relevante."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{system_prompt}\n\n{user_prompt}",
                config={
                    'max_output_tokens': 300,
                    'temperature': 0.7,
                    'timeout': 30
                }
            )
            
            summary = response.text.strip()
            
            # Guardar en cache
            st.session_state[cache_key] = summary
            
            return summary
            
        except Exception as e:
            # Fallback silencioso a plantilla
            return self._template_summary(agent_name, findings, metrics)
    
    def _template_summary(self, agent_name: str, findings: list[str], metrics: dict) -> str:
        """Genera resumen por plantilla cuando IA no está disponible."""
        summary_parts = []
        
        if findings:
            summary_parts.append(findings[0])
        
        if len(findings) > 1:
            summary_parts.append(findings[1])
        
        if metrics:
            key_metrics = list(metrics.items())[:3]
            metrics_str = ", ".join([f"{k}: {v}" for k, v in key_metrics])
            summary_parts.append(f"Métricas clave: {metrics_str}")
        
        return " ".join(summary_parts) if summary_parts else f"Análisis completado por agente {agent_name}."
