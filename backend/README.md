# Image Codex - Backend

Backend for Image Codex.

API Documentation:
- http://localhost:8000/docs
- https://image-codex-enac.epfl.ch/api/docs

Module `image_codex` is created by Poetry and follows its files structure: https://python-poetry.org/docs/basic-usage/#project-setup

Entrypoint: `image_codex.main`

## Commands

```bash
# Project setup
make install

# Run and hot-reloads for development
make run

# Run unit tests
make test
```

## Run CLI

```bash
poetry run dotenv run python cli.py -h

poetry run dotenv run python cli.py ../openapi.json
```
