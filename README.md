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
make run-frontend
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

### Server

Deploy on https://enacvm0062.xaas.epfl.ch/ (alias https://image-codex-enac.epfl.ch/)

Prerequisites:

- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

```bash
# Install on new server
ansible-galaxy install -r ansible/requirements.yml
ansible-playbook ansible/install.yml -i ansible/inventory.ini

# Deploy
make deploy-server
```
