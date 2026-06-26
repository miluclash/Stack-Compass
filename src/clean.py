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
    """Conserva solo las filas cuyo DevType incluye al menos un rol data/IA del catálogo.

    DevType es una cadena con roles separados por ';'. La función parte cada celda,
    intersecta con ROLES (núcleo + frontera) y devuelve las filas donde esa
    intersección no está vacía. No modifica ni añade columnas.
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
    """Conserva solo las filas cuyo Country pertenece a los 27 estados miembro de la UE.

    La lista de países válidos está en PAISES_UE. No modifica ni añade columnas.
    """
    # 1. crear una máscara booleana para Country en PAISES_UE
    mask = df['Country'].isin(PAISES_UE)
    
    # 2. devolver solo las filas donde mask es True
    return df[mask]


def add_region(df:pd.DataFrame) -> pd.DataFrame:
    """Añade la columna 'Region' con dos valores: 'España' o 'UE sin España'.

    Asigna 'España' cuando Country == 'Spain' y 'UE sin España' para el resto.
    Devuelve una copia de df con la nueva columna; no modifica el original.
    """
    df = df.copy()  # Evitar modificar el DataFrame original
    df['Region'] = np.where(
        df['Country'] == 'Spain', 'España', 'UE sin España'
    )
    return df

def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Pone a NaN los valores de ConvertedCompYearly fuera del rango [5 000, 300 000].

    Los umbrales son fijos (no basados en percentiles): valores por debajo de 5 000 USD
    o por encima de 300 000 USD se consideran errores de reporte o casos atípicos
    extremos y se anulan para no distorsionar las métricas salariales.
    Devuelve una copia de df; no modifica el original.
    """
    df = df.copy()  # Evitar modificar el DataFrame original
    # 1. eliminar filas con ConvertedCompYearly nulo
    df.loc[
        (df['ConvertedCompYearly'] < 5000) | (df['ConvertedCompYearly'] > 300000),
        'ConvertedCompYearly'
    ] = np.nan
    
    return df

def normalize_multi_valued(df: pd.DataFrame, col: str, sep: str = ";") -> pd.DataFrame:
    """Expande una columna multi-valor en filas individuales (una tecnología por fila).

    Divide cada celda de `col` por `sep` y crea una fila por valor resultante,
    replicando el resto de columnas. Por ejemplo, una fila con
    LanguageHaveWorkedWith='Python;SQL;R' se convierte en tres filas independientes.

    Pendiente de implementar (TODO).
    """
    # TODO
