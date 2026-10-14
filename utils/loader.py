"""Carga y validación de archivos de datos."""
import pandas as pd
import streamlit as st
from pathlib import Path


def load_data_file(uploaded_file, sheet_name: str = None) -> pd.DataFrame:
    """
    Carga archivo CSV, XLS o XLSX con validaciones.
    
    Args:
        uploaded_file: Archivo cargado desde st.file_uploader
        sheet_name: Nombre de hoja (solo para Excel)
        
    Returns:
        DataFrame cargado
        
    Raises:
        ValueError: Si el archivo es inválido
    """
    if uploaded_file is None:
        raise ValueError("No se proporcionó archivo")
    
    # Validar tamaño (max 200 MB)
    file_size_mb = uploaded_file.size / (1024 ** 2)
    if file_size_mb > 200:
        raise ValueError(f"Archivo muy grande ({file_size_mb:.1f} MB). Máximo: 200 MB")
    
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    try:
        if file_extension == '.csv':
            # Intentar con diferentes encodings y separadores
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
                for sep in [',', ';', '\t']:
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding=encoding, sep=sep)
                        if df.shape[1] > 1:  # Asegurar que se detectaron columnas
                            break
                    except:
                        continue
                else:
                    continue
                break
            else:
                raise ValueError("No se pudo detectar formato CSV válido")
                
        elif file_extension in ['.xlsx', '.xls']:
            engine = 'openpyxl' if file_extension == '.xlsx' else 'xlrd'
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine=engine)
        else:
            raise ValueError(f"Formato no soportado: {file_extension}")
        
        # Validaciones
        if df.empty:
            raise ValueError("El archivo está vacío")
        
        if df.shape[1] == 0:
            raise ValueError("No se detectaron columnas")
        
        if df.shape[0] == 0:
            raise ValueError("No hay filas de datos")
        
        # Detectar columnas de fecha
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
        
        return df
        
    except Exception as e:
        raise ValueError(f"Error al cargar archivo: {str(e)}")


def get_excel_sheets(uploaded_file) -> list[str]:
    """
    Obtiene lista de hojas de un archivo Excel.
    
    Args:
        uploaded_file: Archivo Excel cargado
        
    Returns:
        Lista de nombres de hojas
    """
    try:
        uploaded_file.seek(0)
        file_extension = Path(uploaded_file.name).suffix.lower()
        engine = 'openpyxl' if file_extension == '.xlsx' else 'xlrd'
        xl_file = pd.ExcelFile(uploaded_file, engine=engine)
        return xl_file.sheet_names
    except:
        return []


def sample_large_dataframe(df: pd.DataFrame, max_rows: int = 100000) -> tuple[pd.DataFrame, bool]:
    """
    Muestrea DataFrame si es muy grande.
    
    Args:
        df: DataFrame a verificar
        max_rows: Límite de filas
        
    Returns:
        Tupla (DataFrame muestreado, fue_muestreado)
    """
    if len(df) > max_rows:
        sampled = df.sample(max_rows, random_state=42)
        return sampled, True
    return df, False
