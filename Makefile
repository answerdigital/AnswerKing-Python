.PHONY: clean test lint migrate

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info

lint:
	poetry run black . --line-length=79
	poetry run pycodestyle --ignore=E501 .
	poetry run pyright

test: clean
	poetry run coverage run --omit=*/migrations/*,*answerking/* manage.py test --noinput
	poetry run coverage report
	poetry run coverage html

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

prepare: lint test
