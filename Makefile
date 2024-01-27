build:
	docker compose build

run:
	docker compose up

run-build:
	docker compose up --build

stop:
	docker compose down

test:
	docker compose run --rm web python -m pytest ./tests/

makemigrations:
	docker compose run --rm web python manage.py makemigrations

migrate:
	docker compose run --rm web python manage.py migrate

format:
	docker compose run --rm web python -m black . --exclude 'venv/|\.local/|\.cache/|\.git/'