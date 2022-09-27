# Image Codex

https://image-codex-enac.epfl.ch/

## Development

### Installation

Prerequisites:

- [Make](https://www.gnu.org/software/make/)
- [Poetry](https://python-poetry.org/)
- [Node.js](https://nodejs.org/)
- Copy `secrets` folder from `//enac1files.epfl.ch/common/IT4R/github/image-codex` to this repository root

```bash
make install
```

### Run for development

#### CLI

```bash
make run-backend
# http://127.0.0.1:8080

make run-frontend
# http://127.0.0.1:8000
```

#### Visual Studio Code

Some run configurations are in `.vscode`: https://code.visualstudio.com/docs/editor/debugging

## Generate API for frontend

Folder frontend/src/backend is generated from backend API. It should be updated when the backend api changes.

```bash
# update generated files (requires Java installed)
make generate-api
```

## Deployment

### Locally with Docker Compose

```bash
make deploy-local
```

## Build

In Docker (if you don't have the correct python version installed)

```bash
cd backend
docker build -f Dockerfile-build -t image-codex-build .

# linux
docker run -v $(pwd):/app image-codex-build poetry update
# cmd
docker run -v %cd%:/app image-codex-build poetry update
```
