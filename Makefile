.PHONY: clean test lint migrate

clean:
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info

lint:
	poetry run black . --line-length=79
	poetry run pycodestyle . --max-line-length=500
	poetry run pyright

test: clean
	poetry run coverage run --omit=*/migrations/*,*answerking/*,*/tests/*,*manage.py manage.py test --noinput
	poetry run coverage report
	poetry run coverage html

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dockerRunserver:
	poetry run python manage.py waitForDB
	poetry run python manage.py migrate
	poetry run gunicorn -b 0.0.0.0\:8000 answerking.wsgi\:application

prepare: lint test
