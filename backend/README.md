# Image Codex - Backend

Backend for Image Codex: https://image-codex-enac.epfl.ch/api/docs

Created by Poetry and follows its files structure: https://python-poetry.org/docs/basic-usage/#project-setup

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
