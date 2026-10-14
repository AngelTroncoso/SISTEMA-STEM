"""Agente de Tecnología: análisis técnico de datos."""
import pandas as pd
import plotly.graph_objects as go
from agents.base import BaseAgent, AgentResult


class TechnologyAgent(BaseAgent):
    """Agente que analiza aspectos técnicos del dataset."""
    
    def __init__(self):
        super().__init__("Tecnología", "Tecnología", "💻")
    
    def run(self, df: pd.DataFrame, context: dict) -> AgentResult:
        """Analiza calidad técnica de los datos."""
        try:
            findings = []
            metrics = {}
            warnings = []
            recommendations = []
            
            # Shape y memoria
            n_rows, n_cols = df.shape
            memory_mb = df.memory_usage(deep=True).sum() / 1024**2
            
            metrics["Filas"] = n_rows
            metrics["Columnas"] = n_cols
            metrics["Memoria (MB)"] = round(memory_mb, 2)
            
            findings.append(f"Dataset con {n_rows:,} filas y {n_cols} columnas")
            
            # Tipos de datos
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
            
            context['numeric_cols'] = numeric_cols
            context['categorical_cols'] = categorical_cols
            context['datetime_cols'] = datetime_cols
            
            findings.append(f"Columnas numéricas: {len(numeric_cols)}, categóricas: {len(categorical_cols)}, fechas: {len(datetime_cols)}")
            
            # Valores nulos
            null_pct = (df.isnull().sum() / len(df) * 100).round(2)
            null_cols = null_pct[null_pct > 0].sort_values(ascending=False)
            
            if len(null_cols) > 0:
                findings.append(f"Se detectaron valores nulos en {len(null_cols)} columnas")
                for col in null_cols.head(5).index:
                    warnings.append(f"{col}: {null_cols[col]}% de valores nulos")
            else:
                findings.append("No se detectaron valores nulos")
            
            # Gráfico de nulos
            fig_nulls = go.Figure()
            if len(null_cols) > 0:
                top_nulls = null_cols.head(15)
                fig_nulls.add_trace(go.Bar(
                    y=top_nulls.index,
                    x=top_nulls.values,
                    orientation='h',
                    marker_color='indianred'
                ))
                fig_nulls.update_layout(
                    title="Porcentaje de Valores Nulos por Columna",
                    xaxis_title="% Nulos",
                    yaxis_title="Columna",
                    height=max(400, len(top_nulls) * 25)
                )
            
            # Duplicados
            n_duplicates = df.duplicated().sum()
            metrics["Filas duplicadas"] = n_duplicates
            if n_duplicates > 0:
                warnings.append(f"Se encontraron {n_duplicates} filas duplicadas ({n_duplicates/len(df)*100:.1f}%)")
            else:
                findings.append("No se encontraron filas duplicadas")
            
            # Columnas constantes
            constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
            if constant_cols:
                warnings.append(f"Columnas constantes (sin variación): {', '.join(constant_cols)}")
                recommendations.append("Considera eliminar columnas constantes, no aportan información")
            
            # Alta cardinalidad
            high_card_cols = []
            for col in categorical_cols:
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio > 0.5 and df[col].nunique() > 50:
                    high_card_cols.append(col)
            
            if high_card_cols:
                warnings.append(f"Columnas con alta cardinalidad: {', '.join(high_card_cols)}")
                recommendations.append("Las columnas de alta cardinalidad pueden necesitar agrupación o encoding especial")
            
            # Puntaje de calidad (0-100)
            quality_score = 100
            quality_score -= min(null_pct.mean(), 50)  # Penaliza hasta 50 puntos por nulos
            quality_score -= min(n_duplicates / len(df) * 100, 20)  # Penaliza hasta 20 por duplicados
            quality_score -= len(constant_cols) * 5  # -5 por cada columna constante
            quality_score = max(0, quality_score)
            
            metrics["Calidad de datos"] = round(quality_score, 1)
            findings.append(f"Puntaje de calidad de datos: {quality_score:.1f}/100")
            
            # Recomendaciones generales
            if quality_score < 70:
                recommendations.append("La calidad de datos es baja. Se recomienda limpieza antes de modelar")
            
            if memory_mb > 100:
                recommendations.append("El dataset es grande. Considera optimizar tipos de datos o muestrear")
            
            summary = f"Dataset de {n_rows:,} filas × {n_cols} columnas con calidad de {quality_score:.0f}/100. "
            summary += f"Se identificaron {len(numeric_cols)} columnas numéricas y {len(categorical_cols)} categóricas. "
            if len(null_cols) > 0:
                summary += f"Existen valores nulos en {len(null_cols)} columnas. "
            if n_duplicates > 0:
                summary += f"Se detectaron {n_duplicates} filas duplicadas."
            else:
                summary += "No hay filas duplicadas."
            
            return AgentResult(
                agent_name=self.name,
                branch=self.branch,
                summary=summary,
                findings=findings,
                metrics=metrics,
                figures=[fig_nulls] if len(null_cols) > 0 else [],
                recommendations=recommendations,
                warnings=warnings
            )
            
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                branch=self.branch,
                summary="Error en el análisis técnico",
                error=str(e)
            )
