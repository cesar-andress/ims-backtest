# IMSFE 2.0

Reproducible international market selection (IMS) framework with predictive
validation, robustness checks, and an open data pipeline. Design decisions live
in [`SPEC.md`](SPEC.md). Phase prompts for Cursor are in [`PROMPTS.md`](PROMPTS.md).

## Requirements

- Python 3.11
- [`uv`](https://github.com/astral-sh/uv)
- Quarto (manuscript rendering only; not required for `make test`)

## Install

```bash
uv sync
```

Or via Make:

```bash
make install
```

## Run the full pipeline

When data download and analysis modules are implemented:

```bash
make all
```

This runs, in order: `imsfe download` → `imsfe build` → `imsfe run` → `imsfe report`.

Individual targets:

| Target | Command |
|--------|---------|
| `make data` | download sources into `data/raw/` |
| `make build` | panel, features, outcomes |
| `make analysis` | normalisation / MCDM / weights grid |
| `make outputs` | tables and figures under `outputs/` |
| `make legacy` | reproduce and audit the original Excel ranking |
| `make lint` | `ruff check` |
| `make test` | `pytest` |

## Configuration

- `config/settings.yaml` — origins, HS chapters, years, thresholds, seeds
- `config/variables.yaml` — criteria (factor, direction, source, transform)
- `config/experiments.yaml` — normalisation × MCDM × weight grid
- `config/weights_expert.yaml` — filled by `imsfe legacy` (Phase 1)

## Quality rules

No fabricated data. Every manuscript number must come from `outputs/` generated
by code. Features at year *t* may only use information with year ≤ *t*.

Original submission materials under `../old_submission/` are **read-only**.
