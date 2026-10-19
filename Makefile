.RECIPEPREFIX = >
.PHONY: help bootstrap run dbt-build dbt-test dbt-docs lint clean reset

PY ?= python3.12
VENV ?= .venv
BIN := $(VENV)/bin

help:
> @echo "P1 — Biomedical SAV Data Platform"
> @echo "  make bootstrap   # create venv + install pinned deps + dbt deps"
> @echo "  make run         # run pipeline: ingest -> dbt build"
> @echo "  make dbt-build   # dbt build"
> @echo "  make dbt-test    # dbt test"
> @echo "  make dbt-docs    # dbt docs generate && dbt docs serve"
> @echo "  make lint        # ruff + sqlfluff"
> @echo "  make clean       # remove dbt target/ and packages"
> @echo "  make reset       # clean + remove generated data/ and DuckDB file"

bootstrap:
> $(PY) -m venv $(VENV)
> $(BIN)/pip install --upgrade pip
> $(BIN)/pip install -r requirements.txt
> cd transform && ../$(BIN)/dbt deps

run:
> @echo "TODO: wire ingest + dbt build into a single command at Step 2"

dbt-build:
> cd transform && ../$(BIN)/dbt build

dbt-test:
> cd transform && ../$(BIN)/dbt test

dbt-docs:
> cd transform && ../$(BIN)/dbt docs generate && ../$(BIN)/dbt docs serve

lint:
> $(BIN)/ruff check .
> $(BIN)/sqlfluff lint transform/models

clean:
> rm -rf transform/target transform/dbt_packages transform/logs .dagster

reset: clean
> rm -rf data/
> mkdir -p data && touch data/.gitkeep