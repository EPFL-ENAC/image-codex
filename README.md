# Image Codex

## Installation

Prerequisites:

- [Make](https://www.gnu.org/software/make/)
- [Poetry](https://python-poetry.org/)
- [Node.js](https://nodejs.org/)
- Copy `secrets` folder from `//enac1files.epfl.ch/common/IT4R/github/image-codex` to this repository root

```bash
make install
```

## Run for development

```bash
make run-backend
make run-frontend
```

## Generate

Folder frontend/src/backend is generated from backend API.

```bash
# update generated files (requires Java installed)
make generate-api
```

## Deploy

### Locally

```bash
docker-compose up --build --remove-orphans
```

### Server

[Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

```bash
# Install
ansible-galaxy install -r ansible/requirements.yml
ansible-playbook ansible/install.yml -i ansible/inventory.ini

# Deploy
ansible-playbook ansible/deploy.yml -i ansible/inventory.ini
```
