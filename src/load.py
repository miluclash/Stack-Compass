from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).parent.parent  # src/ -> raíz del proyecto
RAW_CSV = ROOT / "data" / "raw" / "results.csv"
PROCESSED_CSV = ROOT / "data" / "processed" / "survey_clean.csv"

def load_raw(path: Path = RAW_CSV) -> pd.DataFrame:
    """Carga el CSV crudo de la encuesta Stack Overflow con low_memory=False."""
    return pd.read_csv(path, low_memory=False)


def get_duckdb_connection(db_path: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """Devuelve una conexión DuckDB. Por defecto en memoria; pasa una ruta para persistir."""
    return duckdb.connect(db_path)


def load_processed(path: Path = PROCESSED_CSV) -> pd.DataFrame:
    """Carga el CSV limpio generado por el pipeline de clean.py."""
    return pd.read_csv(path, low_memory=False)
