import pandas as pd


def salary_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Mediana y percentiles de ConvertedCompYearly agrupados por stack tecnológico.

    Parámetros
    ----------
    df : DataFrame ya filtrado (output de filter_population + clean_salary).

    Devuelve
    --------
    DataFrame con columnas [stack, median_salary, p25, p75, n] ordenado por mediana desc.
    """
    # TODO


def satisfaction_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Puntuación media de JobSat por stack tecnológico.

    Parámetros
    ----------
    df : DataFrame ya filtrado.

    Devuelve
    --------
    DataFrame con columnas [stack, mean_jobsat, n] ordenado por satisfacción desc.
    """
    # TODO


def employability_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Frecuencia de aparición de cada stack en la población filtrada (proxy de empleabilidad).

    Cuenta cuántos respondentes declaran usar cada tecnología en LanguageHaveWorkedWith.

    Parámetros
    ----------
    df : DataFrame ya filtrado (filas expandidas por normalize_multi_valued).

    Devuelve
    --------
    DataFrame con columnas [stack, count, pct] ordenado por frecuencia desc.
    """
    # TODO
