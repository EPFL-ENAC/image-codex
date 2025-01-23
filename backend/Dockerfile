FROM python:3.10-alpine as build-stage
WORKDIR /app
RUN apk add --no-cache \
    gcc \
    musl-dev
RUN pip install poetry
RUN pip install --user poetry-plugin-export
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry export --output requirements.txt


FROM python:3.10-slim as production-stage
EXPOSE 80
WORKDIR /app

COPY --from=build-stage /app/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./image_codex /app/image_codex

CMD [ "uvicorn", "image_codex.main:app", "--host", "0.0.0.0", "--port", "80" ]
