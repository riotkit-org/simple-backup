# Installs poetry
poetry:
	pip3 install poetry poetry-plugin-export --break-system-packages

test:
	PYTHONPATH=. poetry run pytest -s .
