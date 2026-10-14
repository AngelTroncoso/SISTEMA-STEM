"""Orquestador de agentes STEM."""
import pandas as pd
from agents.base import AgentResult
from agents.technology import TechnologyAgent
from agents.math_agent import MathAgent
from agents.science import ScienceAgent
from agents.engineering import EngineeringAgent


class Orchestrator:
    """Coordina la ejecución de los 4 agentes STEM."""
    
    def __init__(self):
        self.agents = [
            TechnologyAgent(),
            MathAgent(),
            ScienceAgent(),
            EngineeringAgent()
        ]
    
    def run_analysis(self, df: pd.DataFrame, target_col: str | None = None, progress_callback=None) -> dict[str, AgentResult]:
        """
        Ejecuta los 4 agentes en orden y retorna los resultados.
        
        Args:
            df: DataFrame a analizar
            target_col: Columna objetivo opcional para el agente de ingeniería
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con resultados de cada agente
        """
        results = {}
        context = {'target_col': target_col}
        
        for i, agent in enumerate(self.agents):
            if progress_callback:
                progress_callback(agent.name, i, len(self.agents))
            
            try:
                result = agent.run(df, context)
                results[agent.branch] = result
            except Exception as e:
                results[agent.branch] = AgentResult(
                    agent_name=agent.name,
                    branch=agent.branch,
                    summary=f"Error al ejecutar agente {agent.name}",
                    error=str(e)
                )
        
        return results
    
    def generate_executive_report(self, results: dict[str, AgentResult]) -> dict:
        """
        Genera informe ejecutivo consolidado.
        
        Args:
            results: Resultados de cada agente
            
        Returns:
            Diccionario con resumen ejecutivo
        """
        # Consolidar hallazgos clave
        key_findings = []
        all_warnings = []
        all_recommendations = []
        
        for branch, result in results.items():
            if result.error:
                all_warnings.append(f"[{branch}] Error: {result.error}")
                continue
            
            # Tomar los 2 hallazgos más importantes de cada agente
            if result.findings:
                for finding in result.findings[:2]:
                    if not finding.startswith("  "):  # Evitar sub-items
                        key_findings.append(f"[{branch}] {finding}")
            
            all_warnings.extend([f"[{branch}] {w}" for w in result.warnings[:2]])
            all_recommendations.extend([f"[{branch}] {r}" for r in result.recommendations[:2]])
        
        # Priorizar los 5 hallazgos más relevantes
        key_findings = key_findings[:5]
        
        # Resumen general
        summary = "Este análisis multiagente STEM evaluó los datos desde 4 perspectivas complementarias. "
        
        tech_result = results.get('Tecnología')
        if tech_result and not tech_result.error:
            quality = tech_result.metrics.get('Calidad de datos', 0)
            summary += f"La calidad técnica de los datos es {quality:.0f}/100. "
        
        math_result = results.get('Matemáticas')
        if math_result and not math_result.error:
            summary += "El análisis estadístico identificó distribuciones, correlaciones y outliers. "
        
        science_result = results.get('Ciencia')
        if science_result and not science_result.error:
            n_hyp = science_result.metrics.get('Hipótesis contrastadas', 0)
            summary += f"Se contrastaron {n_hyp} hipótesis científicas. "
        
        eng_result = results.get('Ingeniería')
        if eng_result and not eng_result.error:
            summary += "Se implementó limpieza de datos y un modelo baseline de machine learning."
        
        # Próximos pasos
        next_steps = [
            "Validar hallazgos con stakeholders y expertos del dominio",
            "Realizar análisis de sensibilidad sobre variables clave",
            "Iterar sobre el modelo de ML con feature engineering avanzado",
            "Recolectar más datos si es necesario para mejorar conclusiones",
            "Implementar dashboard interactivo para monitoreo continuo"
        ]
        
        return {
            'summary': summary,
            'key_findings': key_findings,
            'warnings': all_warnings[:5],
            'recommendations': all_recommendations[:5],
            'next_steps': next_steps
        }
