"""Clase base para todos los agentes STEM."""
from dataclasses import dataclass, field
from typing import Any
import pandas as pd


@dataclass
class AgentResult:
    """Resultado estructurado de un agente."""
    agent_name: str
    branch: str
    summary: str
    findings: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    figures: list[Any] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


class BaseAgent:
    """Clase base para agentes STEM."""
    
    def __init__(self, name: str, branch: str, icon: str):
        self.name = name
        self.branch = branch
        self.icon = icon
    
    def run(self, df: pd.DataFrame, context: dict) -> AgentResult:
        """
        Ejecuta el análisis del agente.
        
        Args:
            df: DataFrame a analizar
            context: Contexto compartido entre agentes
            
        Returns:
            AgentResult con los hallazgos
        """
        raise NotImplementedError("Cada agente debe implementar run()")
