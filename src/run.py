"""Stack Compass — pipeline completo de una tirada.
Correr desde la raíz del proyecto:  python -m src.run
Hace: carga raw -> limpia -> guarda processed -> 3 métricas
-> imprime los números para el README -> genera figures/dashboard.png
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

from src.load import load_raw, PROCESSED_CSV
from src.clean import filter_population, filter_geography, add_region, clean_salary
from src.metrics import salary_by_stack, satisfaction_by_stack, employability_by_stack
from src.plots import build_dashboard

FIG_PATH = Path(__file__).parent.parent / "figures" / "dashboard.png"


def build_processed():
    df = load_raw()
    df = filter_population(df)
    df = filter_geography(df)
    df = add_region(df)
    df = clean_salary(df)
    PROCESSED_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_CSV, index=False)
    print(f"[ok] processed guardado ({len(df)} filas): {PROCESSED_CSV}")
    return df


def show(title, dframe):
    print("\n" + "=" * 60 + f"\n{title}\n" + "=" * 60)
    print(dframe.to_string(index=False))


def main():
    df = build_processed()
    salary = salary_by_stack(df)
    satis = satisfaction_by_stack(df)
    employ = employability_by_stack(df)

    show("SALARIO — mediana por stack y región", salary)
    show("EMPLEABILIDAD — % de uso por stack y región", employ)
    show("SATISFACCIÓN — % que lo repetiría (Admired)", satis)

    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig = build_dashboard(salary, satis, employ,
                          sat_col="admired_pct",  # Admired, no JobSat
                          emp_col="pct")          # %, no el conteo n
    fig.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
    print(f"\n[ok] dashboard guardado: {FIG_PATH}")


if __name__ == "__main__":
    main()