run-frontend:
	npm --prefix frontend run serve

run-backend:
	cd backend; poetry run dotenv run uvicorn image_codex.main:app --reload

deploy-local:
	docker-compose up --build --remove-orphans

deploy-server:
	ansible-playbook ansible/deploy.yml -i ansible/inventory.ini
