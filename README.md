# image-codex

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your unit tests
```
npm run test:unit
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Deploy
[Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
```
# Install
ansible-galaxy install -r ansible/requirements.yml
ansible-playbook ansible/install.yml -i ansible/inventory.ini

# Deploy
ansible-playbook ansible/deploy.yml -i ansible/inventory.ini
```
