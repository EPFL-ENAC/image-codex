# image-codex

## Project setup

```
poetry install
```

### Compiles and hot-reloads for development

```
poetry run uvicorn image_codex.main:app --reload
```

### Run CLI

```
poetry run dotenv run python cli.py -h

poetry run dotenv run python cli.py ../openapi.json
```

### Run your unit tests

```
poetry run pytest
```
