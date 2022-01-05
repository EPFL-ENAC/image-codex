install:
	$(MAKE) -C backend install
	$(MAKE) -C frontend install

run-backend:
	$(MAKE) -C backend run

run-frontend:
	$(MAKE) -C frontend run

deploy-local:
	docker-compose build --pull
	docker-compose up --remove-orphans

install-server:
	ansible-galaxy install -r ansible/requirements.yml
	ansible-playbook ansible/install.yml -i ansible/inventory.ini

deploy-prod:
	ansible-playbook ansible/deploy.yml -i ansible/inventory.ini

generate-api:
	cd backend; poetry run dotenv run python cli.py ../openapi.json
	cd frontend; npm run generate:model
