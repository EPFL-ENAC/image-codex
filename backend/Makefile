install:
	poetry install
	poetry run pre-commit install

run:
	poetry run dotenv -f ../secrets/backend.env run uvicorn image_codex.main:app --reload

test:
	poetry run pytest

lint:
	poetry run pre-commit run --all-files
