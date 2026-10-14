"""Agente de Matemáticas: estadística descriptiva e inferencial."""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy import stats
from agents.base import BaseAgent, AgentResult


class MathAgent(BaseAgent):
    """Agente que realiza análisis estadístico."""
    
    def __init__(self):
        super().__init__("Matemáticas", "Matemáticas", "📐")
    
    def run(self, df: pd.DataFrame, context: dict) -> AgentResult:
        """Ejecuta análisis estadístico completo."""
        try:
            findings = []
            metrics = {}
            figures = []
            warnings = []
            recommendations = []
            
            numeric_cols = context.get('numeric_cols', df.select_dtypes(include=['number']).columns.tolist())
            
            if len(numeric_cols) == 0:
                return AgentResult(
                    agent_name=self.name,
                    branch=self.branch,
                    summary="No hay columnas numéricas para analizar",
                    warnings=["El dataset no contiene columnas numéricas"]
                )
            
            # Estadística descriptiva
            desc = df[numeric_cols].describe()
            findings.append(f"Análisis estadístico de {len(numeric_cols)} variables numéricas")
            
            for col in numeric_cols[:5]:  # Primeras 5
                data = df[col].dropna()
                if len(data) > 0:
                    metrics[f"{col}_media"] = round(data.mean(), 2)
                    metrics[f"{col}_mediana"] = round(data.median(), 2)
                    metrics[f"{col}_std"] = round(data.std(), 2)
            
            # Asimetría y curtosis
            skewness = df[numeric_cols].skew()
            kurtosis = df[numeric_cols].kurtosis()
            
            highly_skewed = skewness[abs(skewness) > 1].sort_values(ascending=False)
            if len(highly_skewed) > 0:
                findings.append(f"Se detectaron {len(highly_skewed)} columnas con asimetría alta")
                for col in highly_skewed.head(3).index:
                    warnings.append(f"{col}: asimetría = {highly_skewed[col]:.2f} (|>1| indica distribución sesgada)")
            
            # Detección de outliers con IQR
            outlier_counts = {}
            for col in numeric_cols:
                data = df[col].dropna()
                if len(data) > 0:
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    outliers = ((data < lower) | (data > upper)).sum()
                    if outliers > 0:
                        outlier_counts[col] = outliers
            
            if outlier_counts:
                findings.append(f"Se detectaron outliers en {len(outlier_counts)} columnas")
                for col, count in list(outlier_counts.items())[:3]:
                    warnings.append(f"{col}: {count} outliers detectados con método IQR")
                recommendations.append("Los outliers pueden distorsionar modelos. Considera winsorización o transformación")
            
            # Matriz de correlación
            if len(numeric_cols) >= 2:
                corr_matrix = df[numeric_cols].corr()
                
                # Heatmap
                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.values.round(2),
                    texttemplate='%{text}',
                    textfont={"size": 10},
                    colorbar=dict(title="Correlación")
                ))
                fig_corr.update_layout(
                    title="Matriz de Correlación",
                    height=max(400, len(numeric_cols) * 30)
                )
                figures.append(fig_corr)
                
                # Top 5 correlaciones
                corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_pairs.append((
                            corr_matrix.columns[i],
                            corr_matrix.columns[j],
                            corr_matrix.iloc[i, j]
                        ))
                
                corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
                
                if corr_pairs:
                    findings.append("Top 5 correlaciones más fuertes:")
                    for col1, col2, corr_val in corr_pairs[:5]:
                        findings.append(f"  • {col1} ↔ {col2}: {corr_val:.3f}")
                        if abs(corr_val) > 0.8:
                            warnings.append(f"Correlación muy alta entre {col1} y {col2} ({corr_val:.2f}), posible multicolinealidad")
            
            # Test de normalidad (Shapiro-Wilk en muestra)
            normality_results = {}
            for col in numeric_cols[:5]:  # Solo primeras 5
                data = df[col].dropna()
                if 3 < len(data) <= 5000:
                    sample = data.sample(min(500, len(data)), random_state=42)
                    stat, p_value = stats.shapiro(sample)
                    normality_results[col] = p_value
            
            if normality_results:
                findings.append("Test de normalidad (Shapiro-Wilk, p>0.05 indica normalidad):")
                for col, p_val in normality_results.items():
                    is_normal = "normal" if p_val > 0.05 else "no normal"
                    findings.append(f"  • {col}: p={p_val:.4f} ({is_normal})")
                    if p_val <= 0.05:
                        recommendations.append(f"{col} no sigue distribución normal, considera transformación logarítmica o Box-Cox")
            
            # Test chi-cuadrado o ANOVA si hay categóricas
            categorical_cols = context.get('categorical_cols', [])
            if categorical_cols and numeric_cols:
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]
                
                groups = [group[num_col].dropna() for name, group in df.groupby(cat_col) 
                          if len(group[num_col].dropna()) >= 2]
                
                if len(groups) >= 2:
                    try:
                        f_stat, p_value = stats.f_oneway(*groups)
                        findings.append(f"ANOVA: {cat_col} vs {num_col}, p={p_value:.4f}")
                        if p_value < 0.05:
                            findings.append(f"  → Existe diferencia significativa entre grupos (p<0.05)")
                        else:
                            findings.append(f"  → No hay diferencia significativa entre grupos")
                    except:
                        pass
            
            # Resumen
            summary = f"Análisis de {len(numeric_cols)} variables numéricas. "
            if outlier_counts:
                summary += f"Se detectaron outliers en {len(outlier_counts)} columnas. "
            if len(highly_skewed) > 0:
                summary += f"{len(highly_skewed)} columnas presentan asimetría alta. "
            if len(numeric_cols) >= 2:
                top_corr = corr_pairs[0][2] if corr_pairs else 0
                summary += f"La correlación más fuerte encontrada es {abs(top_corr):.2f}."
            
            return AgentResult(
                agent_name=self.name,
                branch=self.branch,
                summary=summary,
                findings=findings,
                metrics=metrics,
                figures=figures,
                recommendations=recommendations,
                warnings=warnings
            )
            
        except Exception as e:
            return AgentResult(
                agent_name=self.name,
                branch=self.branch,
                summary="Error en el análisis matemático",
                error=str(e)
            )
