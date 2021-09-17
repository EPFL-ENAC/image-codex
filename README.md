# Image Codex

## Run
```bash
make run-frontend
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
