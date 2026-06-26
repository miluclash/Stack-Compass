import pandas as pd
import duckdb

def salary_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Mediana y percentiles de ConvertedCompYearly agrupados por stack tecnológico.

    Parámetros
    ----------
    df : DataFrame ya filtrado (output de filter_population + clean_salary).

    Devuelve
    --------
    DataFrame con columnas [stack, median_salary, p25, p75, n] ordenado por mediana desc.
    """
    con = duckdb.connect()
    con.register('survey',df)
    result  = con.execute(
        """
        WITH exploded AS(
            SELECT 
                Region,
                UNNEST(string_split(ConvertedCompYearly, ';')) as tech
            FROM survey
            WHERE ConvertedCompYearly IS NOT NULL
            ),
        base AS(
            SELECT 
                Region,
                COUNT(*) as n
            FROM exploded
            GROUP BY Region, tech
        ),
        
        mediana AS(
            SELECT *, MEDIAN(), PERCENTILE_COUNT(0.25) as p25, PERCENTILE_COUNT(0.75) as p75, COUNT(*) as n
            FROM base
        )
        SELECT * 
        FROM mediana
        GROUP BY Region, stack
        """
    )


def satisfaction_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Puntuación media de JobSat por stack tecnológico.

    Parámetros
    ----------
    df : DataFrame ya filtrado.

    Devuelve
    --------
    DataFrame con columnas [stack, mean_jobsat, n] ordenado por satisfacción desc.
    """
    con = duckdb.connect()
    con.register('survey',df)
    result  = con.execute(
        
    )


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
    
    con = duckdb.connect()
    con.register('survey',df)
    
    result = con.execute("""
        WITH exploded AS (
            -- Primero expandimos el array aquí, donde sí está permitido
            SELECT 
                Region,
                UNNEST(string_split(LanguageHaveWorkedWith, ';')) AS tech
            FROM survey 
            WHERE LanguageHaveWorkedWith IS NOT NULL
        ),
        base AS (
            -- Luego agregamos sobre los datos ya expandidos
            SELECT tech, Region, COUNT(*) as n 
            FROM exploded
            GROUP BY Region, tech 
            HAVING n >= 15 
        ),
        ranked AS (
            SELECT *, RANK() OVER (PARTITION BY Region ORDER BY n DESC) AS rank
            FROM base
        )
        SELECT * FROM ranked
        ORDER BY Region, rank
        
    """).df()
    
    return result
