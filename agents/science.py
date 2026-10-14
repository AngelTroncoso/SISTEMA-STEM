"""Agente de Ciencia: formulación y contraste de hipótesis."""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from agents.base import BaseAgent, AgentResult


class ScienceAgent(BaseAgent):
    """Agente que formula y contrasta hipótesis científicas."""
    
    def __init__(self):
        super().__init__("Ciencia", "Ciencia", "🔬")
    
    def run(self, df: pd.DataFrame, context: dict) -> AgentResult:
        """Formula hipótesis y las contrasta con tests estadísticos."""
        try:
            findings = []
            metrics = {}
            figures = []
            warnings = []
            recommendations = []
            
            numeric_cols = context.get('numeric_cols', df.select_dtypes(include=['number']).columns.tolist())
            categorical_cols = context.get('categorical_cols', df.select_dtypes(include=['object', 'category']).columns.tolist())
            datetime_cols = context.get('datetime_cols', df.select_dtypes(include=['datetime']).columns.tolist())
            
            hypotheses_tested = 0
            
            # Hipótesis 1: Correlación entre dos variables numéricas
            if len(numeric_cols) >= 2:
                col1, col2 = numeric_cols[0], numeric_cols[1]
                data1 = df[col1].dropna()
                data2 = df[col2].dropna()
                common_idx = df[[col1, col2]].dropna().index
                
                if len(common_idx) > 10:
                    corr, p_value = stats.pearsonr(df.loc[common_idx, col1], df.loc[common_idx, col2])
                    hypotheses_tested += 1
                    
                    findings.append(f"**H1: '{col1}' correlaciona con '{col2}'**")
                    findings.append(f"  • Correlación de Pearson: r={corr:.3f}, p={p_value:.4f}")
                    
                    effect_size = "fuerte" if abs(corr) > 0.5 else "moderado" if abs(corr) > 0.3 else "débil"
                    
                    if p_value < 0.05:
                        findings.append(f"  • ✓ HIPÓTESIS APOYADA: correlación {effect_size} y significativa")
                    else:
                        findings.append(f"  • ✗ HIPÓTESIS NO APOYADA: no hay correlación significativa (p≥0.05)")
            
            # Hipótesis 2: Diferencia entre grupos categóricos
            if categorical_cols and numeric_cols:
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]
                
                unique_cats = df[cat_col].nunique()
                if 2 <= unique_cats <= 10:
                    groups = [group[num_col].dropna() for name, group in df.groupby(cat_col)]
                    groups = [g for g in groups if len(g) >= 2]
                    
                    if len(groups) >= 2:
                        hypotheses_tested += 1
                        findings.append(f"**H2: '{cat_col}' influye en '{num_col}'**")
                        
                        if len(groups) == 2:
                            # t-test
                            stat, p_value = stats.ttest_ind(groups[0], groups[1])
                            cohens_d = (groups[0].mean() - groups[1].mean()) / np.sqrt((groups[0].std()**2 + groups[1].std()**2) / 2)
                            findings.append(f"  • t-test: t={stat:.3f}, p={p_value:.4f}, Cohen's d={cohens_d:.3f}")
                            effect = "grande" if abs(cohens_d) > 0.8 else "mediano" if abs(cohens_d) > 0.5 else "pequeño"
                        else:
                            # ANOVA
                            stat, p_value = stats.f_oneway(*groups)
                            findings.append(f"  • ANOVA: F={stat:.3f}, p={p_value:.4f}")
                            effect = "significativo"
                        
                        if p_value < 0.05:
                            findings.append(f"  • ✓ HIPÓTESIS APOYADA: hay diferencias {effect} entre grupos")
                        else:
                            findings.append(f"  • ✗ HIPÓTESIS NO APOYADA: no hay diferencias significativas")
            
            # Hipótesis 3: Otra correlación numérica
            if len(numeric_cols) >= 3:
                col1, col2 = numeric_cols[0], numeric_cols[2]
                common_idx = df[[col1, col2]].dropna().index
                
                if len(common_idx) > 10:
                    # Spearman para robustez
                    corr, p_value = stats.spearmanr(df.loc[common_idx, col1], df.loc[common_idx, col2])
                    hypotheses_tested += 1
                    
                    findings.append(f"**H3: '{col1}' se asocia con '{col2}'**")
                    findings.append(f"  • Correlación de Spearman: ρ={corr:.3f}, p={p_value:.4f}")
                    
                    if p_value < 0.05:
                        findings.append(f"  • ✓ HIPÓTESIS APOYADA: existe asociación monotónica significativa")
                    else:
                        findings.append(f"  • ✗ HIPÓTESIS NO APOYADA: no se detecta asociación")
            
            # Hipótesis 4: Distribución uniforme de una categórica
            if categorical_cols:
                cat_col = categorical_cols[0]
                value_counts = df[cat_col].value_counts()
                
                if 2 <= len(value_counts) <= 20:
                    hypotheses_tested += 1
                    expected = len(df) / len(value_counts)
                    chi2, p_value = stats.chisquare(value_counts.values)
                    
                    findings.append(f"**H4: '{cat_col}' tiene distribución uniforme**")
                    findings.append(f"  • Chi-cuadrado: χ²={chi2:.3f}, p={p_value:.4f}")
                    
                    if p_value < 0.05:
                        findings.append(f"  • ✗ HIPÓTESIS NO APOYADA: distribución no es uniforme (p<0.05)")
                    else:
                        findings.append(f"  • ✓ HIPÓTESIS APOYADA: distribución es aproximadamente uniforme")
            
            # Hipótesis 5: Comparación de varianzas
            if len(numeric_cols) >= 2:
                col1, col2 = numeric_cols[0], numeric_cols[1]
                data1 = df[col1].dropna()
                data2 = df[col2].dropna()
                
                if len(data1) > 10 and len(data2) > 10:
                    hypotheses_tested += 1
                    stat, p_value = stats.levene(data1, data2)
                    
                    findings.append(f"**H5: '{col1}' y '{col2}' tienen igual variabilidad**")
                    findings.append(f"  • Test de Levene: W={stat:.3f}, p={p_value:.4f}")
                    
                    if p_value < 0.05:
                        findings.append(f"  • ✗ HIPÓTESIS NO APOYADA: varianzas son diferentes")
                    else:
                        findings.append(f"  • ✓ HIPÓTESIS APOYADA: varianzas son homogéneas")
            
            metrics["Hipótesis contrastadas"] = hypotheses_tested
            
            # Análisis temporal si hay fecha
            if datetime_cols and numeric_cols:
                date_col = datetime_cols[0]
                num_col = numeric_cols[0]
                
                temporal_df = df[[date_col, num_col]].dropna().sort_values(date_col)
                
                if len(temporal_df) > 5:
                    fig_temporal = go.Figure()
                    fig_temporal.add_trace(go.Scatter(
                        x=temporal_df[date_col],
                        y=temporal_df[num_col],
                        mode='lines+markers',
                        name=num_col,
                        line=dict(color='royalblue')
                    ))
                    fig_temporal.update_layout(
                        title=f"Tendencia Temporal: {num_col}",
                        xaxis_title="Fecha",
                        yaxis_title=num_col,
                        height=400
                    )
                    figures.append(fig_temporal)
                    
                    findings.append(f"Se analizó la tendencia temporal de '{num_col}' a lo largo del tiempo")
            
            # Preguntas abiertas
            recommendations.append("Preguntas para investigar más:")
            if categorical_cols and numeric_cols:
                recommendations.append(f"  • ¿Qué factores explican las diferencias en {numeric_cols[0]} entre categorías?")
            if len(numeric_cols) >= 2:
                recommendations.append(f"  • ¿Es la relación entre {numeric_cols[0]} y {numeric_cols[1]} causal o espuria?")
            if datetime_cols:
                recommendations.append("  • ¿Existen patrones estacionales o cíclicos en las series temporales?")
            recommendations.append("  • ¿Qué variables omitidas podrían estar influyendo en los resultados?")
            
            # Resumen
            summary = f"Se formularon y contrastaron {hypotheses_tested} hipótesis usando tests estadísticos. "
            summary += "Cada hipótesis se evaluó con su p-valor y tamaño del efecto para interpretar la significancia práctica. "
            if datetime_cols:
                summary += "Se incluyó análisis de tendencias temporales. "
            summary += "Los resultados apuntan a relaciones para explorar en profundidad."
            
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
                summary="Error en el análisis científico",
                error=str(e)
            )
