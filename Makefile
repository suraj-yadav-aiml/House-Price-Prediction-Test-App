.PHONY: run install clean check runner
.DEFAULT_GOAL:=runner

run: install
	cd src; poetry run python runner.py

install: pyproject.toml
	poetry install

clean:
	rm -rf `find . -type d -name __pycache__`
	# rm -rf .ruff_cache

check:
	poetry run ruff check .

runner: check run clean

