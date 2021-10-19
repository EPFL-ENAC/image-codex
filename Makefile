install: install-backend install-frontend

install-backend:
	cd backend; poetry install

install-frontend:
	cd frontend; npm install

run-backend:
	cd backend; poetry run dotenv run uvicorn image_codex.main:app --reload

run-frontend:
	npm --prefix frontend run serve

deploy-local:
	docker-compose up --build --remove-orphans

deploy-server:
	ansible-playbook ansible/deploy.yml -i ansible/inventory.ini

generate-api:
	cd backend; poetry run dotenv run python cli.py ../openapi.json
	cd frontend; npm run generate:model
