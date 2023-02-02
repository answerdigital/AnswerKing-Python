.PHONY: clean test lint migrate

clean:
	-rm -r htmlcov
	-rm -r .coverage
	-rm -r build
	-rm -r dist
	-rm -r src/*.egg-info

lint:
	poetry run black . --line-length=79
	poetry run pycodestyle . --max-line-length=100
	poetry run pyright

test: clean
	poetry run coverage run --omit=*/migrations/*,*answerking/*,*/tests/*,*manage.py manage.py test --noinput
	poetry run coverage report
	poetry run coverage html

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

colon := :

runGunicorn:
	poetry run gunicorn -b 0.0.0.0$(colon)8000 answerking.wsgi$(colon)application

waitAndMigrate:
	poetry run python manage.py waitForDB
	poetry run python manage.py migrate

dockerRunserver: waitAndMigrate runGunicorn

prepare: lint test
