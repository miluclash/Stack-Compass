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
    """Satisfacción = % de retención (Admired) por tecnología y región.

    Para cada tech: de los que la USARON (LanguageHaveWorkedWith), qué fracción
    la ADMIRA (LanguageAdmired = usó Y repetiría). Score 0-100. Solo techs con
    n_used >= 15. Devuelve [Region, tech, n, admired_pct].
    """
    con = duckdb.connect()
    con.register('survey', df)
    result = con.execute("""
        WITH used AS (
            SELECT ResponseId, Region,
                   trim(UNNEST(string_split(LanguageHaveWorkedWith, ';'))) AS tech
            FROM survey WHERE LanguageHaveWorkedWith IS NOT NULL
        ),
        admired AS (
            SELECT ResponseId, Region,
                   trim(UNNEST(string_split(LanguageAdmired, ';'))) AS tech
            FROM survey WHERE LanguageAdmired IS NOT NULL
        ),
        used_counts AS (
            SELECT Region, tech, COUNT(DISTINCT ResponseId) AS n_used
            FROM used WHERE tech <> '' GROUP BY Region, tech
        ),
        admired_counts AS (
            SELECT Region, tech, COUNT(DISTINCT ResponseId) AS n_admired
            FROM admired WHERE tech <> '' GROUP BY Region, tech
        )
        SELECT u.Region, u.tech, u.n_used AS n,
               COALESCE(a.n_admired, 0) * 100.0 / u.n_used AS admired_pct
        FROM used_counts u
        LEFT JOIN admired_counts a USING (Region, tech)
        WHERE u.n_used >= 15
        ORDER BY u.Region, admired_pct DESC
    """).df()
    return result

def employability_by_stack(df: pd.DataFrame) -> pd.DataFrame:
    """Empleabilidad = % de respondentes que declara cada tech, por región.

    Expande LanguageHaveWorkedWith (separada por ';'), cuenta personas distintas
    por (Region, tech) y lo divide entre el total de personas que contestaron la
    pregunta de stack en esa región. Así el % es comparable entre España y UE pese
    a la diferencia de tamaño de muestra. Solo se devuelven techs con n >= 15.

    Devuelve [tech, Region, n, pct, rank], ordenado por Region y rank ascendente.
    """
    con = duckdb.connect()
    con.register('survey', df)

    result = con.execute("""
        WITH exploded AS (
            SELECT
                ResponseId,
                Region,
                trim(UNNEST(string_split(LanguageHaveWorkedWith, ';'))) AS tech
            FROM survey
            WHERE LanguageHaveWorkedWith IS NOT NULL
        ),
        tech_counts AS (                       -- numerador: personas por tech
            SELECT Region, tech, COUNT(DISTINCT ResponseId) AS n
            FROM exploded
            WHERE tech <> ''
            GROUP BY Region, tech
        ),
        region_totals AS (                     -- denominador: personas por región
            SELECT Region, COUNT(DISTINCT ResponseId) AS region_n
            FROM survey
            WHERE LanguageHaveWorkedWith IS NOT NULL
            GROUP BY Region
        )
        SELECT
            t.tech,
            t.Region,
            t.n,
            t.n * 100.0 / r.region_n AS pct,
            RANK() OVER (PARTITION BY t.Region ORDER BY t.n DESC) AS rank
        FROM tech_counts t
        JOIN region_totals r USING (Region)
        WHERE t.n >= 15
        ORDER BY t.Region, rank
    """).df()

    return result
