.PHONY: install test build publish

install:
	poetry install

ruff:
	poetry run ruff check --fix
	poetry run ruff check
	poetry run ruff format

ruff-format:
	poetry run ruff format

ruff-fix:
	poetry run ruff check --fix

verify: ruff

build:
	poetry build

publish:
	poetry publish
