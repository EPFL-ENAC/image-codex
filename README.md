# Image Codex

## Run

```bash
make run-frontend
make run-backend
```

## Generate

Folder frontend/src/generated is generated from backend API.

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
