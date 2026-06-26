from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).parent.parent  # src/ -> raíz del proyecto
RAW_CSV = ROOT / "data" / "raw" / "results.csv"
PROCESSED_CSV = ROOT / "data" / "processed" / "survey_clean.csv"

def load_raw(path: Path = RAW_CSV) -> pd.DataFrame:
    """Lee el CSV crudo de la encuesta Stack Overflow y devuelve un DataFrame con todas sus columnas.

    Usa low_memory=False para evitar advertencias de inferencia de tipos mixtos
    en columnas de texto largas (DevType, LanguageHaveWorkedWith, etc.).
    """
    return pd.read_csv(path, low_memory=False)


def get_duckdb_connection(db_path: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """Abre y devuelve una conexión DuckDB.

    Por defecto crea una base de datos en memoria (`:memory:`) que desaparece al cerrar
    la conexión. Pasa una ruta de archivo para persistir la base de datos en disco.
    """
    return duckdb.connect(db_path)


def load_processed(path: Path = PROCESSED_CSV) -> pd.DataFrame:
    """Lee el CSV limpio producido por el pipeline de clean.py y devuelve un DataFrame.

    El archivo esperado es data/processed/survey_clean.csv: población ya filtrada
    por roles data/IA y geografía UE, con la columna Region añadida y
    ConvertedCompYearly saneada.
    """
    return pd.read_csv(path, low_memory=False)
