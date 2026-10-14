"""Agente de Arte: visualización y storytelling de datos."""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from agents.base import BaseAgent, AgentResult


class ArtAgent(BaseAgent):
    """Agente que transforma datos en narrativas visuales."""
    
    def __init__(self):
        super().__init__("Arte", "Arte", "🎨")
    
    def run(self, df: pd.DataFrame, context: dict) -> AgentResult:
        """Crea visualizaciones artísticas y narrativas de datos."""
        try:
            findings = []
            metrics = {}
            figures = []
            warnings = []
            recommendations = []
            
            numeric_cols = context.get('numeric_cols', df.select_dtypes(include=['number']).columns.tolist())
            categorical_cols = context.get('categorical_cols', df.select_dtypes(include=['object', 'category']).columns.tolist())
            datetime_cols = context.get('datetime_cols', df.select_dtypes(include=['datetime']).columns.tolist())
            
            findings.append(f"Transformando {len(df):,} filas de datos en narrativa visual")
            
            # 1. Paleta de colores dominante (basada en distribuciones)
            if numeric_cols:
                primary_col = numeric_cols[0]
                data = df[primary_col].dropna()
                
                if len(data) > 0:
                    q1, q2, q3 = data.quantile([0.25, 0.5, 0.75])
                    findings.append(f"Paleta emocional de '{primary_col}': bajo ({q1:.1f}), medio ({q2:.1f}), alto ({q3:.1f})")
            
            # 2. Composición visual: distribución de categorías
            if categorical_cols:
                cat_col = categorical_cols[0]
                value_counts = df[cat_col].value_counts()
                
                if len(value_counts) > 0:
                    findings.append(f"Composición dominante: '{value_counts.index[0]}' representa {value_counts.iloc[0]/len(df)*100:.1f}% del dataset")
                    
                    # Sunburst chart artístico
                    fig_sunburst = go.Figure(go.Sunburst(
                        labels=value_counts.index.tolist() + ["Total"],
                        parents=["Total"] * len(value_counts) + [""],
                        values=value_counts.tolist() + [value_counts.sum()],
                        marker=dict(
                            colorscale='Viridis',
                            line=dict(width=2)
                        )
                    ))
                    fig_sunburst.update_layout(
                        title=f"Composición Visual: {cat_col}",
                        height=500
                    )
                    figures.append(fig_sunburst)
            
            # 3. Ritmo temporal (si hay fechas)
            if datetime_cols and numeric_cols:
                date_col = datetime_cols[0]
                num_col = numeric_cols[0]
                
                temporal_df = df[[date_col, num_col]].dropna().sort_values(date_col)
                
                if len(temporal_df) > 5:
                    # Calcular "ritmo" (variación diaria/mensual)
                    temporal_df['diff'] = temporal_df[num_col].diff().abs()
                    avg_change = temporal_df['diff'].mean()
                    
                    findings.append(f"Ritmo temporal: cambio promedio de {avg_change:.2f} en '{num_col}'")
                    
                    # Gráfico de área con gradiente
                    fig_rhythm = go.Figure()
                    fig_rhythm.add_trace(go.Scatter(
                        x=temporal_df[date_col],
                        y=temporal_df[num_col],
                        fill='tozeroy',
                        mode='lines',
                        line=dict(width=2, color='rgb(139, 92, 246)'),
                        fillcolor='rgba(139, 92, 246, 0.3)',
                        name='Flujo temporal'
                    ))
                    fig_rhythm.update_layout(
                        title=f"Ritmo Visual: {num_col} a través del tiempo",
                        xaxis_title="Tiempo",
                        yaxis_title=num_col,
                        height=400
                    )
                    figures.append(fig_rhythm)
            
            # 4. Armonía de datos: correlación como arte
            if len(numeric_cols) >= 3:
                # Scatter 3D artístico
                col1, col2, col3 = numeric_cols[0], numeric_cols[1], numeric_cols[2] if len(numeric_cols) > 2 else numeric_cols[0]
                
                sample_df = df[[col1, col2, col3]].dropna()
                if len(sample_df) > 10:
                    sample_df = sample_df.sample(min(500, len(sample_df)), random_state=42)
                    
                    fig_3d = go.Figure(data=[go.Scatter3d(
                        x=sample_df[col1],
                        y=sample_df[col2],
                        z=sample_df[col3],
                        mode='markers',
                        marker=dict(
                            size=5,
                            color=sample_df[col3],
                            colorscale='Rainbow',
                            opacity=0.7,
                            line=dict(width=0.5, color='white')
                        )
                    )])
                    fig_3d.update_layout(
                        title="Armonía Tridimensional de Datos",
                        scene=dict(
                            xaxis_title=col1,
                            yaxis_title=col2,
                            zaxis_title=col3
                        ),
                        height=600
                    )
                    figures.append(fig_3d)
                    findings.append(f"Constelación de datos en 3D revela patrones espaciales entre {col1}, {col2} y {col3}")
            
            # 5. Textura de datos: densidad y distribución
            if numeric_cols:
                primary_col = numeric_cols[0]
                data = df[primary_col].dropna()
                
                if len(data) > 10:
                    # Violin plot artístico
                    fig_texture = go.Figure()
                    fig_texture.add_trace(go.Violin(
                        y=data,
                        name=primary_col,
                        box_visible=True,
                        meanline_visible=True,
                        fillcolor='rgba(0, 229, 255, 0.5)',
                        line_color='rgb(0, 229, 255)',
                        opacity=0.7
                    ))
                    fig_texture.update_layout(
                        title=f"Textura Visual: Densidad de {primary_col}",
                        yaxis_title=primary_col,
                        height=400
                    )
                    figures.append(fig_texture)
                    
                    # Analizar "textura"
                    std_dev = data.std()
                    mean_val = data.mean()
                    cv = (std_dev / mean_val * 100) if mean_val != 0 else 0
                    
                    if cv < 10:
                        texture = "suave y uniforme"
                    elif cv < 30:
                        texture = "moderadamente variada"
                    else:
                        texture = "altamente texturizada"
                    
                    findings.append(f"Textura de '{primary_col}': {texture} (CV: {cv:.1f}%)")
            
            # 6. Narrativa de balance
            if len(numeric_cols) >= 2:
                col1, col2 = numeric_cols[0], numeric_cols[1]
                
                ratio = df[col1].sum() / df[col2].sum() if df[col2].sum() != 0 else 0
                findings.append(f"Balance narrativo: relación {col1}/{col2} = {ratio:.2f}")
                
                if ratio > 2:
                    findings.append(f"  → '{col1}' domina la composición")
                elif ratio < 0.5:
                    findings.append(f"  → '{col2}' domina la composición")
                else:
                    findings.append(f"  → Composición equilibrada entre ambas variables")
            
            # 7. Storytelling: identificar el "personaje principal"
            if categorical_cols and numeric_cols:
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]
                
                story_df = df.groupby(cat_col)[num_col].agg(['mean', 'sum', 'count']).sort_values('sum', ascending=False)
                
                if len(story_df) > 0:
                    protagonist = story_df.index[0]
                    protagonist_share = story_df.loc[protagonist, 'sum'] / story_df['sum'].sum() * 100
                    
                    findings.append(f"Protagonista de la narrativa: '{protagonist}' con {protagonist_share:.1f}% del total")
                    
                    # Treemap narrativo
                    fig_story = go.Figure(go.Treemap(
                        labels=story_df.index.tolist(),
                        parents=[""] * len(story_df),
                        values=story_df['sum'].tolist(),
                        marker=dict(
                            colorscale='Viridis',
                            line=dict(width=2, color='white')
                        ),
                        textinfo="label+value+percent parent"
                    ))
                    fig_story.update_layout(
                        title=f"Mapa Narrativo: {cat_col} × {num_col}",
                        height=500
                    )
                    figures.append(fig_story)
            
            # Métricas artísticas
            metrics["Dimensiones visuales"] = len(numeric_cols) + len(categorical_cols)
            metrics["Riqueza cromática"] = min(len(df[categorical_cols[0]].unique()) if categorical_cols else 0, 20)
            metrics["Densidad narrativa"] = len(df)
            
            # Recomendaciones artísticas
            recommendations.append("Considera crear un dashboard interactivo para explorar estos patrones visualmente")
            recommendations.append("Las visualizaciones revelan historias que los números solos no pueden contar")
            
            if len(figures) >= 3:
                recommendations.append("La combinación de múltiples vistas crea una narrativa visual completa")
            
            if datetime_cols:
                recommendations.append("La dimensión temporal agrega profundidad narrativa a la historia de los datos")
            
            recommendations.append("Cada visualización es una perspectiva diferente de la misma realidad")
            
            # Resumen artístico
            summary = f"Análisis visual de {len(df):,} puntos de datos. "
            summary += f"Se crearon {len(figures)} visualizaciones artísticas que revelan composición, ritmo, armonía y textura. "
            if categorical_cols:
                summary += f"La narrativa está dominada por '{protagonist if 'protagonist' in locals() else 'múltiples elementos'}'. "
            summary += "Los datos cuentan una historia visual de patrones, balance y flujo."
            
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
                summary="Error en el análisis artístico",
                error=str(e)
            )
