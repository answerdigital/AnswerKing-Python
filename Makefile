.PHONY: clean test

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info

test: clean
	-poetry run coverage run --omit="/migrations/, answerking/" manage.py test
	-poetry run coverage report
	-poetry run coverage html

format:
	-poetry run black . --line-length=79
	-poetry run pycodestyle --ignore=E501 .
	-poetry run pyright

all: format clean test
