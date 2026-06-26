import pandas as pd
import duckdb

def salary_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula mediana salarial y percentiles p25/p75 por tecnología y región.

    Usa DuckDB para expandir la columna LanguageHaveWorkedWith (separada por ';')
    y agrupa por (Region, tech). Excluye grupos con menos de 15 respondentes.

    Parámetros
    ----------
    df : DataFrame ya filtrado (output de filter_population + clean_salary),
         con columnas Region, LanguageHaveWorkedWith y ConvertedCompYearly.

    Devuelve
    --------
    DataFrame con columnas [Region, tech, median_salary, p25, p75, n],
    ordenado por Region y median_salary descendente.
    """
    con = duckdb.connect()
    con.register('survey',df)
    result  = con.execute(
        """
        WITH exploded AS(
            SELECT 
                Region,
                UNNEST(string_split(LanguageHaveWorkedWith, ';')) as tech,
                ConvertedCompYearly
            FROM survey
            WHERE ConvertedCompYearly IS NOT NULL
            ),
        base AS(
            SELECT Region, tech,
            MEDIAN(ConvertedCompYearly) AS median_salary,
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ConvertedCompYearly) AS p25,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ConvertedCompYearly) AS p75,
            COUNT(*) AS n
            FROM exploded
            WHERE ConvertedCompYearly IS NOT NULL
            GROUP BY Region, tech
            HAVING n >= 15
        )
        SELECT * 
        FROM base
        ORDER BY Region, median_salary DESC
        """
    ).df()
    
    return result


def satisfaction_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la satisfacción laboral media (JobSat) por tecnología y región.

    Usa DuckDB para expandir LanguageHaveWorkedWith (separada por ';') y calcula
    AVG(JobSat) por (Region, tech). Excluye grupos con menos de 15 respondentes.

    Parámetros
    ----------
    df : DataFrame ya filtrado, con columnas Region, LanguageHaveWorkedWith y JobSat.

    Devuelve
    --------
    DataFrame con columnas [Region, tech, mean_jobsat, n],
    ordenado por Region y mean_jobsat descendente.
    """
    con = duckdb.connect()
    con.register('survey',df)
    result  = con.execute(
        """ 
        WITH exploded AS(
            SELECT 
                Region,
                UNNEST(string_split(LanguageHaveWorkedWith, ';'))as tech,
                JobSat
            FROM survey
            WHERE LanguageHaveWorkedWith IS NOT NULL
        ),
        base AS(
            SELECT 
                Region,
                tech,
                AVG(JobSat) as mean_jobsat,
                COUNT(*) as n
            FROM exploded
            WHERE JobSat IS NOT NULL
            GROUP BY Region, tech 
            HAVING n >=15
        )
        SELECT * 
        FROM base
        ORDER BY Region,mean_jobsat DESC
        """
    ).df()
    
    return result


def employability_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Cuenta respondentes por tecnología y región como proxy de empleabilidad.

    Usa DuckDB para expandir LanguageHaveWorkedWith (separada por ';'), cuenta
    cuántos respondentes declaran cada tecnología por (Region, tech) y asigna
    un ranking dentro de cada región según esa frecuencia. Excluye grupos con
    menos de 15 respondentes. El DataFrame de entrada no necesita estar pre-expandido.

    Parámetros
    ----------
    df : DataFrame ya filtrado, con columnas Region y LanguageHaveWorkedWith.

    Devuelve
    --------
    DataFrame con columnas [tech, Region, n, rank],
    ordenado por Region y rank ascendente (rank=1 es la tech más frecuente).
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
