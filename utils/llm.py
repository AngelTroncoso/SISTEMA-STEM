"""Capa opcional de IA usando Gemini API."""
import os
from typing import Optional
import json


class LLMEnhancer:
    """Mejora resúmenes de agentes usando IA generativa."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        self.enabled = self.api_key is not None and len(self.api_key) > 10
    
    def enhance_summary(self, agent_name: str, findings: list[str], metrics: dict) -> str:
        """
        Mejora el resumen de un agente usando IA.
        
        Args:
            agent_name: Nombre del agente
            findings: Lista de hallazgos
            metrics: Métricas calculadas
            
        Returns:
            Resumen mejorado o resumen por plantilla si falla
        """
        if not self.enabled:
            return self._template_summary(agent_name, findings, metrics)
        
        try:
            # Preparar datos agregados (nunca enviar datos crudos)
            data_summary = {
                'agente': agent_name,
                'hallazgos': findings[:10],  # Limitar a 10
                'metricas': {k: str(v) for k, v in list(metrics.items())[:10]}
            }
            
            prompt = f"""Eres un analista de datos experto. Resume los siguientes hallazgos del agente '{agent_name}' en 3-5 frases claras y profesionales en español:

Hallazgos: {json.dumps(data_summary['hallazgos'], ensure_ascii=False)}
Métricas: {json.dumps(data_summary['metricas'], ensure_ascii=False)}

Resume de forma ejecutiva y precisa, destacando lo más importante."""
            
            # Simular llamada API (en producción usar requests o google-generativeai)
            # Por ahora, retornar template si no hay implementación real
            return self._template_summary(agent_name, findings, metrics)
            
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
