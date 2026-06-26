import pandas as pd
import math
import numpy as np

ROLES_NUCLEO = [
    "Data engineer",
    "AI/ML engineer",
    "Data scientist",
    "Data or business analyst",
    "Applied scientist",
    "Developer, AI apps or physical AI",
]
ROLES_FRONTERA = [
    "DevOps engineer or professional",
    "Cloud infrastructure engineer",
]
ROLES = ROLES_NUCLEO + ROLES_FRONTERA

PAISES_UE = [
    "Germany", "France", "Netherlands", "Spain", "Italy", "Poland",
    "Sweden", "Austria", "Portugal", "Belgium", "Denmark", "Finland",
    "Ireland", "Czech Republic", "Romania", "Hungary", "Greece",
    "Bulgaria", "Croatia", "Slovakia", "Slovenia", "Lithuania",
    "Latvia", "Estonia", "Luxembourg", "Cyprus", "Malta",
]


def filter_population(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra la encuesta a roles data/IA (núcleo + frontera) en países de la UE.

    Columnas usadas: DevType.
    Devuelve un subconjunto de filas; no modifica columnas.
    """
    def belongs(cell):
        if pd.isna(cell):
            return False
        roles_persona = cell.split(';')
        comunes = set(roles_persona) & set(ROLES)
        return len(comunes) > 0
    
    # 1. crear una máscara booleana aplicando belongs a cada celda de DevType
    mask = df['DevType'].apply(belongs)
    
    # 2. devolver solo las filas donde mask es True
    return df[mask] 

def filter_geography(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra la encuesta a países de la UE.

    Columnas usadas: Country.
    Devuelve un subconjunto de filas; no modifica columnas.
    """
    # 1. crear una máscara booleana para Country en PAISES_UE
    mask = df['Country'].isin(PAISES_UE)
    
    # 2. devolver solo las filas donde mask es True
    return df[mask]


def add_region(df:pd.DataFrame) -> pd.DataFrame:
    """Agrega una columna Region con valor 'UE' para todos los registros.

    Devuelve df con la nueva columna.
    """
    df = df.copy()  # Evitar modificar el DataFrame original
    df['Region'] = np.where(
        df['Country'] == 'Spain', 'España', 'UE sin España'
    )
    return df

def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia los valores de ConvertedCompYearly nulos o en percentiles extremos (p1–p99).

    Devuelve df sin los outliers salariales para evitar distorsión en métricas.
    """
    df = df.copy()  # Evitar modificar el DataFrame original
    # 1. eliminar filas con ConvertedCompYearly nulo
    df.loc[
        (df['ConvertedCompYearly'] < 5000) | (df['ConvertedCompYearly'] > 300000),
        'ConvertedCompYearly'
    ] = np.nan
    
    return df

def normalize_multi_valued(df: pd.DataFrame, col: str, sep: str = ";") -> pd.DataFrame:
    """Expande una columna multi-valor separada por `sep` en filas individuales.

    Ejemplo: 'Python;SQL;R' → tres filas. Útil para LanguageHaveWorkedWith, etc.
    Devuelve un DataFrame con las demás columnas replicadas por fila.
    """
    # TODO
