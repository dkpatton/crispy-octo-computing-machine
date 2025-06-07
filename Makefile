run:
	python run_game.py

test:
	pytest

lint:
	black .
	isort .
	ruff .
