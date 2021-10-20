install:
	$(MAKE) -C backend install
	$(MAKE) -C frontend install

run-backend:
	$(MAKE) -C backend run

run-frontend:
	$(MAKE) -C frontend run

deploy-local:
	docker-compose up --build --remove-orphans

deploy-server:
	ansible-playbook ansible/deploy.yml -i ansible/inventory.ini

generate-api:
	cd backend; poetry run dotenv run python cli.py ../openapi.json
	cd frontend; npm run generate:model
