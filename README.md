# Stack Compass

Análisis de la **Stack Overflow Annual Developer Survey** para identificar qué stacks tecnológicos maximizan **salario, satisfacción y empleabilidad** para un perfil data-IA junior en España o Europa remota.

## Stack técnico

- **pandas** — ingesta, limpieza y normalización
- **DuckDB** — SQL embebido para métricas y window functions
- **matplotlib + seaborn** — visualización
- **Jupyter** — análisis narrado

**Flujo:** `data/raw/results.csv` → `clean.py` → `data/processed/` → `metrics.py` → notebook

## Estructura

```
stack-compass/
├── data/
│   ├── raw/                 # CSV crudo de la encuesta (no versionado)
│   └── processed/           # salida del pipeline de limpieza
├── notebooks/
│   └── 01_analisis.ipynb    # análisis narrado
├── src/
│   ├── load.py              # load_raw(), get_duckdb_connection(), load_processed()
│   ├── clean.py             # filter_population(), clean_salary(), normalize_multi_valued()
│   └── metrics.py           # salary_by_stack(), satisfaction_by_stack(), employability_by_stack()
├── pyproject.toml
└── README.md
```

## Instalación

Requiere [uv](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/miluclash/Stack-Compass.git
cd stack-compass
uv sync
```

## Uso

```bash
# Jupyter para el análisis narrado
uv run jupyter notebook notebooks/01_analisis.ipynb
```

## Estado

- [x] Fase 0 — setup y estructura de módulos
- [ ] Fase 1 — limpieza (`clean.py`) y métricas (`metrics.py`)
- [ ] Fase 2 — notebook narrado con conclusiones
