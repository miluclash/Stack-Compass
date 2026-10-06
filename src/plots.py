"""
Stack Compass — Figura compuesta 3×2 (Punto 8)

Fila   = métrica (salario / empleabilidad / satisfacción)
Columna = región (España / UE-sin-España)

Entrada: los 3 DataFrames que devuelven las queries de DuckDB (metrics.py).

Spec del dashboard respetada:
  · colormap tab20 GLOBAL — cada tech conserva su color en todos los paneles
  · techs presentes en una sola región → gris neutro (no son comparables)
  · eje de satisfacción arranca en 4
  · barras de error de salario = p25–p75 respecto a la mediana

>>> AJUSTA el bloque de constantes a los nombres reales de tus queries. <<<
"""
import matplotlib.pyplot as plt
import numpy as np

# ── Constantes a verificar contra tus DataFrames ──────────────────
REGION_COL, TECH_COL = "Region", "tech"
ES, EU = "España", "UE-sin-España"

COLS = {
    "salary": {"value": "median_salary", "p25": "p25", "p75": "p75"},
    "employ": {"value": "pct"},    # porcentaje 0–100, NO conteo (ojo bug M2)
    "satis":  {"value": "score"},  # % de retención, 0–100
}
TITLES = {
    "salary": "Salario mediano (USD)",
    "employ": "Empleabilidad (% de uso)",
    "satis":  "Satisfacción (% retención)",
}
GRAY = "#9aa0a6"


def _color_map(dfs):
    """Un color tab20 por tech, estable en toda la figura."""
    techs = sorted({t for df in dfs for t in df[TECH_COL].unique()})
    cmap = plt.get_cmap("tab20", max(len(techs), 1))
    return {t: cmap(i) for i, t in enumerate(techs)}


def _shared_techs(df_a, df_b):
    """Techs presentes en ambas regiones → comparables (color); el resto, gris."""
    return set(df_a[TECH_COL]) & set(df_b[TECH_COL])


def _draw(ax, df, metric, colors, shared, region_label):
    c = COLS[metric]
    d = df.sort_values(c["value"]).reset_index(drop=True)
    y = np.arange(len(d))
    bar_colors = [colors[t] if t in shared else GRAY for t in d[TECH_COL]]

    if metric == "salary":
        vals = d[c["value"]].to_numpy(dtype=float)
        lo = vals - d[c["p25"]].to_numpy(dtype=float)
        hi = d[c["p75"]].to_numpy(dtype=float) - vals
        ax.barh(y, vals, color=bar_colors,
                xerr=[lo, hi], error_kw=dict(ecolor="#555", lw=0.8, capsize=2))
    else:
        ax.barh(y, d[c["value"]].to_numpy(dtype=float), color=bar_colors)
        if metric == "satis":
            ax.set_xlim(left=4)  # spec: eje de satisfacción desde 4

    ax.set_yticks(y)
    ax.set_yticklabels(d[TECH_COL], fontsize=8)
    ax.set_title(region_label, fontsize=10, loc="left")
    ax.tick_params(axis="x", labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)


def build_figure(salary_df, employ_df, satis_df, outfile="figures/dashboard.png"):
    data = {"salary": salary_df, "employ": employ_df, "satis": satis_df}
    colors = _color_map([salary_df, employ_df, satis_df])

    fig, axes = plt.subplots(3, 2, figsize=(12, 13))
    for row, metric in enumerate(["salary", "employ", "satis"]):
        df = data[metric]
        es = df[df[REGION_COL] == ES]
        eu = df[df[REGION_COL] == EU]
        shared = _shared_techs(es, eu)
        _draw(axes[row, 0], es, metric, colors, shared, ES)
        _draw(axes[row, 1], eu, metric, colors, shared, EU)
        axes[row, 0].set_ylabel(TITLES[metric], fontsize=11)

    fig.suptitle("Stack Compass — España vs UE-sin-España", fontsize=15, y=0.995)
    fig.text(0.5, 0.005,
             "Gris = tech presente en una sola región (no comparable).  "
             "El eje de satisfacción arranca en 4, no en 0.",
             ha="center", fontsize=8, color="#666")
    fig.tight_layout(rect=[0, 0.02, 1, 0.98])
    fig.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"Figura guardada en {outfile}")
    return fig


if __name__ == "__main__":
    # TODO MICHAEL: importa tus DataFrames reales (de src.metrics o del notebook)
    #   from src.metrics import salary_df, employ_df, satis_df
    #   build_figure(salary_df, employ_df, satis_df)
    raise SystemExit(
        "Importa tus DataFrames reales antes de correr. Mira el bloque __main__."
    )
