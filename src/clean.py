import pandas as pd

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

    Columnas usadas: Country, DevType.
    Devuelve un subconjunto de filas; no modifica columnas.
    """
    # TODO


def clean_salary(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas con ConvertedCompYearly nulo o en percentiles extremos (p1–p99).

    Devuelve df sin los outliers salariales para evitar distorsión en métricas.
    """
    # TODO


def normalize_multi_valued(df: pd.DataFrame, col: str, sep: str = ";") -> pd.DataFrame:
    """Expande una columna multi-valor separada por `sep` en filas individuales.

    Ejemplo: 'Python;SQL;R' → tres filas. Útil para LanguageHaveWorkedWith, etc.
    Devuelve un DataFrame con las demás columnas replicadas por fila.
    """
    # TODO
