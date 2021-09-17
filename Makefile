run-frontend:
	npm --prefix frontend run serve

run-backend:
	cd backend; poetry run uvicorn image_codex.main:app --reload
