"""Agente de Ingeniería: limpieza, modelado y optimización."""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
from agents.base import BaseAgent, AgentResult


class EngineeringAgent(BaseAgent):
    """Agente que implementa soluciones de ingeniería de datos y ML."""
    
    def __init__(self):
        super().__init__("Ingeniería", "Ingeniería", "⚙️")
    
    def run(self, df: pd.DataFrame, context: dict) -> AgentResult:
        """Limpia datos, entrena modelo baseline y genera recomendaciones."""
        try:
            findings = []
            metrics = {}
            figures = []
            warnings = []
            recommendations = []
            
            numeric_cols = context.get('numeric_cols', df.select_dtypes(include=['number']).columns.tolist())
            categorical_cols = context.get('categorical_cols', [])
            
            # Limpieza automática
            df_clean = df.copy()
            
            # Eliminar duplicados
            n_duplicates = df_clean.duplicated().sum()
            if n_duplicates > 0:
                df_clean = df_clean.drop_duplicates()
                findings.append(f"Se eliminaron {n_duplicates} filas duplicadas")
            
            # Imputación
            for col in numeric_cols:
                null_count = df_clean[col].isnull().sum()
                if null_count > 0:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                    findings.append(f"Imputados {null_count} valores nulos en '{col}' con mediana")
            
            for col in categorical_cols:
                null_count = df_clean[col].isnull().sum()
                if null_count > 0:
                    mode_val = df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else "DESCONOCIDO"
                    df_clean[col] = df_clean[col].fillna(mode_val)
                    findings.append(f"Imputados {null_count} valores nulos en '{col}' con moda")
            
            # Winsorización de outliers
            for col in numeric_cols:
                data = df_clean[col]
                lower = data.quantile(0.01)
                upper = data.quantile(0.99)
                n_clipped = ((data < lower) | (data > upper)).sum()
                if n_clipped > 0:
                    df_clean[col] = data.clip(lower, upper)
                    findings.append(f"Winsorización de outliers en '{col}': {n_clipped} valores ajustados")
            
            context['df_clean'] = df_clean
            metrics["Filas después de limpieza"] = len(df_clean)
            
            # Selección de variable objetivo
            target_col = context.get('target_col', None)
            
            if not target_col and len(numeric_cols) > 0:
                # Seleccionar automáticamente: la última numérica
                target_col = numeric_cols[-1]
                findings.append(f"Variable objetivo seleccionada automáticamente: '{target_col}'")
            
            if target_col and target_col in df_clean.columns:
                # Preparar features
                feature_cols = [col for col in numeric_cols if col != target_col]
                
                if len(feature_cols) >= 1:
                    X = df_clean[feature_cols].copy()
                    y = df_clean[target_col].copy()
                    
                    # Remover filas con nulos en features o target
                    valid_idx = X.notna().all(axis=1) & y.notna()
                    X = X[valid_idx]
                    y = y[valid_idx]
                    
                    if len(X) > 10:
                        # Decidir si es regresión o clasificación
                        is_classification = y.nunique() < 20 and y.dtype in ['object', 'category', 'int64']
                        
                        if is_classification:
                            le = LabelEncoder()
                            y = le.fit_transform(y.astype(str))
                            findings.append(f"Tarea de CLASIFICACIÓN con {len(np.unique(y))} clases")
                        else:
                            findings.append(f"Tarea de REGRESIÓN")
                        
                        # Split
                        X_train, X_test, y_train, y_test = train_test_split(
                            X, y, test_size=0.2, random_state=42
                        )
                        
                        # Entrenar modelo baseline
                        if is_classification:
                            model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
                        else:
                            model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
                        
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        
                        # Métricas
                        if is_classification:
                            acc = accuracy_score(y_test, y_pred)
                            f1 = f1_score(y_test, y_pred, average='weighted')
                            metrics["Accuracy"] = round(acc, 3)
                            metrics["F1-Score"] = round(f1, 3)
                            findings.append(f"Modelo baseline: Accuracy={acc:.3f}, F1={f1:.3f}")
                        else:
                            mae = mean_absolute_error(y_test, y_pred)
                            r2 = r2_score(y_test, y_pred)
                            metrics["MAE"] = round(mae, 2)
                            metrics["R²"] = round(r2, 3)
                            findings.append(f"Modelo baseline: MAE={mae:.2f}, R²={r2:.3f}")
                        
                        # Importancia de variables
                        importance = pd.DataFrame({
                            'feature': feature_cols,
                            'importance': model.feature_importances_
                        }).sort_values('importance', ascending=False)
                        
                        top_n = min(10, len(importance))
                        fig_imp = go.Figure()
                        fig_imp.add_trace(go.Bar(
                            y=importance.head(top_n)['feature'],
                            x=importance.head(top_n)['importance'],
                            orientation='h',
                            marker_color='teal'
                        ))
                        fig_imp.update_layout(
                            title=f"Importancia de Variables (Top {top_n})",
                            xaxis_title="Importancia",
                            yaxis_title="Variable",
                            height=max(400, top_n * 35)
                        )
                        figures.append(fig_imp)
                        
                        findings.append(f"Variables más importantes: {', '.join(importance.head(3)['feature'].tolist())}")
                        
                        # Recomendaciones
                        if is_classification and metrics.get("Accuracy", 0) < 0.7:
                            recommendations.append("Accuracy baja. Considera ajuste de hiperparámetros, más datos o feature engineering")
                        
                        if not is_classification and metrics.get("R²", 0) < 0.5:
                            recommendations.append("R² bajo. El modelo explica poco la varianza. Prueba modelos no lineales o transforma features")
                        
                        recommendations.append("Validación cruzada mejoraría la robustez de las métricas")
                        recommendations.append("Considera probar XGBoost, LightGBM o redes neuronales")
                        
                        if len(categorical_cols) > 0:
                            recommendations.append(f"Hay {len(categorical_cols)} columnas categóricas no usadas. Codifícalas con OneHotEncoder o TargetEncoder")
                    else:
                        warnings.append("Muy pocas filas válidas para entrenar modelo")
                else:
                    warnings.append("No hay suficientes features numéricas para modelar")
            else:
                warnings.append("No se pudo identificar una variable objetivo válida")
            
            # Resumen
            summary = f"Se limpiaron {len(df_clean)} filas. "
            if n_duplicates > 0:
                summary += f"Se eliminaron {n_duplicates} duplicados. "
            summary += "Se aplicó imputación y winsorización a outliers. "
            if target_col:
                summary += f"Se entrenó modelo baseline con '{target_col}' como objetivo. "
            summary += "El dataset limpio está listo para análisis avanzados."
            
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
                summary="Error en el análisis de ingeniería",
                error=str(e)
            )
