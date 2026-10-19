.RECIPEPREFIX = >
.PHONY: help up down build dbt-build dbt-test dbt-docs lint clean

help:
> @echo "P1 — Biomedical SAV Data Platform"
> @echo "  make up         # docker compose up -d"
> @echo "  make down       # docker compose down -v"
> @echo "  make build      # docker compose build"
> @echo "  make dbt-build  # dbt build"
> @echo "  make dbt-test   # dbt test"
> @echo "  make dbt-docs   # dbt docs generate && dbt docs serve"
> @echo "  make lint       # ruff + sqlfluff"
> @echo "  make clean      # remove dbt target/ and packages"

up:
> docker compose up -d

down:
> docker compose down -v

build:
> docker compose build

dbt-build:
> dbt build

dbt-test:
> dbt test

dbt-docs:
> dbt docs generate && dbt docs serve

lint:
> ruff check . && sqlfluff lint transform/models

clean:
> rm -rf target/ dbt_packages/ logs/ .dagster/
