install:
	poetry install

run:
	poetry run dotenv -f ../secrets/backend.env run uvicorn image_codex.main:app --reload

test:
	poetry run pytest
