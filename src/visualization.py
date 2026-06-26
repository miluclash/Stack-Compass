import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import pandas as pd

NEUTRAL = "#8C8C8C"   # tech exclusiva de la región
TOP_N = 15


def _prep(df_metric, region, value_col, sort_desc=True):
    """Devuelve las TOP_N filas de df_metric para la región dada, ordenadas por value_col.

    Filtra las filas donde la columna 'Region' coincide con region, ordena
    descendentemente si sort_desc=True (ascendentemente si False) y recorta
    al máximo de TOP_N filas.
    """
    sub = df_metric[df_metric["Region"] == region].copy()
    sub = sub.sort_values(value_col, ascending=not sort_desc)
    return sub.head(TOP_N)


def _global_color_map(df_salary, df_sat, df_emp, region_es, region_eu,
                      salary_col, sat_col, emp_col):
    """Construye un mapa {tech: color} consistente para todo el dashboard.

    Recorre los tres DataFrames de métricas (salario, satisfacción, empleabilidad)
    y calcula la intersección de tecnologías que aparecen en el top de ambas
    regiones en al menos una métrica. A cada tech común le asigna un color
    único de la paleta tab20. Las techs que no están en la intersección se
    representarán con NEUTRAL (gris) al pintar las barras.
    """
    common = set()
    for df_metric, vcol in [(df_salary, salary_col),
                            (df_sat, sat_col),
                            (df_emp, emp_col)]:
        es = _prep(df_metric, region_es, vcol)
        eu = _prep(df_metric, region_eu, vcol)
        common |= set(es["tech"]) & set(eu["tech"])

    cmap = cm.get_cmap("tab20")
    return {tech: cmap(i % 20) for i, tech in enumerate(sorted(common))}


def _bar_colors(sub, color_map):
    """Devuelve la lista de colores para las barras de un subplot.

    Para cada fila de sub (ordenada como se va a dibujar) busca su tech en
    color_map. Si la tech está en el mapa devuelve su color asignado;
    si no (tech exclusiva de esa región), devuelve NEUTRAL.
    """
    return [color_map.get(t, NEUTRAL) for t in sub["tech"]]


def build_dashboard(df_salary, df_sat, df_emp,
                    region_es="España", region_eu="UE sin España",
                    salary_col="median_salary", sat_col="mean_jobsat", emp_col="n"):
    """Genera la figura comparativa España vs UE con las tres métricas clave.

    Crea una cuadrícula de 3 filas × 2 columnas (fila=métrica, columna=región).
    Cada subgráfico es un gráfico de barras horizontales con las TOP_N tecnologías
    de esa región para esa métrica:
      - Fila 0: salario mediano con barras de error p25–p75.
      - Fila 1: satisfacción media (JobSat).
      - Fila 2: empleabilidad (número de respondentes).

    Las techs comunes a ambas regiones en al menos una métrica comparten color
    entre todos los subgráficos; las exclusivas de cada región se pintan en gris.
    La leyenda global se sitúa en la parte superior de la figura.

    Devuelve el objeto matplotlib.figure.Figure resultante.
    """
    color_map = _global_color_map(
        df_salary, df_sat, df_emp, region_es, region_eu,
        salary_col, sat_col, emp_col,
    )

    fig, axes = plt.subplots(3, 2, figsize=(14, 16))

    metrics = [
        ("Salario mediano (€/año)", df_salary, salary_col, True),
        ("Satisfacción media (JobSat)", df_sat, sat_col, True),
        ("Empleabilidad (nº respondentes)", df_emp, emp_col, True),
    ]

    for row, (title, df_metric, vcol, desc) in enumerate(metrics):
        es = _prep(df_metric, region_es, vcol, desc)
        eu = _prep(df_metric, region_eu, vcol, desc)

        for col, (sub, region_label) in enumerate([(es, "España"), (eu, "UE")]):
            ax = axes[row][col]
            y_pos = range(len(sub))
            colors = _bar_colors(sub, color_map)

            ax.barh(y_pos, sub[vcol], color=colors)

            if vcol == salary_col:
                err_low = sub[vcol] - sub["p25"]
                err_high = sub["p75"] - sub[vcol]
                ax.errorbar(sub[vcol], y_pos,
                            xerr=[err_low, err_high],
                            fmt="none", ecolor="#444", elinewidth=1.2, capsize=3)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(sub["tech"])
            ax.invert_yaxis()
            ax.set_title(f"{region_label} — {title}", fontsize=11)
            ax.tick_params(labelsize=9)

    legend_handles = [
        mpatches.Patch(color=color, label=tech)
        for tech, color in color_map.items()
    ]
    legend_handles.append(mpatches.Patch(color=NEUTRAL, label="Exclusiva de la región"))
    fig.legend(handles=legend_handles, loc="upper center",
               ncol=6, fontsize=9, bbox_to_anchor=(0.5, 1.0))

    fig.suptitle("Stack Compass — España vs UE", fontsize=15, y=1.04)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    return fig